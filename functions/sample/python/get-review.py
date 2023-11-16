from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

def main(params):
    try:
        # Initialize Cloudant client
        client = Cloudant.iam(
            account_name=params["COUCH_USERNAME"],
            api_key=params["IAM_API_KEY"],
            connect=True
        )
        client.connect()

        # Access the specified database
        dbname = params['dbname']
        database = client[dbname]

        # Build selector based on parameters
        selector = {}
        if 'dealerId' in params:
            selector['dealership'] = int(params['dealerId'])

        # Execute a query based on the selector
        query_result = database.get_query_result(selector)

        # Extract documents from query result
        documents = [doc for doc in query_result]

        return {"body": documents}

    except CloudantException as e:
        return {"error": str(e)}
    except (requests.exceptions.RequestException, ConnectionResetError) as e:
        return {"error": str(e)}
