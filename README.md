# qea_scripting
Scripting to pull quiz grades and survey responses from Canvas and save to a Dashboard
The dashboard generates figues in a jupyter notebook, and displays GPT-generated summaries about student feedback on assignments

## Requirements and Constants
Before you can use the dasboard, make sure you have all requirements installed and the correct tokens are set in `constants.py`. To install the requirements, run `pip install -r requirements.txt`. 
This repo uses both the Canvas API and Azure API. Open up `constants.py` and set the constants as the following:

### Canvas
To get your Canvas API Token, follow the instructions here: \
https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89 \
Set CANVAS_API_TOKEN equal to the token.
The course ID can be found by clicking on the course. The URL should look like "https://canvas.[institution].edu/courses/###". The numbers at the end are the course ID that you should set COURSE_ID equal to. The CANVAS_API_URL should follow the same format, just replace [institution] with the name that appears in the Canvas URL above.

### Azure
Azure API tokens are resource specific. Sign into the Azure portal (https://portal.azure.com/#home) and select the resource you are using (it should be an Azure OpenAI resource). If you do not already have an existing resource, you can create one. \
Select "Keys and Endpoints" in the left sidebar under "Resource Management". \
![image](https://github.com/user-attachments/assets/56a8afe4-1655-4ec2-a5a7-c608054a180f) \
Set `AZURE_TOKEN` equal to either Key 1 or Key 2 (does not matter which) and `AZURE_ENDPOINT`equal to the endpoint.
Next, go to "Model Deployments" (right under Keys and Endpoints in the sidebare) and click "Manage Deployments". Set `AZURE_DEPLOYMENT_NAME` equal to the deployment you want to use to generate your assignment summaries. This is case sensitive. I recommend that you use a gpt-4o model. If you do not have a deployment, you can create a new deployment. Optionally, you can `AZURE_API_DEPLOYMENT` to the date under "Model version", but if this causes issues change it to the default version already in `constants.py`. \
\
You can rename the csv files in `constants.py` if you would like. `STUDENT_REPORT_CSV` contains Canvas information, while `GPT_OUTPUT_CSV` contains GPT-generated summaries. \

## Dashboard
Now that all your tokens and constants are set, you can use the dashboard. This is the main way to interact with this software. Open up `dashboard.ipynb` and follow the instruction within to generate figures on student and assignment data

## Further Development
The following sections should make it easier to continue further work on this project.

### File Structure & Summary
- `get_quiz_respones.py` gets all the information from Canvas and saves it to multiple csvs and txt files
- `process_quiz_reports.py` takes those csvs and consolidates the information used in the dashboard. It also cleans up the directory by deleting all the csvs `get_quiz_responses.py` generates
- `summarize.py` uses the txt files created by `get_quiz_responses` to send survey responses to Azure OpenAI and automatically generate summaries. It saves these responses to a csv and deletes the txt files
- `get_all_reports.py` runs `get_quiz_responses.py`, `process_quiz_reports.py`, and `summarize.py` in one function
- `create_figures.py` contains all the functions used to generate the graphs in `dashboard.ipynb`
- `dashboard.ipynb` is the main dashboard users interact with. It calls upon the other functions/files to generate dataframes and create figures
- `constants.py` contains all the constans used in this repo. Most importantly, it contains the API tokens for Canvas and Azure. You should NEVER push these tokens to Github
- `promp.txt` contains the prompt that is being sent to OpenAI to generate summaries. The responses to student surveys are added to the end of prompt when the prompt is being sent to OpenAI. Prompting should be improved as more student data becomes available.
- `requirement.txt` is a list of all the dependencies that need to be installed to run this software. It is automatically created by running `pipreqs` in the directory.

### Next Steps
There are several improvements that can be made to this project. In no particular order, some are:
- Make it so you can pull one homework from Canvas at a time. Currently, the program will get all reports and consolidate them, which can take a lot of time, espeically with many students and assignments. Requests to the Canvas API should should append to `STUDENT_REPORT_CSV` or overwrite pre-existing entries (entries with the same student and assignment)
- Superimpose averages plot onto random students plot (`assignment_vs_time` and `assignment_vs_score` in `create_figures.py`)
- Make the sample of students in `assignment_vs_time` and `assignment_vs_score` the same
- Change the filtering done in `process_reports.py` - right now it saves certain columns based on their column index. All surveys should be structured the same, but to avoid errors, it would be better to do this filtering by key word. For example, "detail any concepts or technical content you are still confused by" appears in all the questions we want to look at student responses for. Column names should also be renamed to something more concise
- Generate multiple summaries based on student understanding of material. For example, filter it so you only get a summary about what students are struggling with for students that indicate they are still struggling with the material
- Test and improve GPT prompting with real data