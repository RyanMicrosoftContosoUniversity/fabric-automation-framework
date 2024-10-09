from src.service_principal import ServicePrincipal
from src.scan import Scan   
import json



# base tests
config_data = json.loads(open('docs/non-prod-spn-config.json').read())
spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)
    
scan = Scan(spn=spn)

# pass scan request id to get scan status
scan_status = scan.get_scan_status(scan_id=scan.scan_request['id'])

# write scan to file in docs folder
with open('docs/scan_response.json', 'w') as f:
    json.dump(scan.scan_results, f, indent=4)

