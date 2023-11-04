import docx
import PyPDF2
import os
import pandas as pd
import json
import csv
import re
import spacy
import subprocess
import sqlite3

JOBS_SKILLS_CONFIG = None

# Download spaCy model if not already installed

# Load our model which would be use for masking of sensitive data using spacy library
nlp = spacy.load("en_core_web_sm")


# FUNCTIONS FOR EXTRACTION.PY

def get_data_directory_path():
    """
        function is used to get path
    """
    ROOT_DIR = os.getcwd()
    # This is to extract the patent directory from the ful path(ETLSystem)
    ROOT_DIR = os.path.dirname(ROOT_DIR)
    DATA_DIR = os.path.join(ROOT_DIR, "AllData")

    return DATA_DIR


def word_extractor(filepath):
    """
        function is used to extract data from a word document
    """
    doc = docx.Document(filepath)  # Reading in the file using Document method
    extracted_text = []  # an array that would hold the extracted file
    for paragraph in doc.paragraphs:
        # loop through each paragraph in the word doc and extracting the text.
        extracted_text.append(paragraph.text)

    return "\n".join(extracted_text)


def pdf_extractor(filepath):
    """
        function is used to extract data from a word pdf document
    """
    with open(filepath, 'rb') as pdf_file:  # reading in the pdf file
        # using a pdfreader to read in the file as a pdf
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""  # empty string that holds the extracted data

        # loops that loop over each page of the pdf and extract text form it and add its to the empty string
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            extracted_text += page_text

    return extracted_text


def remove_non_breaking_spaces(text):
    """
        This function removes non breaking spaces in our json
    """
    if isinstance(text, str):
        # Define a regular expression pattern to match various representations of non-breaking spaces
        pattern = re.compile(r'[\u00a0\xa0\s]+')
        return re.sub(pattern, ' ', text)
    return text


