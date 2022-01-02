# kpmg-challenge
Repo for KPMG technical round challenge

Infrastructure:
An HTTP API Gateway integrated with a Lambda in backend with necessary roles & permissions
Lambda's function is to return available vaccination slot details for a given pincode & date, via an API.

The API URL is based on API Gateway's ID which is a random string assigned to it during its creation which means that it can change with every deployment.
For this reason, the URL is returned as an Output in its Cloudformation template and is also returned by Git Actions : Click on Actions tab in this repository, click on the latest successful workflow and then click on 'deploy' job to get details. Finally , click on 'API Link' step to get the link.

Latest Link: https://i9lbkbzh7d.execute-api.ap-south-1.amazonaws.com/getJabSlot?pincode=122002&date=01-01-2022

Automation:
Git Actions is configured to automatically deploy above infrastructure in AWS on any changes pushed to [master] branch
There is also an option to manually trigger deployment, if required

The file that enables automation is placed the root level at .github path : .github/workflows/deployCFT.yml
This file is also placed in 'automation' folder only for reference: automation/deployCFT.yml

Coding:
Lambda's function is a Python code that parses the query strings in the API that triggered it, and checks availability of vaccination slots.
If slots are available, it returns the details of the vaccination center and timings as follow:

Centre                         From Time                      To Time                        Vaccine                       

Fortis Memorial Resarch Inst   14:00:00                       18:00:00                       COVISHIELD                    
Fortis Memorial Resarch Inst   14:00:00                       18:00:00                       COVISHIELD                    
Fortis Memorial Resarch Inst   09:00:00                       13:00:00                       COVAXIN                       
Fortis Memorial Resarch Inst   09:00:00                       13:00:00                       COVAXIN  

Error handling is done to notify in case of missing parameters (date/pincode) or if there are no slots available for the given date / pincode.
Although the code in present in the CFT at 'infrastructure/VaccineSlotFinder.yml' , it can also be found in a separate file at 'coding/VaccineSlotFinder.py' for reference.



