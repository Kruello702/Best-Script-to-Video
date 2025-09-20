# Azure Setup Guide - Script to Video Generator

This guide provides detailed instructions for setting up Microsoft Azure services to enable cloud features in the Script to Video Generator application.

## 🎯 Overview

The application integrates with several Azure services:
- **Azure Blob Storage**: Video file storage and hosting
- **Azure Media Services**: Video streaming and encoding
- **Azure AI Video Indexer**: Video analysis and insights
- **Azure CDN**: Global content delivery
- **Azure Application Insights**: Monitoring and analytics

## 📋 Prerequisites

### Azure Account Requirements
- Active Azure subscription
- Sufficient credits or billing setup
- Owner or Contributor role on the subscription

### Local Tools
- Azure CLI installed and configured
- PowerShell or Bash terminal
- Text editor for configuration files

## 🚀 Step-by-Step Setup

### Step 1: Create Resource Group

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "Your Subscription Name"

# Create resource group
az group create \
  --name "rg-video-generator" \
  --location "East US"
```

### Step 2: Create Storage Account

```bash
# Create storage account
az storage account create \
  --name "stvideogenerator$(date +%s)" \
  --resource-group "rg-video-generator" \
  --location "East US" \
  --sku "Standard_LRS" \
  --kind "StorageV2"

# Get storage account key
STORAGE_KEY=$(az storage account keys list \
  --resource-group "rg-video-generator" \
  --account-name "stvideogenerator$(date +%s)" \
  --query "[0].value" --output tsv)

# Create containers
az storage container create \
  --name "videos" \
  --account-name "stvideogenerator$(date +%s)" \
  --account-key "$STORAGE_KEY" \
  --public-access blob

az storage container create \
  --name "thumbnails" \
  --account-name "stvideogenerator$(date +%s)" \
  --account-key "$STORAGE_KEY" \
  --public-access blob
```

### Step 3: Create Media Services Account

```bash
# Create Media Services account
az ams account create \
  --name "amsvideogen$(date +%s)" \
  --resource-group "rg-video-generator" \
  --storage-account "stvideogenerator$(date +%s)" \
  --location "East US"

# Create service principal for authentication
az ad sp create-for-rbac \
  --name "sp-video-generator" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-video-generator
```

### Step 4: Configure Video Indexer

```bash
# Create Video Indexer account (via Azure portal)
# 1. Go to Azure Portal
# 2. Search for "Video Indexer"
# 3. Create new Video Indexer account
# 4. Link to your Media Services account
```

### Step 5: Create CDN Profile

```bash
# Create CDN profile
az cdn profile create \
  --name "cdn-video-generator" \
  --resource-group "rg-video-generator" \
  --sku "Standard_Microsoft" \
  --location "Global"

# Create CDN endpoint
az cdn endpoint create \
  --name "videos-$(date +%s)" \
  --profile-name "cdn-video-generator" \
  --resource-group "rg-video-generator" \
  --origin "stvideogenerator$(date +%s).blob.core.windows.net" \
  --origin-host-header "stvideogenerator$(date +%s).blob.core.windows.net"
```

## 🔐 Authentication Setup

### Option 1: Service Principal (Recommended for Production)

```bash
# Create service principal
SP_OUTPUT=$(az ad sp create-for-rbac \
  --name "sp-video-generator-prod" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv))

# Extract values
CLIENT_ID=$(echo $SP_OUTPUT | jq -r '.appId')
CLIENT_SECRET=$(echo $SP_OUTPUT | jq -r '.password')
TENANT_ID=$(echo $SP_OUTPUT | jq -r '.tenant')

echo "Client ID: $CLIENT_ID"
echo "Client Secret: $CLIENT_SECRET"
echo "Tenant ID: $TENANT_ID"
```

### Option 2: Managed Identity (For Azure-hosted applications)

```bash
# Enable system-assigned managed identity on your App Service
az webapp identity assign \
  --name "your-app-name" \
  --resource-group "rg-video-generator"

