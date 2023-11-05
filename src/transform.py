# Import Libraries
from extraction import extracted_survey
import json
from extraction import extracted_text
import utilities

extracted_survey = json.loads(extracted_survey)

# Creats a dictionary after using the method create_mapping that map both cv and survey on email.
dict_cvsurvey = utilities.create_mapping(extracted_text, extracted_survey)

# retruns cv and survey from the dictionary for masking
extracted_text, extracted_surveys, email = utilities.mask(dict_cvsurvey)
extracted_sur = [extracted_surveys]
extracted_surveys = json.dumps(extracted_sur)


class Transformsuvery:
    def __init__(self, extracted_surveys):
        self.extracted_surveys = extracted_surveys

    def masking_on_data(self):
        """
            This method of the class call on the mask function in utilities
            Mask the extracted_cv and returns the masked data 
        """
        data = self.extracted_surveys
        data = utilities.mask_sensitive_data(data)

        return data


class Transformcv:
    def __init__(self, extraction_data):
        self.extraction_data = extraction_data

    def masking_on_data(self):
        """
            This method of the class call on the mask function in utilities
            Mask the extracted_cv and returns the masked data 
        """
        data = self.extraction_data
        data = utilities.mask_personal_information_2(data)

        return data


# if __name__ == "__main__":

# Creating object of class
Transformcvobject = Transformcv(extracted_text)
Transformsurveyobject = Transformsuvery(extracted_surveys)

# Outputs
masked_cv = Transformcvobject.masking_on_data()
masked_survey = Transformsurveyobject.masking_on_data()
cvsurveyemail = email
