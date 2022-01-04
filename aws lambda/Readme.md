# AWS Lambda

BentoML has great support for AWS Lambda. You can deploy, update and delete Lambda deployment with single command, and customize deployment to fit your needs with parameters such as `region`, `memory_size` and `timeout`.

Pre-requsities:

- An active AWS account configured on the machine with AWS CLI installed and configured
    - Install instruction: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html
    - Configure AWS account instruction: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
- AWS SAM CLI tool
    - Install instruction: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install

## Run

Deploying BentoML service to AWS Lambda

```bash
git clone git@github.com:bentoml/aws-lambda-deploy.git
cd aws-lambda-deploy
# create a conda env
pip install -r requirements.txt
```

Update the `lambda-config.json` configuration as required

```json
{
  "region": "us-east-1",
  "timeout": 60,
  "memory_size": 1024
}
```

Finally, create a lambda deployment

```bash
BENTO_BUNDLE_PATH=$(bentoml get TransformerSentimentService:latest --print-location -q)
python deploy.py $BENTO_BUNDLE_PATH sentiment-lambda-deployment lambda_config.json
```

Get information about deployment

```bash
python describe.py sentiment-lambda-deployment
```

Test the lambda application

```bash
curl -i -X POST "https://6p43vhnw7i.execute-api.us-east-1.amazonaws.com/Prod/predict" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you\"}"
```

Delete the lambda application (if required)

```bash
python delete.py sentiment-lambda-deployment
```

Update the existing lambda deployment with new image (if required)

```bash
python update.py <new Bento_bundle_path> <new Deployment_name> <Config_JSON>
```
