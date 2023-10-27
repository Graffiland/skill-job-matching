from extraction import extracted_survey
import re
import json
import spacy
from extraction import extracted_text
import spacy
import re
import utilities

nlp = spacy.load("en_core_web_sm")

extracted_survey = json.loads(extracted_survey)
# print(f' second : {type(extracted_survey)}')
dict_cvsurvey = utilities.create_mapping(extracted_text, extracted_survey)

extracted_text, extracted_surveys = utilities.mask(dict_cvsurvey)
extracted_sur = [extracted_surveys]
extracted_surveys = json.dumps(extracted_sur)
# print(extracted_surveys)
# print(f' first : {type(extracted_surveys)}')


def mask_sensitive_data(extracted_surveys):
    # extracted_surveys = list(extracted_surveys)
    # print(type(extracted_surveys))
    # Regular expression pattern to match email addresses
    email_pattern = r'\b[\w.-]+@[a-zA-Z.-]+\b'

    # Regular expression pattern to match gender-related words
    gender_pattern = r'\b(?:male|female|man|woman|boy|girl)\b'

    # Regular expression pattern to match ethnic region-related words
    ethnic_region_pattern = r'\b(?:race|ethnicity|origin|ethnic background)\b'

    # Religious pattern
    religious_pattern = r'\b(?:religion|religious beliefs|faith)\b'

    # Genetic pattern
    genetic_pattern = r'\b(?:genetic information|genetic data)\b'

    # Biometric pattern
    biometric_pattern = r'\b(?:biometric data|fingerprint|retina scan|iris scan|facial recognition)\b'

    # Health-related pattern
    health_pattern = r'\b(?:health information|medical data|medical history|disease|condition|treatment|medication)\b'

    # to mask email addresses
    def mask_email(match):
        return '***@***.com'

    # to mask names (assuming a name is two or more words)
    def mask_name(match):
        return '***'

    # Parse the JSON string into a Python object (list of dictionaries)
    # extracted_surveys = list(extracted_surveys)
    extracted_surveys = json.loads(extracted_surveys)
    print(type(extracted_surveys))
    # Extract names from "First/Given names" and "Last/Family names"
    names_to_mask = set()
    for item in extracted_surveys:
        first_name = item.get("First/Given names", "")
        last_name = item.get("Last/Family names", "")
        if first_name:
            names_to_mask.add(first_name)
        if last_name:
            names_to_mask.add(last_name)

    masked_data = []
    for item in extracted_surveys:
        masked_item = {}
        for key, value in item.items():
            if key == "Email Address":
                value = re.sub(email_pattern, mask_email, value)
            elif key in ["First/Given names", "Last/Family names"]:
                if value:
                    masked_name = "***"
                    masked_item[key] = masked_name
                else:
                    masked_item[key] = None
            else:
                # Mask names using regular expressions and country/continent names using spaCy
                if isinstance(value, str):
                    for name in names_to_mask:
                        value = value.replace(name, '***')
                    doc = nlp(value)
                    for ent in doc.ents:
                        # Filter country and continent names
                        if ent.label_ in ("GPE", "LOC"):
                            value = value.replace(ent.text, '***')
                    value = re.sub(gender_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(ethnic_region_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(religious_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(genetic_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(biometric_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    value = re.sub(health_pattern, '***',
                                   value, flags=re.IGNORECASE)
                    masked_item[key] = value
                else:
                    masked_item[key] = value
        masked_data.append(masked_item)

    return masked_data


class Transformcv:
    def __init__(self, extraction_data):
        self.extraction_data = extraction_data

    def masking_on_data(self):
        data = self.extraction_data

        data = utilities.clean_phone_number(data)

        # Load the pre-trained statistical model
        nlp = spacy.load("en_core_web_sm")
        # Process the text using spaCy
        doc = nlp(data)

        # List to store all the proper-nouns for human names
        pii = []

        mob_regex = r"\+?\d{1,4}[-\s\.]?\(?\d{1,4}\)?[-\s\.]?\d{1,10}[-\s\.]?\d{1,10}[-\s\.]?\d{1,10}"

        email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        # Common non-human names that we want to filter out
        excluded_names = {"Coursera", "Git", "Github", "Linkedln", "Python"}

        for token in doc:
            if token.pos_ == 'PROPN':
                # Check if it's a person's name or a country name based on NER
                if token.ent_type_ in ['PERSON', 'GPE'] and token.text.lower() not in map(str.lower, excluded_names):
                    pii.append(token.text)
                    # Replace the name with a mask (e.g., "MASKED")
                    data = re.sub(r'\b' + re.escape(token.text) +
                                  r'\b', "*****", data, flags=re.I)
            elif re.search(mob_regex, str(token), re.IGNORECASE):
                pii.append(token.text)
                data = re.sub(re.escape(token.text), "*****", data, flags=re.I)
            elif re.search(email_regex, token.text, re.IGNORECASE):
                pii.append(token.text)
                data = re.sub(re.escape(token.text), "*****", data, flags=re.I)

        return data, len(pii), pii


# if __name__ == "__main__":
    # Creating object of class
Transformcvobject = Transformcv(extracted_text)

masked_text, count, maskeddata = Transformcvobject.masking_on_data()

# print(dict_cvsurvey)
# print(extracted_text)
# print(extracted_surveys)
# print(masked_text)

# print("\n")
# print(count)
# print("\n")
# print(maskeddata)
# Process the JSON data
masked_survey = mask_sensitive_data(extracted_surveys)
# print(json.dumps(masked_survey, indent=2))
