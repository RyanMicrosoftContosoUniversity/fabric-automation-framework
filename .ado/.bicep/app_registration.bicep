param app_display_name string

resource app 'Microsoft.Graph/applications@1.0' = {
  name: app_display_name
  properties: {
    displayName: app_display_name
    signInAudience: 'AzureADMyOrg' // Single Tenant
    requiredResourceAccess: [
      {
        resourceAppId: '00000003-0000-0000-c000-000000000000' // Microsoft Graph
        resourceAccess: [
          {
            id: 'e1fe6dd8-ba31-4d61-89e7-88639da4683d' // User.Read
            type: 'Scope'
          }
        ]
      }
      {
        resourceAppId: '00000009-0000-0000-c000-000000000000' // Power BI Service
        resourceAccess: [
          {
            id: 'b0d7a3d6-0d6d-4d8a-9f1d-0b91f6f3b8ad' // Tenant.Read.All
            type: 'Role'
          }
        ]
      }
    ]
  }
}

