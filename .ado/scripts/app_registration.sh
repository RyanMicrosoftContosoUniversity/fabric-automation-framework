# Variables
appDisplayName="YourAppDisplayName"
tenantId=$(az account show --query tenantId -o tsv)

# Create the app registration
appId=$(az ad app create --display-name $appDisplayName --sign-in-audience AzureADMyOrg --query appId -o tsv)

# Create a service principal for the app
az ad sp create --id $appId

# Assign API permissions
# Microsoft Graph - User.Read
az ad app permission add --id $appId --api 00000003-0000-0000-c000-000000000000 --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope

# Power BI Service - Tenant.Read.All
az ad app permission add --id $appId --api 00000009-0000-0000-c000-000000000000 --api-permissions b0d7a3d6-0d6d-4d8a-9f1d-0b91f6f3b8ad=Role

# Grant admin consent for the required permissions
az ad app permission grant --id $appId --api 00000003-0000-0000-c000-000000000000 --scope User.Read
az ad app permission grant --id $appId --api 00000009-0000-0000-c000-000000000000 --scope Tenant.Read.All

# Output the app and service principal details
echo "App ID: $appId"