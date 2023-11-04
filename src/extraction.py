import os
import pandas as pd
import utilities

DATA_DIR = utilities.get_data_directory_path()

cv_directory = os.path.join(DATA_DIR, 'RawData', 'CVs')
# List all files in the CV directory
cv_files = os.listdir(cv_directory)
# Gets the only file from the cv
nameofcv = cv_files[0]


# CV filepath
filepath = os.path.join(cv_directory, nameofcv)
# survey filepath
surveypath = os.path.join(DATA_DIR, 'RawData', 'Surveys1.xlsx')


def extraction_cv(filepath):
    '''
        This function is used to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
        # function use to extract data from a word doc
        return utilities.word_extractor(filepath)
    else:
        # function use to extract data from a pdf file
        return utilities.pdf_extractor(filepath)


def extraction_survey(surveypath):
    '''
        This function is used to extract data from the survey
    '''
    result = utilities.extract_survey_data(surveypath)

    return result


# OUTPUTS (extracted_text(string) and extracted_survey(JSON format))
extracted_survey = extraction_survey(surveypath)
extracted_text = extraction_cv(filepath)
