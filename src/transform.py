from extraction import extracted_text
import re
import utilities


def mask_data(text):
    # Define a list of sensitive information patterns to match
    patterns = [
        # Matches names with the assumption of an uppercase letter followed by lowercase letters
        # Matches Belgian phone numbers with the assumption of "+32 <digits> <digits> <digits>"
        r'\+32\s\d+\s\d+\s\d+',
        r'\S+@\S+',  # Matches email addresses
        r'\b(?:city1|city2|city3)\b'
    ]

    # Define a function to replace matches with a mask and count the replacements
    def replace_and_count(match):
        nonlocal mask_count
        mask_count += 1
        return '*' * len(match.group(0))

    mask_count = 0  # Initialize the mask count

    # Apply the masking to the input text
    for pattern in patterns:
        text = re.sub(pattern, replace_and_count, text)

    return text, mask_count


data, count = mask_data(extracted_text)

print(utilities.mask_personal_information((extracted_text)))

# print("The number of mask text is :", count)
