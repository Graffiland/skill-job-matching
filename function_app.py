import json
import azure.functions as func
import logging
from src.Chartgpt import process_data 

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="skilljob")
def skilljob(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
            masked_cv_result= req_body.get('masked_cv')
            masked_survey_result= req_body.get('masked_survey')
            
            # Call LLM script to process data
            processed_result = process_data(masked_cv_result, masked_survey_result)
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            
    # Return the processed result to the web app
    if name:
        return func.HttpResponse(json.dumps({"result": processed_result}), status_code=200, mimetype="application/json")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )