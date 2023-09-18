import os
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain

def getfilepaths():
    """
    Function to get file paths for Excel file and API key file.
    """
    ROOT_DIR = os.getcwd()
    ROOT_DIR = os.path.dirname(ROOT_DIR)  # Extract the parent directory from the full path (ETLSystem)
    DATA_DIR = os.path.join(ROOT_DIR, "AllData", "RawData")

    # the file paths
    excelpath = os.path.join(DATA_DIR, "Surveys.xlsx")
    apipath = os.path.join(DATA_DIR, "api.txt")

    return excelpath, apipath

def extract_surveydata(excelpath, apipath, schema):
    # Read the API key from a file and set it as an environment variable
    with open(apipath, 'r') as file:
        api_key = file.read().strip()
        os.environ['OPENAI_API_KEY'] = api_key

    data = pd.read_excel(excelpath)
    
    # Initializing empty string to store the text
    text = ""

    # Iterate through the rows of the DataFrame and convert to text
    for index, row in data.iterrows():
        # Initialize a sentence for each row
        sentence = ""

        # Iterate through the columns and add column values to the sentence
        for column_value in row.iloc[1:]:  # Skip the first column ('id')
            sentence += str(column_value) + " "

        # Adding  newline character at the end of the sentence
        sentence += "\n"
        text += sentence

    # Initialize ChatOpenAI with the specified model and temperature.
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    # Create an extraction chain based on the provided schema
    chain = create_extraction_chain(schema, llm)

    # Run the chain on the generated text
    result = chain.run(text)

    return result

# Get file paths using the getfilepaths function
excelpath, apipath = getfilepaths()

# Define your schema based on the data
data = pd.read_excel(excelpath)  # Define data here

# Define your schema
schema = {
    "properties": {
        column: {
            "type": "string" if data[column].dtype == 'object' else "integer"
        } for column in data.columns
    },
    "required": [],  # All columns are required
}

# Calling function to extract data and run the chain
result = extract_surveydata(excelpath, apipath, schema)

# Print the extracted result
print(result)
