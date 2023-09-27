from extraction import extracted_text
import re
import spacy

def mask_data(text):
    # Define a list of sensitive information patterns to match
    patterns = [
                                 # Matches names with the assumption of an uppercase letter followed by lowercase letters
        r'\+32\s\d+\s\d+\s\d+',  # Matches Belgian phone numbers with the assumption of "+32 <digits> <digits> <digits>"
        r'\S+@\S+'  # Matches email addresses
    ]

    # Define a function to replace matches with a mask
    def replace(match):
        return '*' * len(match.group(0))

    # Apply the masking to the input text
    for pattern in patterns:
        text = re.sub(pattern, replace, text)

    return text

data = mask_data(extracted_text)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define a function to extract names from a string
def extract_names(input_string):
    # Process the input string with spaCy
    doc = nlp(input_string)

    # Extract names (PERSON entities) from the processed text
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    return names

names = extract_names(data)

print(names)



