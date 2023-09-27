from extraction import extracted_text
import re

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




