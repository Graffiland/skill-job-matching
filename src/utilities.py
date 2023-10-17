import docx
import PyPDF2
import os
import pandas as pd
import json
import csv
import re
import spacy
import magic


def get_file_type(file_path):
    mime = magic.Magic()
    file_type = mime.from_file(file_path)
    return file_type

def get_data_directory_path():
    """
        function is used to get path
    """
    ROOT_DIR = os.getcwd()
    ROOT_DIR = os.path.dirname(ROOT_DIR) # This is to extract the patent directory from the ful path(ETLSystem)
    DATA_DIR = os.path.join(ROOT_DIR , "AllData")

    return DATA_DIR


def word_extractor(filepath):
    """
        function is used to extract data from a word document
    """
    doc = docx.Document(filepath) # Reading in the file using Document method
    extracted_text = [] # an array that would hold the extracted file
    for paragraph in doc.paragraphs:
        extracted_text.append(paragraph.text) # loop through each paragraph in the word doc and extracting the text.

    return "\n".join(extracted_text)

def pdf_extractor(filepath):
    """
        function is used to extract data from a word pdf document
    """
    with open(filepath, 'rb') as pdf_file: # reading in the pdf file
                pdf_reader = PyPDF2.PdfReader(pdf_file) #using a pdfreader to read in the file as a pdf
                extracted_text = "" #empty string that holds the extracted data

                for page_num in range(len(pdf_reader.pages)): # loops that loop over each page of the pdf and extract text form it and add its to the empty string
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    extracted_text += page_text

    return extracted_text


def remove_non_breaking_spaces(text):
    if isinstance(text, str):
        # Define a regular expression pattern to match various representations of non-breaking spaces
        pattern = re.compile(r'[\u00a0\xa0\s]+')
        return re.sub(pattern, ' ', text)
    return text

def extract_survey_data(surveypath):
    
    sv = pd.read_excel(surveypath)

    # Clean up the text data in columns by removing non-breaking space characters
    sv = sv.applymap(remove_non_breaking_spaces)

    # Clean up column names (headers)
    sv.columns = [str(x).replace("\u00a0", " ") for x in sv.columns]

    csv_path = "temp.csv"
    sv.to_csv(csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

    sv_csv = pd.read_csv(csv_path)

    json_data = sv_csv.to_json(orient="records", default_handler=str)
    
    #print the JSON data
    json_data = json.dumps(json.loads(json_data), indent=4)

    # Clean up the temporary CSV file
    os.remove(csv_path)

    return json_data

def mask_personal_information(text):
    # Load the English language model for spaCy
    nlp = spacy.load("en_core_web_sm")

    # Process the input text using spaCy
    doc = nlp(text)

    # Define categories of personal information
    personal_info_categories = [
        "PERSON",  # Name
        "PHONE",  # Phone number
        "NORP",  # Nationalities, religious, or political groups
        "ORG"  # Organizations (e.g., trade unions)
    ]

    # Mask out identified personal information
    masked_text = text
    for ent in doc.ents:
        if ent.label_ in personal_info_categories:
            masked_text = masked_text.replace(ent.text, '*' * len(ent.text))

    return masked_text

def mask_accuracy():
    """
        function is to check accuracy of masked data
    """
