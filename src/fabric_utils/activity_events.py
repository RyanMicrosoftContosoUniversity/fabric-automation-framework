"""
This module will be used to get activity events for a workspace
"""
import requests
from datetime import datetime, timedelta
import json

class ActivityLogs:
    """
    This class will be used to get activity logs for a workspace
    """
    def __init__(self, spn):
        self.spn = spn

        self.activity_logs = self.get_activity_logs()

    def get_activity_logs(self, startDateTime:str=None, endDateTime:str=None, continuationToken:str=None, filter:str=None):
        """
        Get activity logs for a workspace
        startDate: str: Start date and time in UTC. The format is 'YYYY-MM-DDTHH:MM:SSZ'. 
        endDate: str: End date and time in UTC. Default is now
        """
        if startDateTime==None and endDateTime==None:
            startDateTime = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')
            endDateTime = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT00:00:00')

        if continuationToken!=None and filter!=None:
            url = f'https://api.powerbi.com/v1.0/myorg/admin/activityevents?startDateTime={startDateTime}&endDateTime={endDateTime}&continuationToken={continuationToken}&$filter={filter}'
        else:
            url = f"https://api.powerbi.com/v1.0/myorg/admin/activityevents?startDateTime='{startDateTime}'&endDateTime='{endDateTime}'"

        response = requests.get(url, headers={'Authorization': f'Bearer {self.spn.access_token}'})

        return response.json()

    def get_30_days_activity_logs(self, write_path=str):
        """
        
        """
        logs_schema = self.create_log_schema()
        day_counter = 30

        while day_counter>0:
            log_date = (datetime.now() - timedelta(days=day_counter)).strftime('%Y-%m-%d')
            startDateTime = (datetime.now() - timedelta(days=day_counter)).strftime('%Y-%m-%dT00:00:00')
            endDateTime = (datetime.now() - timedelta(days=day_counter)).strftime('%Y-%m-%dT00:00:00')

            logs = self.get_activity_logs(startDateTime=startDateTime, endDateTime=endDateTime)

            # add date
            logs['date'] = log_date
            # add logs to schema
            logs_schema['activity_logs_list'].append(logs)

            day_counter -= 1

        if day_counter==0:
            with open(write_path, 'a') as f:
                json.dump(logs_schema, f, indent=4)

        print(f'logs written to {write_path}')
        return f'logs written to {write_path}'
    
    def create_log_schema(self):
        """
        Create a schema for the activity logs
        """
        logs_schema = {
            "activity_logs_list": []
        }

        return logs_schema