# Grant permissions to storage account
az role assignment create \
  --assignee $(az webapp identity show --name "your-app-name" --resource-group "rg-video-generator" --query principalId -o tsv) \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-video-generator/providers/Microsoft.Storage/storageAccounts/stvideogenerator*
```

## ⚙️ Environment Configuration

### Backend Environment Variables

Create a `.env` file in your backend directory:

```env
# Azure Storage
AZURE_STORAGE_ACCOUNT_NAME=stvideogenerator1234567890
AZURE_STORAGE_ACCOUNT_KEY=your-storage-account-key-here

# Azure Media Services
AZURE_MEDIA_SERVICES_ACCOUNT=amsvideogen1234567890
AZURE_RESOURCE_GROUP=rg-video-generator
AZURE_SUBSCRIPTION_ID=your-subscription-id-here

# Service Principal Authentication
AZURE_CLIENT_ID=your-client-id-here
AZURE_CLIENT_SECRET=your-client-secret-here
AZURE_TENANT_ID=your-tenant-id-here

# Video Indexer
AZURE_VIDEO_INDEXER_ACCOUNT_ID=your-video-indexer-account-id
AZURE_VIDEO_INDEXER_LOCATION=eastus

# CDN
AZURE_CDN_PROFILE=cdn-video-generator
AZURE_CDN_ENDPOINT=videos-1234567890
```

### Application Configuration

Update your Flask application configuration:

```python
# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure Storage
    AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    AZURE_STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    
    # Azure Media Services
    AZURE_MEDIA_SERVICES_ACCOUNT = os.getenv('AZURE_MEDIA_SERVICES_ACCOUNT')
    AZURE_RESOURCE_GROUP = os.getenv('AZURE_RESOURCE_GROUP')
    AZURE_SUBSCRIPTION_ID = os.getenv('AZURE_SUBSCRIPTION_ID')
    
    # Authentication
    AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
    AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
```

## 🧪 Testing the Setup

### Test Storage Connection

```python
# test_azure_storage.py
from azure.storage.blob import BlobServiceClient
import os

def test_storage_connection():
    try:
        blob_service_client = BlobServiceClient(
            account_url=f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net",
            credential=os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
        )
        
        # List containers
        containers = blob_service_client.list_containers()
        print("Storage connection successful!")
        print("Containers:", [c.name for c in containers])
        
    except Exception as e:
        print(f"Storage connection failed: {e}")

if __name__ == "__main__":
    test_storage_connection()
```

### Test Media Services Connection

```python
# test_media_services.py
from azure.identity import ClientSecretCredential
from azure.mgmt.media import AzureMediaServices
import os

def test_media_services():
    try:
        credential = ClientSecretCredential(
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET')
        )
        
        client = AzureMediaServices(
            credential=credential,
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID')
        )
        
        # List assets
        assets = client.assets.list(
            resource_group_name=os.getenv('AZURE_RESOURCE_GROUP'),
            account_name=os.getenv('AZURE_MEDIA_SERVICES_ACCOUNT')
        )
        
        print("Media Services connection successful!")
        print("Assets count:", len(list(assets)))
        
    except Exception as e:
        print(f"Media Services connection failed: {e}")

if __name__ == "__main__":
    test_media_services()
```

### Test API Endpoints

```bash
# Test Azure status endpoint
curl -X GET http://localhost:5000/api/azure/status

# Test upload endpoint (with a test file)
curl -X POST http://localhost:5000/api/azure/upload \
  -H "Content-Type: application/json" \
  -d '{"video_path": "/path/to/test/video.mp4"}'
```

## 💰 Cost Optimization

### Storage Costs
- Use **Hot** tier for frequently accessed videos
- Use **Cool** tier for archive videos
- Enable **lifecycle management** for automatic tier transitions

```bash
# Set lifecycle management policy
az storage account management-policy create \
  --account-name "stvideogenerator$(date +%s)" \
  --resource-group "rg-video-generator" \
  --policy @lifecycle-policy.json
