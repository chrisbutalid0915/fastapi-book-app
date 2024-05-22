import json
import unittest

import requests


class TestBookAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"

    def test_post_request(self):
        url = f"{self.base_url}/create_address"

        payload = json.dumps(
            {"location": "Malolos", "latitude": 14.832211, "longitude": 120.23}
        )

        headers = {"content-type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_post_required_field(self):
        url = f"{self.base_url}/create_address"

        payload = json.dumps(
            {
                "location": "Malolos",
                "latitude": 14.832211,
            }
        )

        headers = {"content-type": "application/json"}

        response = requests.request("POST", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 422)

    def test_put_request(self):
        url = f"{self.base_url}/update_address/9"

        payload = json.dumps(
            {"location": "Baliwag", "latitude": 14.832211, "longitude": 120.25}
        )

        headers = {"content-type": "application/json"}

        response = requests.request("PUT", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_put_invalid_id(self):
        url = f"{self.base_url}/update_address/122"

        payload = json.dumps(
            {"location": "Baliwag", "latitude": 14.832211, "longitude": 120.25}
        )

        headers = {"content-type": "application/json"}

        response = requests.request("PUT", url, headers=headers, data=payload)

        self.assertEqual(response.status_code, 404)

    def test_get_address_by_id(self):
        url = f"{self.base_url}/get_address/11"

        payload = {}
        headers = {"content-type": "application/json"}

        respose = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(respose.status_code, 200)

    def test_get_address_invalid_id(self):
        url = f"{self.base_url}/get_address/1222"

        payload = {}
        headers = {"content-type": "application/json"}

        respose = requests.request("GET", url, headers=headers, data=payload)

        self.assertEqual(respose.status_code, 404)

    def test_delete_address_by_id(self):
        url = f"{self.base_url}/delete_address/15"

        payload = {}
        headers = {"content-type": "application/json"}

        respose = requests.request("DELETE", url, headers=headers, data=payload)

        self.assertEqual(respose.status_code, 200)

    def test_delete_invalid_id(self):
        url = f"{self.base_url}/delete_address/12323"

        payload = {}
        headers = {"content-type": "application/json"}

        respose = requests.request("DELETE", url, headers=headers, data=payload)

        self.assertEqual(respose.status_code, 404)


if __name__ == "__main__":
    unittest.main()
