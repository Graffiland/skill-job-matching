import sqlite3
import json
from transform import masked_cv, masked_survey, cvsurveyemail
import utilities


# Connect to the SQLite database

utilities.create_and_insert_skilljob_table(
    cvsurveyemail, masked_cv, masked_survey)
