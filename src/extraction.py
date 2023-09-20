import mlflow
import os
import pandas as pd
import utilities

DATA_DIR = utilities.getfilepath()

def extraction_cv(filepath):
    '''
        This function is use to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
        return utilities.wordextractor(filepath) # function use to extract data from a word doc
    else :    
        return utilities.pdfextractor(filepath) # function use to extract data from a pdf file
    
def extraction_survey(surveypath):
   '''
        This function is use to extract data from the survey
   '''
   result= utilities.extract_surveydata(surveypath)

   return result

if __name__=='__main__':
    filepath = os.path.join(DATA_DIR, 'RawData','Njinju.pdf')
    surveypath = os.path.join(DATA_DIR,'RawData','Surveys.xlsx')
    extracted_survey = extraction_survey(surveypath)
    extracted_text = extraction_cv(filepath)

    #print(extracted_text)
    #mlflow.log_text(extracted_text, "extracted_text.txt")

    print(extracted_survey)
    mlflow.log_text(extracted_survey, "extracted_survey.txt")
    #print("PyPDF2 Version:", mlflow.__version__)

