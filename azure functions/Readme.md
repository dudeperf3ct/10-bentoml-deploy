# Azure Functions

Azure Functions similar to AWS Lambda is event driven, serverless execution model. BentoML supports effortless deployment on Azure Functions.

Pre-requsities:

- An active Azure account configured on the machine with Azure CLI installed and configured
    - Install instruction:  https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
    - Configure Azure account instruction: https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install

## Run

**Deploying BentoML service to Azure Functions**

```bash
git clone https://github.com/bentoml/azure-functions-deploy
cd azure-functions-deploy
# create a conda env
pip install -r requirements.txt
```

Update the `azure_config.json` configuration as required (for in-detail information see section `Configuration Details` at the end)

```json
{
  "location": "< replace with resource location that is setup in azure>",
  "min_instances": 1,
  "max_burst": 20,
  "function_sku": "B1",
  "function_auth_level": "anonymous",
  "acr_sku": "Standard"
}
```

Finally, **create** a Azure Functions deployment

```bash
BENTO_BUNDLE_PATH=$(bentoml get TransformerSentimentService:latest --print-location -q)
python deploy.py $BENTO_BUNDLE_PATH sentiment-azfunc-deployment azure_config.json
```

**Get information** about deployment

```bash
python describe.py sentiment-azfunc-deployment
```

**Test** the Azure Functions application

```bash
curk -i -X POST "<deployed-function-here>/predict" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"text\":\"i like you\"}"
```

**Delete** the Azure Functions application (if required)

```bash
python delete.py sentiment-azfunc-deployment
```

**Update** the existing Azure Functions deployment with new image (if required)

```bash
python update.py <new Bento_bundle_path> <new Deployment_name> <Config_JSON>
```

### Configuration Details

`location`: Azure Function location. Use az account list-locations to find list of Azure locations.

`min_instances`: The number of workers for the deployed app. Default is 1

`max_burst`: The maximum number of workers for the deployed app Default is 20

`function_auth_level`: The authentication level for  the function. Allowed values: anonymous, function, admin. Default is  anonymous. See the link for more information, https://docs.microsoft.com/en-us/java/api/com.microsoft.azure.functions.annotation.httptrigger.authlevel?view=azure-java-stable

`premium_plan_sku`: The app service plan SKU. Allowed values: EP1, EP2, EP3. Default is EP1. See the link for more information, https://docs.microsoft.com/en-us/azure/azure-functions/functions-premium-plan

`acr_sku`: The SKU for Azure Container Registry. Allowed values: Basic, Classic, Premium, Standard. Default is Standard
