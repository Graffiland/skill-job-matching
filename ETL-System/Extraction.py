import PyPDF2
import mlflow
import os
ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR , "AllData")


def extraction(filepath):
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
    extracted_text = extraction(filepath)

    print(extracted_text)
    mlflow.log_text(extracted_text, "extracted_text.txt")

    #print("PyPDF2 Version:", mlflow.__version__)
