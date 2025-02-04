# Use the official Spark image from Docker Hub
FROM bitnami/spark:3.1.2

USER root

RUN mkdir -p data/ && mkdir -p /opt/spark/

# Add /.local/bin to the PATH to make installed scripts accessible
ENV PATH="/.local/bin:${PATH}"

# Set the working directory in the container
WORKDIR /opt/spark

# Copy your Spark job (Python script) into the container
COPY ./spark /opt/spark/

RUN pip install --user --no-cache-dir --upgrade pip && pip install --user --no-cache-dir -r /opt/spark/requirements.txt

# Expose the Spark port (optional)
EXPOSE 7077

CMD ["/.local/bin/spark-submit", "--master", "local[*]", "/opt/spark/main.py"]