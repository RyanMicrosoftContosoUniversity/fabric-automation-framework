import json
import logging

def read_config_file(api_name, config_folder):

    """
    Synopsis:
    Reads the configuration file for a given API name from a specified folder.
    It prints the API name and file path, then attempts to load and return the configuration data
    in JSON format.

    Args:
    api_name (str): The name of the API for which the configuration file is to be read.
    config_folder (str): The folder path where configuration files are stored.

    Return:
    dict or None: Returns a dictionary with the configuration data if successful.
                  Returns None if the file is not found or if it contains invalid JSON.
    """
    
    file_path = config_folder+api_name+'.json'
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            print(content)

            f.seek(0)
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit() #temporary exit to stop execution, need to gracefully exit and stop session
        # return None
    except json.JSONDecodeError:
        exit() #temporary exit to stop execution, need to gracefully exit and stop session
    except :
        exit()
        # return None


# test
data = read_config_file('non-prod-spn-config', 'docs/')