import openai
import utilities
from transform import email
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variabel from .evn.


# enrionment variables
openai.api_key = os.getenv("API_KEY")


# Getting Data From Database
email_to_search = email

masked_cv_result, masked_survey_result = utilities.get_masked_cv_and_survey(
    email_to_search)


# Geting data from prompts
DATA_DIR = utilities.get_data_directory_path()

promptpath = os.path.join(DATA_DIR, 'RawData', 'prompts', 'prompt.docx')

# extracting data from prompt documents
extractedwordtext = utilities.word_extractor(promptpath)

input = f'''
Below you will find a list of prompts questions for both a masked_cv and masked_survey , still provide responds if no cv was provided and indicate that no cv was provided: 

{extractedwordtext}

Here is the masked survey : 

{masked_survey_result}

Here is the masked cv : 

{masked_cv_result}

please can you provide detail response for this prompts.

'''


input_messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Bellow you will find a list of prompts questions..."},
    {"role": "user", "content": f"{input}"}
    # Add more user or assistant messages as needed
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=input_messages,
    temperature=0.7
)


# Parse the JSON string
response_dict = response

# Access and print the content field
print(response_dict['choices'][0]['message']['content'])
