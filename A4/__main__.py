import pulumi
from pulumi_azure_native import resources, storage, web, operationalinsights
from pulumi import AssetArchive, FileArchive, Config
from pulumi_azure_native import insights
resource_group = resources.ResourceGroup("resource_group", location="eastus2")

# if return code is 429, change to germanywestcentral, uksouth, eastus2 etc.

# Retrieve configuration values
config = Config()
workspace_name = config.require("workspace_name")

# Create a Storage Account
storage_account = storage.StorageAccount(
    "storageaccount",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(name=storage.SkuName.STANDARD_LRS),
    kind=storage.Kind.STORAGE_V2,
    allow_blob_public_access=True,  # Enable public access at the storage account level
)

# Create a Blob Container
container = storage.BlobContainer(
    "appcontainer",
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    public_access=storage.PublicAccess.CONTAINER,  # Enable public access
)
# Upload the application code as a zip file to the Blob
app_code = AssetArchive({".": FileArchive(".")})  # Archive current directory
blob = storage.Blob(
    "appzip",
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    container_name=container.name,
    source=app_code,
)

# Get the Blob URL
blob_url = pulumi.Output.concat(
    "https://",
    storage_account.name,
    ".blob.core.windows.net/",
    container.name,
    "/",
    blob.name,
)

# Create a Web App Service Plan
app_service_plan = web.AppServicePlan(
    "appserviceplan",
    resource_group_name=resource_group.name,
    kind="Linux",  # Set to Linux
    reserved=True,
    sku=web.SkuDescriptionArgs(
        tier="Basic",
        name="F1",  # Adjust based on requirements
    ),
)

# Create the Web App
web_app = web.WebApp(
    "webapp",
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(name="WEBSITES_ENABLE_APP_SERVICE_STORAGE", value="false"),
            web.NameValuePairArgs(name="WEBSITE_RUN_FROM_PACKAGE", value=blob_url),
        ],
        linux_fx_version="PYTHON|3.11",
    ),
)
subscription_id = "5bb64e70-0225-40e2-b87c-ede62684f322"
resource_group_name = resource_group.name


# Create a Log Analytics Workspace
workspace = operationalinsights.Workspace(
    "logAnalyticsWorkspace",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=operationalinsights.WorkspaceSkuArgs(
        name="PerGB2018"
    ),
    retention_in_days=30,
)

# Create an Application Insights resource
app_insights = insights.Component(
    "appInsights",
    resource_group_name=resource_group.name,
    application_type="web",
    location=resource_group.location,
    kind="web",
    ingestion_mode="LogAnalytics",
    workspace_resource_id=workspace.id,
)

# Export the instrumentation key
pulumi.export("app_insights_instrumentation_key", app_insights.instrumentation_key)


# Export outputs
pulumi.export("resource_group_name", resource_group.name)
pulumi.export("web_app_url", pulumi.Output.concat("http://", web_app.default_host_name))
pulumi.export("blob_url", blob_url)
pulumi.export("scm_web_app_url", pulumi.Output.concat("http://", web_app.default_host_name.apply(lambda name: name.replace(".azurewebsites.net", ".scm.azurewebsites.net"))))
pulumi.export("log_tail_command", pulumi.Output.all(web_app.name, resource_group.name).apply(lambda args: f"az webapp log tail --name {args[0]} --resource-group {args[1]}"))

# Log the web app URL to the info column
web_app.default_host_name.apply(lambda url: pulumi.log.info(f"Web App URL: http://{url}"))
