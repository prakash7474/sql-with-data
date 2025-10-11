import http.client
import json

def get_languages():
    try:
        conn = http.client.HTTPSConnection("worldwide-restaurants.p.rapidapi.com")

        headers = {
            "x-rapidapi-key": "72f7f8db6cmsh86cea59b26e8ccap1c2c45jsn7086577bc614",
            "x-rapidapi-host": "worldwide-restaurants.p.rapidapi.com"
        }

        conn.request("GET", "/languages", headers=headers)
        res = conn.getresponse()

        if res.status != 200:
            print(f"Error: Received status code {res.status}")
            return None

        data = res.read()
        return json.loads(data.decode("utf-8"))

    except Exception as e:
        print(f"Request failed: {e}")
    finally:
        conn.close()

# Example usage
if __name__ == "__main__":
    languages = get_languages()
    if languages:
        print(json.dumps(languages, indent=2))
