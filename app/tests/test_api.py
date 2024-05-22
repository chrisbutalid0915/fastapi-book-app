import json
import unittest

import requests
# from fastapi.testclient import TestClient


# client = TestClient()


class TestBookAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:8000"
    api_version = "/api/v1"


    def setUp(self):
        self.username = "chris"
        self.password = "En3il45"
        self.wrong_password = "wrong_password"
        self.token_url = f"{self.base_url}{self.api_version}/token"
        self.token_headers = {"content-type": "application/x-www-form-urlencoded"}
    
    def test_login(self):
        """Test with correct credentials"""
        payload = {"username": self.username, "password": self.password}
        response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("token_type", response.json())


    def test_invalid_login(self):
        """Test with incorrect credentials"""
        payload = {"username": self.username, "password": self.wrong_password}
        response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=payload)
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.json())


    def test_post_request(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" , self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address"
        payload = json.dumps(
            {"location": "Malolos", "latitude": 70.832211, "longitude": 120.23}
        )
        headers = {"content-type": "application/json", 
                 "Authorization": f'Bearer {token}'
                 }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)


    def test_post_required_field(self):
         # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address"
        payload = json.dumps(
            {
                "location": "Malolos",
                "latitude": 14.832211,
            }
        )
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 422)


    def test_put_request(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address/2"
        payload = json.dumps(
            {"location": "Baliwag", "latitude": 80.832211, "longitude": 120.25}
        )
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("PUT", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)


    def test_put_invalid_id(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address/122"
        payload = json.dumps(
            {"location": "Baliwag", "latitude": 14.832211, "longitude": 120.25}
        )
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("PUT", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_get_address_by_id(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address/2"
        payload = {}
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    def test_get_address_invalid_id(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address/1222"
        payload = {}
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

    # def test_delete_address_by_id(self):
    #     # Get the token first
    #     token_payload = {"username": self.username, "password": self.password}
    #     token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
    #     token = token_response.json()["access_token"]

    #     # use the token to access the protected endpoint

    #     url = f"{self.base_url}{self.api_version}/address/9"
    #     payload = {}
    #     headers = {"content-type": "application/json",
    #                "Authorization": f'Bearer {token}'
    #                }

    #     response = requests.request("DELETE", url, headers=headers, data=payload)

    #     self.assertEqual(response.status_code, 200)

    def test_delete_invalid_id(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address/12323"
        payload = {}
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 404)

    def test_address_distance(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f'{self.base_url}{self.api_version}/address/distance/'
        payload = json.dumps({
                    "distance": 100,
                    "latitude": 70,
                    "longitude": 120
                })
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)

    
    def test_get_addresses(self):
        # Get the token first
        token_payload = {"username": self.username, "password": self.password}
        token_response = requests.request("POST" ,self.token_url, headers=self.token_headers, data=token_payload)
        token = token_response.json()["access_token"]

        # use the token to access the protected endpoint
        url = f"{self.base_url}{self.api_version}/address"
        payload = {}
        headers = {"content-type": "application/json",
                   "Authorization": f'Bearer {token}'
                   }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
