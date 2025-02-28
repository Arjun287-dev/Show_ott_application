import requests  # Import the requests library to make HTTP requests




def show_query():
    title = input(str("Enter the title of the movie: "))  # Prompt the user to enter the title of the movie
    try:
    # Define the query parameters for the API request
        querystring = {f"country":"in","title":{title},"series_granularity":"show","show_type":"movie","output_language":"en"}
        
        # Define the URL for the API endpoint
        url = "https://streaming-availability.p.rapidapi.com/shows/search/title"
        
        # Define the headers, including the API key and host
        headers = {
            "x-rapidapi-key": "e448bfa06emsh9053d11a8be63ddp188ae7jsnf440b6eadba1",
            "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
        }
        
        # Make the GET request to the API
        response = requests.get(url, headers=headers,params=querystring)
        
        # Parse the response JSON data
        data = response.json()

        title = data[0].get("title")
        overView = data[0].get("overview")
        relesed_year = data[0].get("releaseYear")
        rating = data[0].get("rating")
        images = data[0]["imageSet"]["horizontalPoster"].get("w1440")

        for i in range(len(data[0]["streamingOptions"]["in"])):
            streaming_type = data[0]["streamingOptions"]["in"][i].get('type')
            if streaming_type == "subscription":
                streaming_options = data[0]["streamingOptions"]["in"][i].get("link")
            else:
                streaming_options = "Not Available"
        return title,overView,relesed_year,rating,images,streaming_options

    except Exception as e:
        print (e)

# Call the map_query function and store the result in the map variable
movie = show_query()

# Print the result of the API request
print(movie)

