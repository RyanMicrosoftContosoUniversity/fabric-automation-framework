import requests
import json
from .service_principal import ServicePrincipal


class API_Utils:
    """
    This will be used to initiate a scan and hold all data that results from a scan
    Will require an SPN instance to authenticate
    """
    @staticmethod
    def getReport(spn:ServicePrincipal, reportId:str) -> dict:
        """
        https://api.powerbi.com/v1.0/myorg/reports/{reportId}
        """
        url = f"https://api.powerbi.com/v1.0/myorg/reports/{reportId}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {spn.getAccessToken()}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get report: {response.status_code} {response.text}")
        
        

    