import requests
import time
from datetime import datetime, timedelta, timezone
from dev_env.setup_files.logging.logger import logger

def run_bsp_bau_tasks():
    """ 
    1) Monitor health endpoints: call each microservices /health endpoint 
    and append to actions list if any are marked as DOWN. 

    Example of data to work with:

    2) Warn if expiration dates for certificates are upcoming (within a month), 
    or show an error if they have been exceeded. Add an action in both cases to 
    the actions list to print out at the end of the script

    Example to work with: input file json, where dates need to be changed manually for now

    3) Check stale envelopes in blob router - this should always be empty. In the case it isn't, 
    add an action to the list

    4) Stale envelopes in processor - should be empty, if not then do a PUT request to make 
    the envelope reprocess itself as an exception record so that a caseworker can investigate further

    5) Stale letters in bulk print - depending on the state, call abort or complete
    
    """
    # Prompt the user for the Authorization token and set headers
    headers = {"Authorization": input("Enter your Authorization token (Bearer token): ")}


    handle_stale_letters(headers)
    # reprocess_stale_envelopes()

def handle_stale_letters(headers: dict):
    # Fetch the JSON data from the URL
    url = "http://rpe-send-letter-service-prod.service.core-compute-prod.internal/stale-letters"
    
    # Fetching the data for bulk print sometimes gives a 502 for some reason, so retry a few times
    response = fetch_data_with_retries(url)
    data = response['stale_letters']

    # Calculate the date one week ago from the current date
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

    # Iterate through the "stale_letters" list
    for letter in data:
        created_at_str = letter["created_at"].replace("Z", "+00:00")  # Replace "Z" with "+00:00" for parsing
        created_at = datetime.fromisoformat(created_at_str)
        letter_id = letter["id"]
        action = "empty"

        if created_at < one_week_ago or letter['status'] == 'Uploaded':
            # If created_at is more than a week old, or it has already been uploaded then mark as aborted
            action = "mark-aborted"
            mark_url = f"http://rpe-send-letter-service-prod.service.core-compute-prod.internal/letters/{letter_id}/mark-aborted"
        else:
            # If created_at is less than a week old and the status is not Uploaded, mark as created
            action = "mark-created"
            mark_url = f"http://rpe-send-letter-service-prod.service.core-compute-prod.internal/letters/{letter_id}/mark-created"

        # Make the HTTP request to mark the letter
        response = requests.put(mark_url, data={}, headers=headers)

        if response.status_code == 200:
            print(f"Letter with ID {letter_id} marked successfully: {action}.")
        else:
            print(f"Failed to mark letter with ID {letter_id}. Status code: {response.status_code}")

def reprocess_stale_envelopes():
    # Define the base URL of the GET endpoint to retrieve initial data
    initial_data_url = "http://bulk-scan-processor-prod.service.core-compute-prod.internal/envelopes/stale-incomplete-envelopes"

    # Define the base URL of the PUT endpoint
    base_url = "http://bulk-scan-processor-prod.service.core-compute-prod.internal/actions/reprocess/"

    # Make a GET request to fetch the initial data
    response = fetch_data_with_retries(initial_data_url)

    # Check if the GET request was successful (HTTP status code 200)
    if response.status_code == 200:
        json_data = response.json()
        # Extract envelope data
        envelope_data = json_data["data"]

        # Prompt the user for the Authorization token and set headers
        headers = {"Authorization": input("Enter your Authorization token (Bearer token): ")}

        # Iterate over each envelope data
        for entry in envelope_data:
            envelope_id = entry["envelope_id"]
            container = entry["container"]
            file_name = entry["file_name"]
            
            # Construct the URL for the specific envelope ID
            url = base_url + envelope_id

            # Make the PUT request with the Authorization header
            put_response = requests.put(url, json={}, headers=headers)

            # Check if the PUT request was successful (HTTP status code 200)
            if put_response.status_code == 200:
                logger.info(f"PUT request successful for envelope ID: {envelope_id}")
                
                # Construct the new URL
                new_url = f"http://bulk-scan-processor-prod.service.core-compute-prod.internal/envelopes/{container}/{file_name}"
                logger.info(new_url)

                # Initialize a timer
                start_time = time.time()
                timeout = 20  # 20 seconds timeout

                while True:
                    # Make a GET request to the new URL
                    response = requests.get(new_url)

                    # Check if the GET request was successful (HTTP status code 200)
                    if response.status_code == 200:
                        response_data = response.json()
                        ccd_id = response_data.get("ccd_id")
                        if ccd_id is not None:
                            logger.info(f"ccd_id is populated: {ccd_id}")
                            break  # Exit the loop if ccd_id is populated

                    # Check if the timeout has been reached
                    if time.time() - start_time > timeout:
                        logger.info("Timeout reached. ccd_id is not populated.")
                        break
                    time.sleep(1)  # Wait for 1 second before checking again
            else:
                logger.error(f"PUT request failed for envelope ID: {envelope_id} "
                             f"with zip file: {file_name} and container: {container}")
                logger.error(f"Response status code: {put_response.status_code}")
                logger.error(f"Response content: {put_response.text}")
    else:
        logger.error(f"GET request failed with status code: {response.status_code}")
        logger.error(f"Response content: {response.text}")

# Function to fetch data with retries
def fetch_data_with_retries(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            retries += 1
            print(f"Failed to fetch data (Attempt {retries}/{max_retries}). Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed to fetch data after multiple retries.")
