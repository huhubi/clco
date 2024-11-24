import unittest
import requests
import subprocess


class TestDeployedApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Retrieve the web app, SCM, and blob URLs from the main Python file."""
        result = subprocess.run(["pulumi", "stack", "output", "web_app_url"], capture_output=True, text=True)
        cls.web_app_url = result.stdout.strip()

        result = subprocess.run(["pulumi", "stack", "output", "scm_web_app_url"], capture_output=True, text=True)
        cls.scm_web_app_url = result.stdout.strip()

        result = subprocess.run(["pulumi", "stack", "output", "blob_url"], capture_output=True, text=True)
        cls.blob_url = result.stdout.strip()

    def test_web_app_url(self):
        """Test if the web app URL is accessible."""
        response = requests.get(self.web_app_url)
        self.assertEqual(response.status_code, 200, "Web app URL is not accessible.")

    def test_scm_web_app_url(self):
        """Test if the SCM web app URL is accessible."""
        response = requests.get(self.scm_web_app_url)
        self.assertEqual(response.status_code, 200, "SCM web app URL is not accessible.")

    def test_logstream_url(self):
        """Test if the logstream URL is accessible."""
        logstream_url = f"{self.scm_web_app_url}/api/logstream"
        response = requests.get(logstream_url)
        self.assertEqual(response.status_code, 200, "Logstream URL is not accessible.")

    def test_blob_url(self):
        """Test if the blob URL is accessible."""
        response = requests.get(self.blob_url)
        self.assertEqual(response.status_code, 200, "Blob URL is not accessible.")


if __name__ == "__main__":
    unittest.main()