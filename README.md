# Introduction
Skill job matching tool uses large large model such as chatGPT at its core to match skills with trending professional jobs in high demand in the job market.


Project Name :  Skill Job Matching Tool.


-- Project Status: [Active ]


# Project Intro/Objective:
- It's an automated AI application desined to empower professionl career coaches. 
- It provides accurate and up-to-date career advicce to client. 
- we aimed at combining inputs and contextual information wit the aims for enhancing the career decision-making process by matching skills to high-demand jpb roles.

# Architecture - PART 1 (steps on Ingestion and Preparation pipeline)
Using Azure
- Getting all our data from different source, performing an exploratory analysis on them to understand trend between the variables in our data set.
- The next step is either building a pipeline in Azure or orchestrating it in Gitlab if need be. 
- In Azure we will put all our data set gotten from our various data source in a datalake. 
- We also intend builing an ETL system using databricks using a data factory as a pipeline guiding the flow of data in this pipeline. 
- Then finally pushing the complete transform file in a Datawarehouse.

Using GITLAB
- we intend to put all our data on our local pc, creating a folder all source. 
- Then we create 3 files (Extra.py , Transfrom.py , Load.py) for our pipeline.
- Then we build a pipeline in Gitlab uing YMAL to control and monitor the flow of data within the system.
- Then we would create SQL database using python to hold our final databases


# Partner:

- Graffiland


# Methods Used
- Machine Learning
- Data Visualization
- ETL pipeline
- AI 
- Draw.io
- Pycharm
- YMAL


# Technologies:
  - Python
  - Pandas, jupyter
  - Streamlit web application

# Project Description


# Steps to Set-up and run this project 
1. install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
2. run `conda env create --file environment.yml -n skill-job-matching-4`
3. Download spacy's en_core_web_sm `python -m spacy download en_core_web_sm`
4. Install `python-magic` dependencies according to your OS using the instructions below:

  - Debian/Ubuntu
     
  `sudo apt-get install libmagic1`
  
  - Windows
  
  You'll need DLLs for libmagic. @julian-r maintains a pypi package with the DLLs, you can fetch it with:

   `pip install python-magic-bin`
   
  - OSX
  
  When using Homebrew: `brew install libmagic`
  
  When using macports: `port install file`
