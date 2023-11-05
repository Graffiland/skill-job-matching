import os
import utilities

DATA_DIR = utilities.get_data_directory_path()

cv_directory = os.path.join(DATA_DIR, 'RawData', 'CVs')
# List all files in the CV directory
cv_files = os.listdir(cv_directory)
# Gets the only file from the cv
# nameofcv = cv_files[0]


def extraction_cv(filepath):
    '''
        This function is used to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
        # function use to extract data from a word doc
        return utilities.word_extractor(filepath)
    elif filepath.lower().endswith('.docx'):
        # function use to extract data from a pdf file
        return utilities.pdf_extractor(filepath)
    else:
        print("the file does not exist")


def extraction_survey(surveypath):
    '''
        This function is used to extract data from the survey
    '''
    result = utilities.extract_survey_data(surveypath)

    return result


# Set a default value for cv_files (empty list if not provided)
cv_files = cv_files if cv_files else []

# Always access the first element (or None if the list is empty)
filepath = os.path.join(cv_directory, cv_files[0]) if cv_files else None

# Survey filepath
surveypath = os.path.join(DATA_DIR, 'RawData', 'Surveys1.xlsx')

# OUTPUTS (extracted_text(string) and extracted_survey(JSON format))
extracted_survey = extraction_survey(surveypath)
extracted_text = extraction_cv(filepath) if filepath else None
