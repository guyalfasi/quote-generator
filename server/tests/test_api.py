import requests

url = "http://127.0.0.1:5000/generate"
data = {
    "character": "gafsdgfsad",
    "quote": "bye"
}

# Send POST request with JSON payload
response = requests.post(url, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
