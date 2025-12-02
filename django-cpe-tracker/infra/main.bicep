// Bicep template for deploying Django app to Azure App Service with PostgreSQL
param location string = resourceGroup().location
param appServicePlanName string = 'cpeAppServicePlan'
param webAppName string = 'cpeWebApp'
param postgresServerName string = 'cpepg${uniqueString(resourceGroup().id)}'
param postgresDbName string = 'cpe_db'
param storageAccountName string = toLower('cpe${uniqueString(resourceGroup().id)}storage')

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
    }
  }
}

resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: 'pgadminuser'
    administratorLoginPassword: adminPassword
    version: '15'
    storage: {
      storageSizeGB: 32
    }
    highAvailability: {
      mode: 'Disabled'
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    createMode: 'Default'
  }
}

resource postgresDb 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: postgresDbName
  parent: postgresServer
  properties: {}
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {}
}

output webAppName string = webApp.name
output webAppUrl string = webApp.properties.defaultHostName
output postgresServerName string = postgresServer.name
output postgresDbName string = postgresDb.name
output storageAccountName string = storageAccount.name
@secure()
param adminPassword string
