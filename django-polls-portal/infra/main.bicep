targetScope = 'resourceGroup'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Web app name')
param webAppName string

@description('App Service plan name')
param appServicePlanName string

@description('Storage account name')
param storageAccountName string

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    siteConfig: {
      appSettings: [
        {
          name: 'DJANGO_SETTINGS_MODULE'
          value: 'polls_portal.settings'
        }
      ]
    }
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
