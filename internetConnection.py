import requests

def isConnected() -> bool:
    try:
        request = requests.get("https://www.google.com", timeout=5)
        connected = True
    except (requests.ConnectionError, requests.Timeout) as exception:
        connected = False
    
    return connected