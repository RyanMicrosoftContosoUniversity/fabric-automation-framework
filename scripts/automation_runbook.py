import sys
import json
import time
import requests

def main():
    print('Runbook started...')

    # these will be populated from the webhook payload
    callback_url = None

    # Check if we have at least one argumant (the JSON payload)
    if len(sys.argv) > 1:
        raw_input = sys.argv[1]
        try:
            #2 Parse the top-level JSON
            top_level = json.loads(raw_input)
            print(f'Top-Level webhook data parsed: {top_level}')

            # 3 Extract the RequestBody string
            request_body_str = top_level.get('RequestBody', '')
            request_body_str = request_body_str.strip()

            if request_body_str:
                # 4 parse the RequestBody JSON (which contains 'callBackUri', etc)
                body_json = json.loads(request_body_str)

                # 5 finally extract the callback URL
                callback_url = body_json.get('callBackUri')
                print(f'Parsed callback_url: {callback_url}')

        except Exception as e:
            print(f'Could not parse webhook payload: {e}')
    else:
        print('No webhook payload was provided to the runbook')

    # simulate a short task
    time.sleep(5)

    print('Runbook finishing... now calling back to ADF if callback URL is present.')

    # If this runbook was invoked by ADF's webhook activity, we should POST back
    # to the callback URL to signal success (or failure)
    if callback_url:
        try:
            # Construct a simple JSON body indicating success
            payload = {
                'status': 'Succeeded',
                'message': 'Runbook completed successfully'
            }
            headers = {'Content-Type': 'application/json'}

            response = requests.post(callback_url, json=payload, headers=headers)
            print(f'Callback response status code: {response.status_code}')
            print(f'Callback response body: {response.text}')
        except Exception as cb_ex:
            print(f'Error calling back to ADF: {cb_ex}')

    print('Runbook completed successfully')

if __name__ == '__main__':
    main()




### Working
import sys
import re
import requests

x=sys.argv
pattern = r'[a-zA-Z].*?True'
match = re.search(pattern, x[5])
callback_uri = match.group(0)

try:
    print('Hello World')

except Exception as e:
    err=str(e)
    error_data = {"StatusCode": "500", "Error": {"ErrorCode": 100, "Message": err}}
    response = requests.post(callback_uri, json=error_data)
    raise e

else: 
    response = requests.post(callback_uri, json={"StatusCode": "200"})
    print('Workflow executed successfully')



from azure.ai.ml.entities import Data

# Register a new version of a dataset
my_dataset = Data(
    path="path/to/your/data",
    type=AssetTypes.URI_FILE,
    description="Updated version of the dataset with new records",
    name="my_dataset_name",  # Same name as the original dataset
    version="2"  # Specify a new version number
)
