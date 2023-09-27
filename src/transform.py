from extraction import extracted_survey
#print(extracted_survey)

import re
import json

def mask_sensitive_data(extracted_survey):
    # Regular expression pattern to match email addresses
    email_pattern = r'\b[\w.-]+@[a-zA-Z.-]+\b'

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
                masked_item[key] = re.sub(email_pattern, mask_email, value)
            elif key in ["First/Given names", "Last/Family names"]:
                if value:
                    masked_name = "***"
                    masked_item[key] = masked_name
                else:
                    masked_item[key] = None
            else:
                # Mask names and email addresses within text fields
                if isinstance(value, str):
                    for name in names_to_mask:
                        value = value.replace(name, '***')
                    masked_item[key] = re.sub(email_pattern, mask_email, value)
                else:
                    masked_item[key] = value
        masked_data.append(masked_item)

    return masked_data


# Process the JSON data
masked_json = mask_sensitive_data(extracted_survey)
print(json.dumps(masked_json, indent=2))