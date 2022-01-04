# Kubernetes Cluster

Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications. It is the de-facto solution for deploying applications today. Machine learning services also can take advantage of Kubernetes’ ability to quickly deploy and scale base on demand.

Pre-requisites:

- Kubernetes Cluster
    - minikube is the recommended way to run Kubernetes locally: https://kubernetes.io/docs/tasks/tools/install-minikube/
    - Kubernetes guide: https://kubernetes.io/docs/setup/

- kubectl CLI tool
    - Install instruction: https://kubernetes.io/docs/tasks/tools/install-kubectl/

- Docker and Docker Hus is properly configured on your system
    - Install instruction: https://docs.docker.com/install

Tutorial : [Kubernetes Tutorial](https://github.com/dudeperf3ct/9-fastapi-kubernetes-monitoring/tree/main/tutorials)

## Run

Push the docker image of the application to docker hub registry.

```bash
# find the local path of the latest saved bundle
saved_path=$(bentoml get TransformerSentimentService:latest --print-location --quiet)
# replace {docker_username} with your Docker Hub username
docker build -t {docker_username}/sentiment-classifier $saved_path
docker login
docker push {docker_username}/sentiment-classifier
minikube start # create a kubernetes cluster
```

`sentiment-classifier.yaml` specifies the resources required to run and expose BentoML service in a Kubernetes cluster. In `sentiment-classifier.yaml`, replace `docker_username` with your docker username.

Deploy the application to Kubernetes cluster

```bash
kubectl apply -f sentiment-classifier.yaml
```

Optional : if `kubectl get service` returns `Pending` state for `EXTERNAL-IP` corresponding to `NAME` of our service. Since, we are deploying and testing application locally using `LoadBalancer` service. Minikube [doesn't support](https://stackoverflow.com/questions/55462654/access-minikube-loadbalancer-service-from-host-machine) `LoadBalancer` service and this service is compatible only with cloud services.

```bash
kubectl delete -f sentiment-classifier.yaml # delete the previous deployment and service
minikube tunnel # in separate terminal
kubectl apply -f sentiment-classifier.yaml  # start new deployment and service
```

Test the application locally

```bash
curl -i -X POST http://{service-external-ip}:5000/predict -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you\"}"
```

Else with the following, the predict api is accessible at `http://localhost:5000`

```bash
kubectl port-forward <pod-name> 5000:5000 # forward pod port
```

Test the application locally

```bash
curl -i -X POST http://localhost:5000/predict -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you\"}"
```

Access the Kubernetes dashboard: https://www.replex.io/blog/how-to-install-access-and-add-heapster-metrics-to-the-kubernetes-dashboard

Remove the deployment

```bash
kubectl delete -f sentiment-classifier.yaml
minikube stop
```

## Exercises

- Add monitoring to the application using Prometheus and Grafana: https://docs.bentoml.org/en/0.13-lts/guides/monitoring.html