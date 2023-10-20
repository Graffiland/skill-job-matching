import fitz  # PyMuPDF
from docx import Document
import spacy
import re
<<<<<<< HEAD
import utilities as util
import os
from extraction import extracted_text

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
=======
import utilities as util;
import os; 
from SkillsExtractor import SkillsExtractor

# Load the NLP model
>>>>>>> 5c7036598e39c2165b0b877d592a28797cce06b2


def redact_cv(text):
    """
    Takes a path to a CV, reads its text and applies redaction the text
    :param str cv_path: path to cv document
    :return: null
    """
    # file_type = util.get_file_type(cv_path)

    # Replace text using the redaction function
<<<<<<< HEAD
    # if "PDF" in file_type:
    # text = util.pdf_extractor(cv_path)
    redacted_text = redact_with_spacy(text)
    print(redacted_text)

    # elif "Microsoft Word" in file_type:
    #     text = util.word_extractor(cv_path)
    #     redacted_text = redact_with_spacy(text)
    #     print(redacted_text)
    # else:
    #     print(f"{cv_path} is not PDF or Microsoft Word document.")


def main():
    redact_cv(extracted_text)
    # data_home_directory = util.get_data_directory_path()
    # ROOT_DIR = os.getcwd()
    # cv_directory = os.path.join(ROOT_DIR, "AllData", "RawData", "CVs")
=======
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
    
    ROOT_DIR = os.getcwd()
    cv_directory = os.path.join(ROOT_DIR , "AllData", "RawData", "CVs")
    jobs_skills_config_path = os.path.join(ROOT_DIR , "AllData", "SkilsConfig", "jobs_skills_config.yaml")
 

>>>>>>> 5c7036598e39c2165b0b877d592a28797cce06b2

    # # List all files in the folder
    # files = os.listdir(cv_directory)

    # # Print the list of files
    # for file in files:
    #     file = os.path.join(cv_directory, file)
    #     print("Redacting file: {file}")
    #     redact_cv(file)

<<<<<<< HEAD
=======
    # Print the list of files
    for file in files:
        file = os.path.join(cv_directory,file)
        print(f'Redacting file: {file} =====================================' )
        redacted_text = redact_cv(file)
        print(redacted_text)
        skills_Extractor =  SkillsExtractor(jobs_skills_config_path)
        skills_list = skills_Extractor.extract_skills(redacted_text)

        union_skill_set = set()
        for skill_set_name, skill_set in skills_list:
            if skill_set:
                union_skill_set.update(skill_set)
                print(f"Entries in category {skill_set_name} \n %%%%%%%%%%%%%%%%%")
                print(skill_set)
            else:
                print(f"There are no entries found in category {skill_set_name} \n %%%%%%%%%%%%%%%%%")
        
        print(f"Total number of skills found is {len(union_skill_set)} and the skills are: ***************************************************** \n {union_skill_set}")
>>>>>>> 5c7036598e39c2165b0b877d592a28797cce06b2

if __name__ == "__main__":
    main()
