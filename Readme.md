# Sentiment Classification

In this exercise, we will use BentoML library to deploy the sentiment classification model from Hugging Face :hugs: on following services. BentoML supports wide range of deployment options mentioned [here](#deployment-options).

- [AWS Lambda Deployment](aws%20lambda/Readme.md)
- [Azure Functions Deployment](azure%20functions/Readme.md)
- [Kubernetes Cluster Deployment](kubernetes/Readme.md)

## BentoML

BentoML is super cool :rocket:!

[BentoML](http://bentoml.ai/) is an open-source framework for machine learning model serving, aiming to bridge the gap between Data Science and DevOps. Using BentoML, the shipping of models is made super easy such that it is easy to test, deploy and integrate with wide range of cloud providers.

BentoML model serving can be used once there is a trained ML model. Basically deploying using BentoML consists of two steps: `service` and `package`.

### Service

The first step is to create a prediction service using BentoML. For our application of the following BentoML service is created.

```python
@bentoml.env(
  requirements_txt_file="./requirements.txt"
)
@bentoml.artifacts([TransformersModelArtifact("distilbertModel")])


class TransformerSentimentService(bentoml.BentoService):
  
    @bentoml.api(input=JsonInput(), batch=False)
    def predict(self, parsed_json):
        src_text = parsed_json.get("text")
        model = self.artifacts.distilbertModel.get("model")
        tokenizer = self.artifacts.distilbertModel.get("tokenizer")
        inputs = tokenizer(src_text, return_tensors="pt")
        input_id = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        with torch.no_grad():
          outputs = model(input_id, attention_mask)
          probs = F.softmax(outputs.logits, dim=1).numpy()[0]
        return self.create_dict(src_text, probs)

    def create_dict(self, text: str, probs: list) -> dict:
        d = defaultdict()
        d["input_text"] = text
        d["pos_label"] = "positive"
        d["pos_score"] = float(probs[1])
        d["neg_label"] = "negative"
        d["neg_score"] = float(probs[0])
        return d

```

`@bentoml.env` decorator is the API for defining the environment settings and dependencies of your prediction service. BentoML provides [different ways](https://docs.bentoml.org/en/0.13-lts/concepts.html#defining-service-environment) this can be done.

`@bentoml.artifacts` decorator is the API that allow users to specify the trained models required by a BentoService. BentoML automatically handles model serialization and deserialization when saving and loading a BentoService. There are different `Artifcat` classes depending on machine learning framework. All the popular ML [frameworks](https://docs.bentoml.org/en/0.13-lts/frameworks.html) are supported by BentoML.

Inside the service, multiple inference API can be defined. For each inference API, input type must be specified via a `InputAdapter` instance. This defines the expected input data type and data format. BentoML supports most input serving use cases such as `DataframeInput`, `TfTensorInput`, `ImageInput` and `JsonInput`. BentoML also provides  The output type will be infered automatically by BentoML at runtime based on the return value of the API function.

### Package

The second step is to package the BentoML service.

```python
ts = TransformerSentimentService()
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = DistilBertForSequenceClassification.from_pretrained(model_name)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
artifact = {"model": model, "tokenizer": tokenizer}
ts.pack("distilbertModel", artifact)
saved_path = ts.save()
```

Here a BentoService instance is bundled with the trained model using the [`pack()`](https://docs.bentoml.org/en/0.13-lts/api/bentoml.html#bentoml.BentoService.pack) method. This trained model is then accessible within the API function code via `self.artifacts.ARTIFACT_NAME` (in this case `self.artifacts.distilbertModel`).  BentoML automatically handles model serialization and deserialization when saving and loading a BentoService.

The BentoService instance is now ready to be used for inference.

## Run

### Locally

BentoML service will be packaged and ready for inference. The command below will generate a BentoML bundle. The BentoML bundle is a file directory that contains all the code, files and configs that are required to run this prediction service.

Create a conda environment with packages as mentioned in `requirements.txt` and run the following python commands in the environment.

```bash
python bento_test_model_packed.py
bentoml list -o wide # list all bentoml bundles 
```

> BentoML stores all packaged model files under the `~/bentoml/{service_name}/{service_version}` directory by default. The BentoML file format contains all the code, files, and configs required to  deploy the model for serving.

Test the packaged service

> This requires getting a saved path for BentoML bundle or using the command `bentoml get TransformerSentimentService:latest --print-location`

```bash
python bento_test_model_packed.py
```

or using CLI

```bash
bentoml run TransformerSentimentService:latest predict --input '{"text": "i like you"}'
```

### Rest API Model Serving

#### Flask

This creates a Flask app using the service.

```bash
bentoml serve TransformerSentimentService:latest # also includes option to run with ngrok --run-with-ngrok
```

Test using curl (replace the localhost port address with the one obtained from above)

```bash
curl -X POST "http://0.0.0.0:5000/predict" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you!\"}"
```

#### Gunicorn

This creates a gunicorn service for the application.

```bash
bentoml serve-gunicorn TransformerSentimentService:latest
```

Test using curl

```bash
curl -X POST "http://0.0.0.0:5000/predict" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you!\"}"
```



### Containerize model server with Docker

One common way of distributing this model API server for production deployment, is via Docker containers.

```bash
bentoml containerize TransformerSentimentService:latest -t sentiment-classifier:v1
```

Test the container

```bash
docker run -p 5000:5000 sentiment-classifier:v1 --workers=2
```

We are ready to deploy this containzeried application them as online API serving endpoints (or offline batch inference jobs) on any cloud platform.

## Deployment Options

If you are at a small team with limited engineering or DevOps resources, try out automated deployment with BentoML CLI, currently supporting AWS Lambda, AWS SageMaker, and Azure Functions:

- [AWS Lambda Deployment Guide](https://docs.bentoml.org/en/latest/deployment/aws_lambda.html)
- [AWS SageMaker Deployment Guide](https://docs.bentoml.org/en/latest/deployment/aws_sagemaker.html)
- [Azure Functions Deployment Guide](https://docs.bentoml.org/en/latest/deployment/azure_functions.html)

If the cloud platform you are working with is not on the list above,  try out these step-by-step guide on manually deploying BentoML packaged  model to cloud platforms:

- [AWS ECS Deployment](https://docs.bentoml.org/en/latest/deployment/aws_ecs.html)
- [Google Cloud Run Deployment](https://docs.bentoml.org/en/latest/deployment/google_cloud_run.html)
- [Azure container instance Deployment](https://docs.bentoml.org/en/latest/deployment/azure_container_instance.html)
- [Heroku Deployment](https://docs.bentoml.org/en/latest/deployment/heroku.html)

Lastly, if you have a DevOps or ML Engineering team who's operating a Kubernetes or OpenShift cluster, use the following guides as references for implementating your deployment strategy:

- [Kubernetes Deployment](https://docs.bentoml.org/en/latest/deployment/kubernetes.html)
- [Knative Deployment](https://docs.bentoml.org/en/latest/deployment/knative.html)
- [Kubeflow Deployment](https://docs.bentoml.org/en/latest/deployment/kubeflow.html)
- [KFServing Deployment](https://docs.bentoml.org/en/latest/deployment/kfserving.html)
- [Clipper.ai Deployment Guide](https://docs.bentoml.org/en/latest/deployment/clipper.html)
