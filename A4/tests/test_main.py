import unittest
import os
import unittest
import os
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.identity import DefaultAzureCredential

# Define subscription_id
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "5bb64e70-0225-40e2-b87c-ede62684f322")

# Initialize Azure clients
credential = DefaultAzureCredential()
resource_client = ResourceManagementClient(credential, subscription_id)
web_client = WebSiteManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)

class TestDeployedApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Azure clients and required variables."""
        cls.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "5bb64e70-0225-40e2-b87c-ede62684f322")
        cls.resource_group_name = os.getenv("RESOURCE_GROUP_NAME", "resource_group")
        cls.web_app_name = os.getenv("WEB_APP_NAME", "webapp")
        cls.storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME", "storageaccount")

        # Initialize Azure clients
        credential = DefaultAzureCredential()
        cls.resource_client = ResourceManagementClient(credential, cls.subscription_id)
        cls.web_client = WebSiteManagementClient(credential, cls.subscription_id)
        cls.storage_client = StorageManagementClient(credential, cls.subscription_id)

    def test_resource_group_exists(self):
        """Test if the resource group exists."""
        resource_group = self.resource_client.resource_groups.get(self.resource_group_name)
        self.assertIsNotNone(resource_group, "Resource group does not exist.")

    def test_web_app_exists(self):
        """Test if the web app exists."""
        web_app = self.web_client.web_apps.get(self.resource_group_name, self.web_app_name)
        self.assertIsNotNone(web_app, "Web app does not exist.")
        self.assertEqual(web_app.kind, "app", "Web app kind is incorrect.")

    def test_web_app_url(self):
        """Test if the web app URL is accessible."""
        web_app = self.web_client.web_apps.get(self.resource_group_name, self.web_app_name)
        web_app_url = f"http://{web_app.default_host_name}"

        # Send an HTTP request to the web app
        import requests
        response = requests.get(web_app_url)
        self.assertEqual(response.status_code, 200, "Web app URL is not accessible.")

    def test_blob_exists(self):
        """Test if the blob exists in the storage account."""
        blob_service_client = BlobServiceClient(
            f"https://{self.storage_account_name}.blob.core.windows.net/",
            credential=DefaultAzureCredential()
        )
        container_client = blob_service_client.get_container_client("appcontainer")
        blob_list = list(container_client.list_blobs())

        self.assertTrue(any(blob.name == "appzip" for blob in blob_list), "Blob 'appzip' does not exist.")

    def test_app_insights_exists(self):
        """Test if Application Insights is configured."""
        from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
        app_insights_client = ApplicationInsightsManagementClient(
            DefaultAzureCredential(), self.subscription_id
        )
        app_insights = app_insights_client.components.list_by_resource_group(self.resource_group_name)
        self.assertTrue(any(insight.name == "appInsights" for insight in app_insights),
                        "Application Insights does not exist.")


if __name__ == "__main__":
    unittest.main()


class TestDeployedApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Azure clients and required variables."""
        cls.subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "5bb64e70-0225-40e2-b87c-ede62684f322")
        cls.resource_group_name = os.getenv("RESOURCE_GROUP_NAME", "resource_group")
        cls.web_app_name = os.getenv("WEB_APP_NAME", "webapp")
        cls.storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME", "storageaccount")

        # Initialize Azure clients
        credential = DefaultAzureCredential()
        cls.resource_client = ResourceManagementClient(credential, cls.subscription_id)
        cls.web_client = WebSiteManagementClient(credential, cls.subscription_id)
        cls.storage_client = StorageManagementClient(credential, cls.subscription_id)

    def test_resource_group_exists(self):
        """Test if the resource group exists."""
        resource_group = self.resource_client.resource_groups.get(self.resource_group_name)
        self.assertIsNotNone(resource_group, "Resource group does not exist.")

    def test_web_app_exists(self):
        """Test if the web app exists."""
        web_app = self.web_client.web_apps.get(self.resource_group_name, self.web_app_name)
        self.assertIsNotNone(web_app, "Web app does not exist.")
        self.assertEqual(web_app.kind, "app", "Web app kind is incorrect.")

    def test_web_app_url(self):
        """Test if the web app URL is accessible."""
        web_app = self.web_client.web_apps.get(self.resource_group_name, self.web_app_name)
        web_app_url = f"http://{web_app.default_host_name}"

        # Send an HTTP request to the web app
        import requests
        response = requests.get(web_app_url)
        self.assertEqual(response.status_code, 200, "Web app URL is not accessible.")

    def test_blob_exists(self):
        """Test if the blob exists in the storage account."""
        blob_service_client = BlobServiceClient(
            f"https://{self.storage_account_name}.blob.core.windows.net/",
            credential=DefaultAzureCredential()
        )
        container_client = blob_service_client.get_container_client("appcontainer")
        blob_list = list(container_client.list_blobs())

        self.assertTrue(any(blob.name == "appzip" for blob in blob_list), "Blob 'appzip' does not exist.")

    def test_app_insights_exists(self):
        """Test if Application Insights is configured."""
        from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
        app_insights_client = ApplicationInsightsManagementClient(
            DefaultAzureCredential(), self.subscription_id
        )
        app_insights = app_insights_client.components.list_by_resource_group(self.resource_group_name)
        self.assertTrue(any(insight.name == "appInsights" for insight in app_insights),
                        "Application Insights does not exist.")


if __name__ == "__main__":
    unittest.main()