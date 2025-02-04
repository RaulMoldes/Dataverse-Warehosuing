# INSTRUCTIONS TO BUILD AND RUN LOCALLY

1. Build the image: Inside the project directory, execute:
```
docker build -t dataverse-preprocessing .
```
Optionally, you can force docker to use the buildkit which is a new feature to it for performing image builds:

```
DOCKER_BUILDKIT=1 docker build -t dataverse-preprocessing .
```
Note that this requires to have the /etc/docker/daemon.json configuration set this way:
```
{
  "features": {
    "buildkit": true
  }
}
```
For more info on the docker buildkit: https://docs.docker.com/build/buildkit/

2. Run the container: It is important to forward a local port to the port 8080, where the Spark UI is running.
 - Note that by default the running master is local[*]. For production workloads, yarn[*] ks preferred, although this requires a proper hdfs-site.yml and yarn-site.xml set up which I do not have right now set.

```
docker run -it --rm -v $(pwd)/spark:/opt/spark -p 7077:7077 -p 4040:4040  dataverse-preprocessing
```

3. Monitor your job at the spark UI: https://localhost:4040


# INSTRUCTIONS TO BUILD AND RUN ON KUBERNETES

1. Make sure minikube and kubectl are installed.

2. Start a minikube cluster with 4 vcpus and 8000 MB of memory. Enable addons for monitoring and ingress.
```
minikube start --memory=8192 --cpus=4

minikube addons enable ingress

minikube addons enable metrics-server

```
3. Since Spark needs Hadoop + Yarn, deploy Hadoop and YARN on Kubernetes using helm provider.
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install hadoop bitnami/hadoop --set yarn.enabled=true
```
This deploys:
-  HDFS (Storage)
-   YARN (Resource Manager)
-   MapReduce (For computations)

You can check the running pods via:
```
 kubectl get pods 
```
4. Deploy apache spark on minikube using the spark operator
```
git clone https://github.com/GoogleCloudPlatform/spark-on-k8s-operator.git
cd spark-on-k8s-operator

kubectl create namespace spark
kubectl apply -f manifest/spark-operator.yaml

```

5. Submit your job to the spark cluster

```
kubectl exec -it <spark-driver-pod> -- /opt/spark/bin/spark-submit \
    --master yarn \
    --deploy-mode cluster \
    --conf spark.executor.instances=4 \
    --conf spark.executor.cores=2 \
    --conf spark.executor.memory=4g \
    --conf spark.driver.memory=4g \
    --conf spark.sql.shuffle.partitions=32 \
    $(pwd)/spark/main.py
```

6. Monitor:
```
    kubectl get pods -n spark
    kubectl port-forward <spark-driver-pod> 4040:4040

```
