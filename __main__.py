"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("pulumi_rg")

# Create an Azure Storage Account
account = storage.StorageAccount(
    "sa",
    resource_group_name=resource_group.name,
    sku={
        "name": storage.SkuName.STANDARD_LRS,
    },
    kind=storage.Kind.STORAGE_V2,
)

# Create an Azure Static Web App
static_website = storage.StorageAccountStaticWebsite(
    "website",
    resource_group_name=resource_group.name,
    account_name=account.name,
    index_document="index.html",
)

index_html = storage.Blob(
    "index.html",
    resource_group_name=resource_group.name,
    account_name=account.name,
    container_name=static_website.container_name,
    blob_name="index.html",
    source=pulumi.FileAsset("./pulumi.html"),
    content_type="text/html",
)

pulumi.export("url", account.primary_endpoints.web)

# Export the storage account name
pulumi.export("storage_account_name", account.name)
