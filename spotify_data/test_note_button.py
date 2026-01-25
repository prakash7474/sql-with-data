import requests

# Test the Note button functionality
url = 'http://127.0.0.1:5000/api/analyze-track'
data = {'url': 'https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh'}  # Shape of You

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
