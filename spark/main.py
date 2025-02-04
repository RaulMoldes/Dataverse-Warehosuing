from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pyspark.sql.functions as F
import requests
import json
from datetime import datetime
import os
import tempfile
import bz2
import io
from constants import PREPROCESSING_CONFIG, DOI, DATAVERSE, DOWNLOADS, DATA_PATH
from functions import coalesce_column, set_min_value, set_max_value
import shutil
import time as t

def preprocess_df(df, config: dict):
    """
    Preprocesses the DataFrame based on the configuration dictionary.

    :param df: The DataFrame to preprocess
    :param config: A dictionary containing the preprocessing parameters
    :return: Processed DataFrame
    """
    # Iterate through the config and apply preprocessing functions
    for column, params in config.items():
        if 'coalesce' in params:
            # Apply coalesce_column for columns with 'coalesce' key
            df = coalesce_column(df, column, params['coalesce'], params.get('coalesced_value', None))
        
        if 'set_min_value' in params:
            # Apply set_min_value for columns with 'set_min_value' key
            df = set_min_value(df, column, params['set_min_value'])
        
        if 'set_max_value' in params:
            # Apply set_max_value for columns with 'set_max_value' key
            df = set_max_value(df, column, params['set_max_value'])
    
    return df

## Initialize spark

# Crear una sesión de Spark y habilitar Hive

spark = SparkSession.builder.appName("DATAVERSE_APP") \
    .enableHiveSupport().getOrCreate()


# Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")

## CLEAN UP FROM PREVIOUS EXECUTIONS
if os.path.exists(f'{DATA_PATH}/spark-warehouse/'):
    shutil.rmtree(f'{DATA_PATH}/spark-warehouse/')

if os.path.exists(f'{DATA_PATH}/metadata/'):
    shutil.rmtree(f'{DATA_PATH}/metadata/')

if os.path.exists(f'{DATA_PATH}/metastore_db/'):
    shutil.rmtree(f'{DATA_PATH}/metastore_db/')

response = requests.get(DATAVERSE)

if response.status_code == 200:
  
    dataset_info = response.json()
    files = dataset_info['data']['latestVersion']['files']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Downloaded at: {time}")
    
    # Filter only csv files
    data_files = [file['dataFile'] for file in files if file['categories'] == ['2. Data']]
    print("Files to be processed:", len(data_files))
    final_df = None
    for file in data_files:
        print(f"File Name: {file['filename']}")
        file_id = file.get('id', None)
        file['downloaded_at'] = time
        print(file)
        if file_id is not None:
            file_url = f"{DOWNLOADS}{file_id}"
            file["download_url"] = file_url
            print(f"Download URL: {file_url}")
            # Download the data and store locally
            if not os.path.exists(f"{DATA_PATH}/metadata/"):
              os.makedirs(f"{DATA_PATH}/metadata/")

            if not os.path.exists(f"{DATA_PATH}/metadata/{time}/"):
                os.makedirs(f"{DATA_PATH}/metadata/{time}/")  

            with open(f"{DATA_PATH}/metadata/{time}/{file_id}.json", "w") as f:
                json.dump(file, f)

            # Download the CSV data from the URL
            csv_response = requests.get(file_url)

            if csv_response.status_code == 200:
              # Descomprimir el contenido del archivo en memoria
              with bz2.BZ2File(io.BytesIO(csv_response.content), 'rb') as file:
                  decompressed_data = file.read()

              # Guardar los datos descomprimidos en un archivo temporal
              with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
                  temp_file.write(decompressed_data)
                  temp_file_path = temp_file.name
    
              start_time = t.time()
              # Leer el archivo CSV descomprimido en un DataFrame de Spark
              df = spark.read.csv(temp_file_path, header=True, inferSchema=True)
              read_time = t.time()
              print(f"Read time: {read_time - start_time}")
              df = preprocess_df(df, PREPROCESSING_CONFIG)
              preprocess_time = t.time()
              print(f"Preprocess time: {preprocess_time - read_time}") 

              if final_df is None:
                final_df = df  # Si es la primera tabla, asignarla directamente
              else:
                final_df = final_df.unionByName(df, allowMissingColumns=True)  # Unir manteniendo columnas
            
                final_df.coalesce(32)  # Coalesce the DataFrame

              write_time = t.time() 
              print("Write time: ", write_time - preprocess_time)
              # df.explain(True)
              
        else:
          print(f"Download url not found", file.keys())
    

    if final_df is not None:
        table_name = f"flights_{time}"
        start_time = t.time()
        print(f"Writing file {table_name}")
        final_df.write.bucketBy(32, "FlightNum").sortBy("FlightNum").format("parquet").option("compression", "snappy").mode("overwrite").saveAsTable(table_name)
        print("Writing time", t.time() - start_time)
        # df.explain(True)

else:
    print(f"Error al obtener los datos: {response.status_code}")