```

### Media Services Costs
- Use **Standard** encoding for most videos
- Use **Premium** encoding only when necessary
- Delete unused assets and streaming locators

### CDN Costs
- Configure appropriate **caching rules**
- Use **compression** to reduce bandwidth
- Monitor usage and adjust as needed

## 🔒 Security Best Practices

### Access Control
```bash
# Create custom role with minimal permissions
az role definition create --role-definition '{
  "Name": "Video Generator Storage Access",
  "Description": "Custom role for video generator storage access",
  "Actions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/write",
    "Microsoft.Storage/storageAccounts/blobServices/generateUserDelegationKey/action"
  ],
  "AssignableScopes": ["/subscriptions/YOUR_SUBSCRIPTION_ID"]
}'
```

### Network Security
```bash
# Configure storage account firewall
az storage account update \
  --name "stvideogenerator$(date +%s)" \
  --resource-group "rg-video-generator" \
  --default-action Deny

# Add allowed IP ranges
az storage account network-rule add \
  --account-name "stvideogenerator$(date +%s)" \
  --resource-group "rg-video-generator" \
  --ip-address "YOUR_IP_ADDRESS"
```

### Key Management
```bash
# Create Key Vault for secrets
az keyvault create \
  --name "kv-video-generator" \
  --resource-group "rg-video-generator" \
  --location "East US"

# Store secrets
az keyvault secret set \
  --vault-name "kv-video-generator" \
  --name "storage-key" \
  --value "$STORAGE_KEY"
```

## 📊 Monitoring and Alerts

### Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app "ai-video-generator" \
  --location "East US" \
  --resource-group "rg-video-generator" \
  --kind web
```

### Set up Alerts
```bash
# Create action group
az monitor action-group create \
  --name "video-generator-alerts" \
  --resource-group "rg-video-generator" \
  --short-name "vgalerts"

# Create metric alert
az monitor metrics alert create \
  --name "high-storage-usage" \
  --resource-group "rg-video-generator" \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-video-generator/providers/Microsoft.Storage/storageAccounts/stvideogenerator* \
  --condition "avg UsedCapacity > 80000000000" \
  --description "Storage usage is high"
```

## 🔧 Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Check service principal permissions
az role assignment list --assignee $CLIENT_ID

# Test authentication
az login --service-principal -u $CLIENT_ID -p $CLIENT_SECRET --tenant $TENANT_ID
```

#### Storage Access Issues
```bash
# Check storage account status
az storage account show \
  --name "stvideogenerator$(date +%s)" \
  --resource-group "rg-video-generator"

# Test blob access
az storage blob list \
  --container-name "videos" \
  --account-name "stvideogenerator$(date +%s)" \
  --account-key "$STORAGE_KEY"
```

#### Media Services Issues
```bash
# Check Media Services account
az ams account show \
  --name "amsvideogen$(date +%s)" \
  --resource-group "rg-video-generator"

# List streaming endpoints
az ams streaming-endpoint list \
  --account-name "amsvideogen$(date +%s)" \
  --resource-group "rg-video-generator"
```

### Debug Mode
Enable debug logging in your application:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Azure SDK logging
logging.getLogger('azure').setLevel(logging.DEBUG)
```

## 📚 Additional Resources

### Documentation
- [Azure Storage Documentation](https://docs.microsoft.com/en-us/azure/storage/)
- [Azure Media Services Documentation](https://docs.microsoft.com/en-us/azure/media-services/)
- [Azure Video Indexer Documentation](https://docs.microsoft.com/en-us/azure/media-services/video-indexer/)

### SDKs and Tools
- [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)

### Support
- [Azure Support](https://azure.microsoft.com/en-us/support/)
- [Stack Overflow - Azure](https://stackoverflow.com/questions/tagged/azure)
- [Azure Community](https://techcommunity.microsoft.com/t5/azure/ct-p/Azure)

---

**This guide provides a comprehensive setup for Azure integration. For specific use cases or advanced configurations, please refer to the official Azure documentation.**

