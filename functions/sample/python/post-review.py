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

        # Access the specified database
        dbname = params['dbname']
        database = client[dbname]

        # Assuming the review data is passed in params['review']
        # Validate or transform review data as necessary
        review_data = params['review']

        # Insert the review into the database
        document = database.create_document(review_data)

        # Check if the document exists in the database
        if document.exists():
            return {"body": "Review added successfully"}
        else:
            return {"error": "Failed to add review"}

    except CloudantException as e:
        return {"error": str(e)}
    except (requests.exceptions.RequestException, ConnectionResetError) as e:
        return {"error": str(e)}
