import requests
import json
from .models import CarDealer, CarMake, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    try:
        response =  requests.get(url, params=kwargs)
        # Call get method of requests library with URL and parameters
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    api_key = kwargs.get("api_key", None)
    params = {
        "text": kwargs.get("text", ""),
        "version": kwargs.get("version", ""),
        "features": kwargs.get("features", ""),
        "return_analyzed_text": kwargs.get("return_analyzed_text", "")
    }
    headers = {'Content-Type': 'application/json'}
    if api_key:
        print("API_KEY", api_key)
        print("CALLING SECURE API WITH PARAMS: ", params)
        # Basic authentication GET
        response = requests.post(url, params=params, headers=headers,
                                json=json_payload, auth=HTTPBasicAuth('apikey', api_key))
    else:
        # no auth
        response =  requests.post(url, params=kwargs, json=json_payload)

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], state=dealer['state'], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["result"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review["dealership"],  # Assuming dealership_id is the correct field
                          name=review["name"],
                          purchase=review["purchase"],
                          review=review["review"],
                          purchase_date=review["purchase_date"],
                          car_make=review["car_make"],
                          car_model=review["car_model"],
                          car_year=review["car_year"],
                          sentiment=analyze_review_sentiments(review["review"])
                        )
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerReview):
    nlu_url = ""
    api_key = ""
    params = {
        "version": "2021-03-25",
    }
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": dealerReview,
        "features": {"sentiment": {}},
        "return_analyzed_text": True
    }
    print("POST to {} with data: {}".format(nlu_url, data))
    response = requests.post(nlu_url, params=params, headers=headers, auth=HTTPBasicAuth('apikey', api_key), json=data)
    
    print("RESPONSE: ", response.text)
    if response.status_code == 200:
        sentiment_result = response.json()
        sentiment_label = sentiment_result["sentiment"]["document"]["label"]
        return sentiment_label
    else:
        return "Error"



