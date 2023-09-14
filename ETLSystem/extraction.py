import PyPDF2
import mlflow
import os
from docx import Document



ROOT_DIR = os.getcwd()
ROOT_DIR = os.path.dirname(ROOT_DIR) # This is to extract the patent directory from the ful path(ETLSystem)
DATA_DIR = os.path.join(ROOT_DIR , "AllData")


def extraction_cv(filepath):
    '''
        This function is use to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
            
            doc = Document(filepath)
            extracted_text = []
            for paragraph in doc.paragraphs:
                extracted_text.append(paragraph.text)

            return "\n".join(extracted_text)

    else :    
        with open(filepath, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                extracted_text = ""

                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    extracted_text += page_text

        return extracted_text;

if __name__=='__main__':
    filepath = os.path.join(DATA_DIR, 'RawData','Njinju.pdf')
    extracted_text = extraction_cv(filepath)

    print(extracted_text)
   # mlflow.log_text(extracted_text, "extracted_text.txt")

    #print("PyPDF2 Version:", mlflow.__version__)
