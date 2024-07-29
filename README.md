# qea_scripting
Scripting to pull quiz grades and survey responses from Canvas and save to a Dashboard
The dashboard generates figues in a jupyter notebook, and displays GPT-generated summaries about student feedback on assignments

## Requirements and Constants
Before you can use the dasboard, make sure you have all requirements installed and the correct tokens are set in `constants.py`. To install the requirements, run `pip install -r requirements.txt`. 
This repo uses both the Canvas API and Azure API. 

### Canvas
To get your Canvas API Token, follow the instructions here: https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89 
The course ID can be found by clicking on the course. The URL should look like "https://canvas.<institution>.edu/courses/###". The numbers at the end are the course ID that you should set COURSE_ID equal to. The API_URL should follow the same format, just replace <institution> with the name that appears in the Canvas URL above.

### Azure
Azure API tokens are resource specific. Sign into the Azure portal (https://portal.azure.com/#home) and select the resource you are using (it should be an Azure OpenAI resource). If you do not already have an existing resource, you can create one. 
Select "Keys and Endpoints" in the left sidebar under "Resource Management".
![image](https://github.com/user-attachments/assets/56a8afe4-1655-4ec2-a5a7-c608054a180f)
Set `AZURE_TOKEN` equal to either Key 1 or Key 2 (does not matter which) and `AZURE_ENDPOINT`equal to the endpoint.
Next, go to "Model Deployments" (right under Keys and Endpoints in the sidebare) and click "Manage Deployments". Set `AZURE_DEPLOYMENT_NAME` equal to the deployment you want to use to generate your assignment summaries. This is case sensitive. I recommend that you use a gpt-4o model. If you do not have a deployment, you can create a new deployment. Optionally, you can `AZURE_API_DEPLOYMENT` to the date under "Model version", but if this causes issues change it to the default version already in `constants.py`.
