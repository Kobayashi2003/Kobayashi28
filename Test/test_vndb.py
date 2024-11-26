import requests
from typing import Dict, Any, Optional

class APITester:
    def __init__(self, base_url: str, default_method: str = 'GET', default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.default_method = default_method
        self.default_headers = default_headers or {}
        self.session = requests.Session()

    def _send_request(self, endpoint: str, method: Optional[str] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        method = method or self.default_method
        
        # Merge default headers with provided headers
        request_headers = self.default_headers.copy()
        if headers:
            request_headers.update(headers)

        return self.session.request(method, url, headers=request_headers, **kwargs)

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request(endpoint, method='GET', **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request(endpoint, method='POST', **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request(endpoint, method='PUT', **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._send_request(endpoint, method='DELETE', **kwargs)

    def assert_status_code(self, response: requests.Response, expected_status_code: int):
        assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"

    def assert_json_key(self, response: requests.Response, key: str):
        assert key in response.json(), f"Expected key '{key}' not found in response JSON"

    def assert_json_value(self, response: requests.Response, key: str, expected_value: Any):
        assert response.json()[key] == expected_value, f"Expected value '{expected_value}' for key '{key}', but got '{response.json()[key]}'"

    def print_response_details(self, response: requests.Response):
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")

def test_vns():
    api_tester = APITester(
        base_url="http://localhost:5000",
        default_method="GET",
        default_headers={"Content-Type": "application/json"}
    )
    vns_endpoint = "/api/v4/vns"
    tasks_endpoint = "/api/v4/tasks"

    response = api_tester.get(vns_endpoint)
    api_tester.assert_status_code(response, 202)
    api_tester.assert_json_key(response, "task_id")
    api_tester.print_response_details(response)

    task_id = response.json().get("task_id")

    response = api_tester.get(f"{tasks_endpoint}/{task_id}/result")
    api_tester.assert_status_code(response, 200)
    api_tester.assert_json_key(response, "status")
    api_tester.assert_json_value(response, "status", "SUCCESS")
    api_tester.print_response_details(response)
