# qea_scripting
Scripting to pull quiz grades and survey responses from Canvas and save to a functional excel dashboard

Potential to use ChatGPT to automatically generate quiz questions and push those.

## USE
Run main.py to pull all the information you need from Canvas. This includes quiz scores and survey responses for all the homework surveys. 
When you open up the excel dashboard, you may encounter an error that says source data could not be found. To fix this, select the data tab along the top and select "Queries and Connections"
![image](https://github.com/user-attachments/assets/359f6b57-6295-42f0-ab63-147e15f70b31)


You should see Conslidated Reports to the right. Hovering over that opens up a window where you can select edit
![image](https://github.com/user-attachments/assets/f24f3d4b-1229-4d91-a6be-ee09a81bdfe3)


Finally, select the settings wheel next to Source and Browse for your local copy of Consolidated Reports
![image](https://github.com/user-attachments/assets/dba2ad4d-84f4-4d3a-b50b-21900a9bd617)


You should only have to do this once. After that, the Dashboard will refresh everytime you open it. You will have to run main.py to get the most recent quiz/survey responses left on Canvas.