def extract_survey_data(surveypath):
    """
        Extracts data from the survey and returns it in a JSON Format
    """

    sv = pd.read_excel(surveypath)

    columns_to_delete = ["Start time", "Completion time",
                         "Email", "Name", "Last modified time"]

    sv = sv.drop(columns=columns_to_delete)

    # Clean up the text data in columns by removing non-breaking space characters
    sv = sv.applymap(remove_non_breaking_spaces)

    # Clean up column names (headers)
    sv.columns = [str(x).replace("\u00a0", " ") for x in sv.columns]

    csv_path = "temp.csv"
    sv.to_csv(csv_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

    sv_csv = pd.read_csv(csv_path)

    json_data = sv_csv.to_json(orient="records", default_handler=str)

    # print the JSON data
    json_data = json.dumps(json.loads(json_data), indent=4)

    # Clean up the temporary CSV file
    os.remove(csv_path)

    return json_data


# FUCTIONS USED IN TRANSFORM.PY

def mask_personal_information_2(text):
    """
    Takes text and redacts "PERSON", "GPE", "DATE", "PHONE", "NORP", "ORG","EMAIL", "LOC", "FAC" from it
    :param str text: text to be redacted
    :return: redacted text
    """
    doc = nlp(text)
    redacted_text = text

    # Redact email addresses using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b'
    redacted_text = re.sub(email_pattern, "*****", redacted_text)

    # Define a regular expression pattern to match both common and additional phone number formats
    phone_number_pattern = r'\+?\d{0,4}\s?\(?\d+\)?\s?\d+\s?\d+\s?\d+|\(\d{3}\)\s?\d{3}-\d{4}'
    redacted_text = re.sub(phone_number_pattern,
                           "*****", redacted_text)

    # Define a regular expression pattern to match both common and additional phone number formats
    name_pattern = r'\b[A-Z][A-Za-z]* [A-Z][A-Za-z]* [A-Z][A-Za-z]*\b'
    redacted_text = re.sub(
        name_pattern, "*****", redacted_text)

    return redacted_text


def create_mapping(cv_data_string, survey_data):
    """
        This function is use to map survey and cv using their email and returns a dictionary of survey and cv
    """
    cv_email_matches = re.findall(r'\S+@\S+', cv_data_string)
    cv_emails = [email.strip() for email in cv_email_matches]

    # Create a mapping dictionary based on email addresses
    mapping = {}

    for survey_entry in survey_data:
        email = survey_entry.get("Email Address")
        if email in cv_emails:
            cv_text = cv_data_string
            mapping[email] = {
                "CV Text": cv_text,
                "Survey Entry": survey_entry
            }

    return mapping


def mask(mapping):
    if len(mapping) == 0:
        print('check CV OR Survey data')
    else:
        for email, data in mapping.items():
            mask_cv = data["CV Text"]
            mask_survey = data["Survey Entry"]
            datae = email
        return mask_cv, mask_survey, datae


def mask_sensitive_data(extracted_surveys):
    """
        This function is use to mask survey data and returns masked survey in JSON format.
    """
    # Regular expression pattern to match email addresses
    email_pattern = r'\b[\w.-]+@[a-zA-Z.-]+\b'

    # Regular expression pattern to match gender-related words
    gender_pattern = r'\b(?:male|female|man|woman|boy|girl)\b'

    # Regular expression pattern to match ethnic region-related words
    ethnic_region_pattern = r'\b(?:race|ethnicity|origin|ethnic background)\b'

    # Religious pattern
    religious_pattern = r'\b(?:religion|religious beliefs|faith)\b'

    # Genetic pattern
    genetic_pattern = r'\b(?:genetic information|genetic data)\b'

    # Biometric pattern
    biometric_pattern = r'\b(?:biometric data|fingerprint|retina scan|iris scan|facial recognition)\b'

    # Health-related pattern
    health_pattern = r'\b(?:health information|medical data|medical history|disease|condition|treatment|medication)\b'

    # to mask email addresses
    def mask_email(match):
        return '***@***.com'

    # to mask names (assuming a name is two or more words)
    def mask_name(match):
        return '***'

    # Parse the JSON string into a Python object (list of dictionaries)
    # extracted_surveys = list(extracted_surveys)
    extracted_surveys = json.loads(extracted_surveys)

    # Extract names from "First/Given names" and "Last/Family names"
    names_to_mask = set()
    for item in extracted_surveys:
        first_name = item.get("First/Given names", "")
        last_name = item.get("Last/Family names", "")
        if first_name:
            names_to_mask.add(first_name)
        if last_name:
            names_to_mask.add(last_name)

    masked_data = []
    for item in extracted_surveys:
        masked_item = {}
        for key, value in item.items():
            if key == "Email Address":
                value = re.sub(email_pattern, mask_email, value)
            elif key in ["First/Given names", "Last/Family names"]:
                if value:
                    masked_name = "***"
                    masked_item[key] = masked_name
                else:
                    masked_item[key] = None
            else:
                # Mask names using regular expressions and country/continent names using spaCy
                if isinstance(value, str):
                    for name in names_to_mask:
                        value = value.replace(name, '***')
                    doc = nlp(value)
                    for ent in doc.ents:
                        # Filter country and continent names
                        if ent.label_ in ("GPE", "LOC"):
                            value = value.replace(ent.text, '***')
                    value = re.sub(gender_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(ethnic_region_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(religious_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(genetic_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(biometric_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(health_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    masked_item[key] = value
                else:
                    masked_item[key] = value
        masked_data.append(masked_item)

    return masked_data


# FUNCTIONS FROM LOAD.py

def create_and_insert_skilljob_table(cvsurveyemail, masked_cv, masked_survey):
    # Gets connection and cursor from utilities
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    try:
        # Drop the table if it exists (optional)
        cursor.execute('''DROP TABLE IF EXISTS skilljob''')

        # Create the skilljob table with the specified columns
        cursor.execute('''CREATE TABLE skilljob (
            Email_Address TEXT CHECK(LENGTH(Email_Address) <= 1000000000),
            Masked_CV TEXT CHECK(LENGTH(Masked_CV) <= 1000000000),
            Masked_Survey JSON CHECK(LENGTH(Masked_Survey) <= 10000000000),
            Response TEXT CHECK(LENGTH(Response) <= 1000000000)
        )''')

        # Insert data into the table
        insert_data = [
            (cvsurveyemail, masked_cv, json.dumps(masked_survey)),
            # Add more rows as needed
        ]

        cursor.executemany(
            "INSERT INTO skilljob (Email_Address, Masked_CV, Masked_Survey) VALUES (?,?,?)", insert_data)

        # Commit the changes
        conn.commit()

        # Retrieve and display data
        cursor.execute("SELECT * FROM skilljob")
        rows = cursor.fetchall()

        # Print the column names
        column_names = [description[0] for description in cursor.description]
        print(column_names)

        # Print data in each column for each row
        for row in rows:
            print(row)

    finally:
        # Close the connection in a finally block to ensure it happens even if an exception is raised
        conn.close()
