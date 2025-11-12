from azure.identity import DefaultAzureCredential

from azure.mgmt.datafactory import DataFactoryManagementClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-datafactory
# USAGE
    python pipelines_create_run.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = DataFactoryManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="910ebf13-1058-405d-b6cf-eda03e5288d1",
    )

    print(help(client.pipelines.create_run))

    response = client.pipelines.create_run(
        resource_group_name="AFDCookBookRG",
        factory_name="BicepADF",
        pipeline_name="pl_orchestration_recipe_4",
        parameters={
            "input1": {
                "type": "string",
                "value": "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-datafactory-copy-blob-to-blob/azuredeploy.json",
            },
            "input2": {
                "type": "string",
                "value": "https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/101-datafactory-copy-blob-to-blob/azuredeploy.parameters.json",
            },
        },
    )
    print(response)


# x-ms-original-file: specification/datafactory/resource-manager/Microsoft.DataFactory/stable/2018-06-01/examples/Pipelines_CreateRun.json
if __name__ == "__main__":
    main()



"""
ADLS Gen2 operation failed for: Operation returned an invalid status code 'NotFound'. Account: 'adforchstorrheus2test'. 
FileSystem: 'data'. Path: 'Value'. ErrorCode: 'PathNotFound'. Message: 'The specified path does not exist.'. RequestId: '3a5065fb-901f-0073-5652-cbadcd000000'. TimeStamp: 'Thu, 22 May 2025 19:45:39 GMT'.
Operation returned an invalid status code 'NotFound'
"""