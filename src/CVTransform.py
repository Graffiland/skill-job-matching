from extraction import extracted_text
import spacy
import re
import utilities


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


if __name__ == "__main__":
    # Creating object of class
    Transformcvobject = Transformcv(extracted_text)

    masked_text, count, maskeddata = Transformcvobject.masking_on_data()

    print(masked_text)
    print("\n")
    print(count)
    print("\n")
    print(maskeddata)
