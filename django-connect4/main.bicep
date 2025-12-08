// Bicep template to deploy Django Connect4 app to Azure App Service
param location string = 'centralus'
param appServicePlanName string = 'django-connect4-plan'
param webAppName string = 'django-connect4-app'
param skuName string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    tier: 'Basic'
    capacity: 1
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
      linuxFxVersion: 'PYTHON|3.9'
      appSettings: [
        {
          name: 'DJANGO_SETTINGS_MODULE'
          value: 'connect4.settings'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
    httpsOnly: true
  }
}

output webAppUrl string = webApp.properties.defaultHostName
