import requests  # Import the requests library to make HTTP requests

def map_query():
    # Define the query parameters for the API request
    querystring = {"query":"america newyork restaurant"}
    
    # Define the URL for the API endpoint
    url = "https://google-map-scraper1.p.rapidapi.com/api/places/search"
    
    # Define the headers, including the API key and host
    headers = {
        "x-rapidapi-key": "e448bfa06emsh9053d11a8be63ddp188ae7jsnf440b6eadba1",
        "x-rapidapi-host": "google-map-scraper1.p.rapidapi.com"
    }
    
    # Make the GET request to the API
    response = requests.get(url, headers=headers)
    
    # Parse the response JSON data
    data = response.json()
    
    # Check if the response status code is not 200 (OK)
    if response.status_code != 200:
        print("API not working.")  # Print an error message if the API is not working
        return None  # Return None if the API request failed

    return data  # Return the parsed data if the API request was successful

# Call the map_query function and store the result in the map variable
map = map_query()

# Print the result of the API request
print(map)

