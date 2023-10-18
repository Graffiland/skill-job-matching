import fitz  # PyMuPDF
from docx import Document
import spacy
import re
import utilities as util;
import os;

# Load the NLP model

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
        redacted_text = util.mask_personal_information_2(text)
        return redacted_text

    elif "Microsoft Word" in file_type:
        text = util.word_extractor(cv_path)
        redacted_text = util.mask_personal_information_2(text)
        return redacted_text
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
        print(f'Redacting file: {file} =====================================' )
        redacted_text = redact_cv(file)
        print(redacted_text)
        

if __name__ == "__main__":
    main()