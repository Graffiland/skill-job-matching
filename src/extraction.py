import mlflow
import os
import pandas as pd
import utilities

DATA_DIR = utilities.getfilepath()


def extraction_cv(filepath):
    '''
        This function is used to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
        # function use to extract data from a word doc
        return utilities.wordextractor(filepath)
    else:
        # function use to extract data from a pdf file
        return utilities.pdfextractor(filepath)


def extraction_survey(surveypath):
    '''
        This function is used to extract data from the survey
   '''
    result = utilities.extract_surveydata(surveypath)

    return result


cvname = input("Enter your name with extension (.pdf) :")

filepath = os.path.join(DATA_DIR, 'RawData', 'CVs', cvname)
surveypath = os.path.join(DATA_DIR, 'RawData', 'Surveys.xlsx')
extracted_survey = extraction_survey(surveypath)
extracted_text = extraction_cv(filepath)
# mlflow.log_text(extracted_text, "extracted_text.txt")

# print(extracted_survey)
# mlflow.log_text(extracted_survey, "extracted_survey.txt")
# print("PyPDF2 Version:", mlflow.__version__)
