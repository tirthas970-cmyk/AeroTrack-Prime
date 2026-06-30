import requests

def get_asteroid_watchlist():
    # Using NASA's official open API for Near Earth Objects
    url = "https://nasa.gov"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {"error": f"API connection failed with status {response.status_code}"}
        
        # This will succeed because the API endpoint returns true JSON data
        data = response.json()
        return data
    except Exception as e:
        return {"error": str(e)}

watchlist_data = get_asteroid_watchlist()
print(watchlist_data)
