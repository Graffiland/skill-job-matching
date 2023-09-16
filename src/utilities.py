import docx
import PyPDF2

def wordextractor(filepath):
    """
        function is used to extract data from a word document
    """
    doc = docx.Document(filepath) # Reading in the file using Document method
    extracted_text = [] # an array that would hold the extracted file
    for paragraph in doc.paragraphs:
        extracted_text.append(paragraph.text) # loop through each paragraph in the word doc and extracting the text.

    return "\n".join(extracted_text)

def pdfextractor(filepath):
    with open(filepath, 'rb') as pdf_file: # reading in the pdf file
                pdf_reader = PyPDF2.PdfReader(pdf_file) #using a pdfreader to read in the file as a pdf
                extracted_text = "" #empty string that holds the extracted data

                for page_num in range(len(pdf_reader.pages)): # loops that loop over each page of the pdf and extract text form it and add its to the empty string
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    extracted_text += page_text

    return extracted_text
