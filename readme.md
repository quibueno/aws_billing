# **AWS Cost Reporting Tool**
This Python script you are about to run is designed to calculate costs on AWS based on the cost distribution among different accounts and groups.
## **Prerequisites**

- Python 3.6 or higher.
- Packages boto3, pandas, and configparser, which can be installed using the command:

***pip install boto3 pandas configparser***

- Access to AWS with the necessary permissions to access cost information.
## **User Guide**

### **1. AWS Credentials**
You need to provide your AWS credentials in the credentials.ini file. This file should have the following structure:

***[default]***

***aws\_access\_key\_id = YOUR\_ACCESS\_KEY***

***aws\_secret\_access\_key = YOUR\_SECRET\_KEY***

Replace YOUR\_ACCESS\_KEY and YOUR\_SECRET\_KEY with your own AWS credentials.
### **2. Group File (groups.json)**
This file defines the groups of AWS accounts whose costs you want to sum up. It should have the following format:

***{***

`   `***"GroupName1": ["AccountID1", "AccountID2"],***

`   `***"GroupName2": ["AccountID3"]***

***}***

The group names are used to name the rows in the output spreadsheet. The account IDs are the AWS account IDs whose costs you want to sum up for each group.





### **3. Weights File (weights.json)**
This file defines how the costs of shared accounts should be divided among the projects. It should have the following format:

***{***

`   `***"SharedAccountID": {***

`       `***"ProjectName1": 0.5,***

`       `***"ProjectName2": 0.3,***

`       `***"ProjectName3": 0.2***

`   `***}***

***}***

The shared account ID is the ID of the AWS account whose costs are being shared. The project names are the names of the projects that are sharing the costs, and the numbers are the weights that define how the costs are divided. The weights for a shared account must add up to 1.
### **4. Running the Script**
After preparing the above files, you can run the script with the following command in the terminal:

***python your\_script\_name.py***
### **5. Output**
The script generates an Excel file named grouped\_costs.xlsx that contains the total costs for each AWS account group, as well as the fractioned costs for each project based on the weights defined in the weights.json file.

## **Additional Notes**

This script collects costs from the last complete month. For example, if you run the script in May, it will collect costs from April. Please adjust the code if you need a different time period.
## **Contact**

For further queries, you can reach out to <your-email@domain.com>

Please replace "<your-email@domain.com>" with your actual email address.

