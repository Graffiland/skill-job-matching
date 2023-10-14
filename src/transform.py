from extraction import extracted_survey
import re
import json
import spacy

nlp = spacy.load("en_core_web_sm")

def mask_sensitive_data(extracted_survey):
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
    extracted_survey = json.loads(extracted_survey)

    # Extract names from "First/Given names" and "Last/Family names"
    names_to_mask = set()
    for item in extracted_survey:
        first_name = item.get("First/Given names", "")
        last_name = item.get("Last/Family names", "")
        if first_name:
            names_to_mask.add(first_name)
        if last_name:
            names_to_mask.add(last_name)

    masked_data = []
    for item in extracted_survey:
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
                        if ent.label_ in ("GPE", "LOC"):  # Filter country and continent names
                            value = value.replace(ent.text, '***')
                    value = re.sub(gender_pattern, '***', value, flags=re.IGNORECASE)
                    value = re.sub(ethnic_region_pattern, '***', value, flags=re.IGNORECASE)
                    value = re.sub(religious_pattern, '***', value, flags=re.IGNORECASE)
                    value = re.sub(genetic_pattern, '***', value, flags=re.IGNORECASE)
                    value = re.sub(biometric_pattern, '***', value, flags=re.IGNORECASE)
                    value = re.sub(health_pattern, '***', value, flags=re.IGNORECASE)
                    masked_item[key] = value
                else:
                    masked_item[key] = value
        masked_data.append(masked_item)

    return masked_data

# Process the JSON data
masked_json = mask_sensitive_data(extracted_survey)
print(json.dumps(masked_json, indent=2))

def calculate_accuracy(original_data, masked_data):
    total_items = len(original_data)
    correctly_masked = 0

    for i in range(total_items):
        original_item = original_data[i]
        masked_item = masked_data[i]

        if original_item != masked_item:
            correctly_masked += 1

    accuracy = (correctly_masked / total_items) * 100
    return accuracy

# Calculate accuracy
accuracy = calculate_accuracy(json.loads(extracted_survey), masked_json)
print(f"Accuracy: {accuracy:.2f}%")
