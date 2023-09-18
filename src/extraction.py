import mlflow
import os
import utilities

DATA_DIR = utilities.getfilepath()

def extraction_cv(filepath):
    '''
        This function is use to extract data from the csv or word document
    '''
    if filepath.lower().endswith('.docx'):
        return utilities.wordextractor(filepath) # function use to extract data from a word doc
    else :    
        return utilities.pdfextractor(filepath) # function use to extract data from a pdf file
    



if __name__=='__main__':
    filepath = os.path.join(DATA_DIR, 'RawData','Njinju.pdf')
    extracted_text = extraction_cv(filepath)

    print(extracted_text)
    #mlflow.log_text(extracted_text, "extracted_text.txt")
    #print("PyPDF2 Version:", mlflow.__version__)
