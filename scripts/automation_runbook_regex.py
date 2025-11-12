import sys
import re
import requests

def main():
    print('Runbook started with regex approach...')

    # check if we have enough args (the user's snippet references x[5])
    if len(sys.argv) < 6:
        print('No webhook payload argument provided.  Exiting.')
        return
    
    # This is your snippet's logic: the user's code specifically looks at sys.argv[5].
    # (That might be because the entire payload is at index 5 for your environment.)
    raw_arg = sys.argv[5]
    print(f'raw_arg received: {raw_arg}')

    pattern = r'[a-zA-Z].*?True'
    match = re.search(pattern, raw_arg)


    if not match:
        print('Could not find a callback URL in the argument via regex.')
        return
    
    callback_url = match.group(0)
    print(f'Regex extrracted callback_url: {callback_url}')

    try:
        print('Hello World from the Runbook')

        # on success send status=200 
        response = requests.post(callback_url, json={"StatusCode": "200"})
        print(f'Callback response code: {response.status_code}')
        print('Workflow executed successfully')

    except Exception as e:
        print(f'Exception in runbook: {e}')
        # if something fails, call back with a failure code
        error_data = {
            "statusCode": "500",
            "Error": {
                "ErrorCode": 100,
                "Message": str(e)
            }   
        }
        requests.post(callback_url, json=error_data)

if __name__ == '__main__':
    main()


    