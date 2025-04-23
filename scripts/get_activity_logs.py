import json
from fabric_automation_framework.activity_events import ActivityLogs
from fabric_automation_framework.service_principal import ServicePrincipal

# # test
config_data = json.loads(open('docs/non-prod-spn-config.json').read())

spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)

# create activity logs object
activity_logs = ActivityLogs(spn=spn)

# # get month of activity logs
logs = activity_logs.get_30_days_activity_logs(write_path='docs/activity_logs.json')
