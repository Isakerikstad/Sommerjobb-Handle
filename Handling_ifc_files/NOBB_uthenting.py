import requests
from requests.auth import HTTPBasicAuth
import json



# replace with your credentials
username = input(str("Enter your username: "))
password = input(str("Enter your password: "))
base_url = 'https://export.byggtjeneste.no/api/v1'  # The URL of the API endpoint


# A function for getting all assortments from the NOBB api
def get_assortments(username=username, password=password, base_url=base_url):
    url = f"{base_url}/assortments"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={"accept": "text/plain"})
    # Make sure the request was successful
    if response.status_code == 200:
        # If successful, return the JSON response
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        try:
            print("Response headers:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
        except:
            pass
        return None
    

# A function for getting all items from the NOBB api in a certain assortment
def get_items_by_group(assortmentname):
    url = f"{base_url}/items/assortments/{assortmentname}"
    response = requests.get(url, auth=HTTPBasicAuth(username, password), headers={"accept": "text/plain"})
    # Make sure the request was successful
    if response.status_code == 200:
        # If successful, return the JSON response
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        try:
            print("Response headers:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
        except:
            pass
        return None
    
# A function for getting an item from the NOBB api with certain parameters: from (Optional) Filter by items changed from and including date. Format: yyyy-mm-dd, to (Optional) Filter by items changed before and including date. Format: yyyy-mm-dd, nobbnos (Optional) Filter by items: Comma-separated list of NOBB numbers, suppliers (Optional) Filter by suppliers: Comma-separated list of participant numbers.

def get_item(from_ = None, to = None, nobbnos = None, suppliers = None):
    url = f"{base_url}/items"
    params = {}
    if from_ is not None:
        params["from"] = from_
    if to is not None:
        params["to"] = to
    if nobbnos is not None:
        params["nobbnos"] = nobbnos
    if suppliers is not None:
        params["suppliers"] = suppliers
    print('params:', params)
    response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params, h={'accept': 'text/plain'})
    # Make sure the request was successful
    if response.status_code == 200:
        # If successful, return the JSON response
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        try:
            print("Response headers:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
        except:
            pass
        return None
    

# Get items by Nobb number or GTINs. Result can be filtered with selection fields. Batch with repetitive call by sepcifying from and length for each batch. I want just one element.   "select": { "nobbNo": true, "productText1": true, "productText2": true, "productDescription": true, "ownerParticipantNo": true, "ownerParticipantName": true
def post_items_search(from_ = None, length = None, nobbnos = None, gtinnos = None):
    url = f"{base_url}/items/search"
    params = {
        "from": from_ if from_ is not None else 0,
        "length": length if length is not None else 1000,
    }
    data = {
        "nobbNos": [nobbnos] if nobbnos is not None else [],
        "gtinNos": [gtinnos] if gtinnos is not None else [],
        "select": {
            "nobbNo": True,
            "productText1": True,
            "productText2": True,
            "productDescription": True,
            "ownerParticipantNo": True,
            "ownerParticipantName": True,
        }
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, params=params, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(username, password))
    
    # Make sure the request was successful
    if response.status_code == 200:
        # If successful, return the JSON response
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        try:
            print("Response headers:")
            for header, value in response.headers.items():
                print(f"{header}: {value}")
        except:
            pass
        return None
