import fitz  # PyMuPDF
from docx import Document
import spacy
import re
import utilities as util;
import os;

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

def redact_with_spacy(text):
    """
    Takes text and redacts "PERSON", "ORG", "GPE", "DATE" & EMAIL from it
    :param str text: text to be redacted
    :return: redacted text
    """
    doc = nlp(text)
    redacted_text = text

    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE", "DATE"]:
            # Redact entities like names, organizations, locations, and dates
            redacted_text = redacted_text.replace(ent.text, "REDACTED")

    # Redact email addresses using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b'
    redacted_text = re.sub(email_pattern, "REDACTED_EMAIL", redacted_text)

    return redacted_text

def redact_cv(cv_path):
    """
    Takes a path to a CV, reads its text and applies redaction the text
    :param str cv_path: path to cv document
    :return: null
    """
    file_type = util.get_file_type(cv_path)

    # Replace text using the redaction function
    if "PDF" in file_type:
        text = util.pdf_extractor(cv_path)
        redacted_text = redact_with_spacy(text)
        print(redacted_text)

    elif "Microsoft Word" in file_type:
        text = util.word_extractor(cv_path)
        redacted_text = redact_with_spacy(text)
        print(redacted_text)
    else:
        print(f"{cv_path} is not PDF or Microsoft Word document.")

def main():
    data_home_directory = util.get_data_directory_path()
    ROOT_DIR = os.getcwd()
    cv_directory = os.path.join(ROOT_DIR , "AllData", "RawData", "CVs")

    # List all files in the folder
    files = os.listdir(cv_directory)

    # Print the list of files
    for file in files:
        file = os.path.join(cv_directory,file)
        print("Redacting file: {file}")
        redact_cv(file)

if __name__ == "__main__":
    main()