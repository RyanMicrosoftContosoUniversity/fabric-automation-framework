param keyVaultName string
param location string = resourceGroup().location
param tenantID string = subscription().tenantId
param keyVaultURL string

resource keyVault 'Microsoft.KeyVault/vaults@2021-04-01-preview' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: tenantID
    accessPolicies: []
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: true
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    provisioningState: 'Succeeded'
    publicNetworkAccess: 'Enabled'
    vaultUri: keyVaultURL
  }
}

output keyVaultId string = keyVault.id

