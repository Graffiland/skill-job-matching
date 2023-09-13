import PyPDF2
import mlflow


def extraction():
    with open('/AllData/RawData/Njinju.pdf', 'rb') as pdf_file:

        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            extracted_text += page_text

    pdf_file.close()

    return extracted_text;

extracted_text = extraction()

print(extracted_text)
mlflow.log_text(extracted_text, "extracted_text.txt")

#print("PyPDF2 Version:", mlflow.__version__)
