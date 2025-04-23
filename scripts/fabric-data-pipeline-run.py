from fabric_automation_framework.service_principal import ServicePrincipal
from fabric_automation_framework.fabricDataPipeline import FabricDataPipelineRun
import json
import time
import requests
        

# base tests
config_data = json.loads(open('docs/non-prod-spn-config.json').read())
spn = ServicePrincipal(
    client_id=config_data['client_id'],
    tenant_id=config_data['tenant_id'],
    spn_secret_name=config_data['spn_secret_name'],
    vault_url=config_data['vault_url']
)
    

workspace_id = 'c0a7b8a9-eb12-495a-b863-2cb583e31154'
pipeline_id = '114cad78-70c4-4c85-8d16-7e5210f9231d'

job_url = FabricDataPipelineRun.run_on_demand_item_job(spn, workspace_id, pipeline_id)

# get job id
job_id = FabricDataPipelineRun.get_jobid_from_job_url(job_url)

# check job status
job_status = FabricDataPipelineRun.check_job_status(spn, workspace_id, pipeline_id, job_id)



