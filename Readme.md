# INSTRUCTIONS TO BUILD AND RUN

1. Build the image: Inside the project directory, execute:
```
docker build -t dataverse-preprocessing .
```
2. Run the container: It is important to forward a local port to the port 8080, where the Spark UI is running.
 - Note that by default the running master is local[*]. For production workloads, yarn[*] ks preferred, although this requires a proper hdfs-site.yml and yarn-site.xml set up which I do not have right now set.

```
docker run -it --rm -v $(pwd)/spark:/opt/spark -p 7077:7077 -p 4040:4040  dataverse-preprocessing
```

3. Monitor your job at the spark UI: https://localhost:4040