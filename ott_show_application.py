import requests  # Import the requests library to make HTTP requests
import streamlit as st  # Import the streamlit library for creating web apps

st.title("Movie Radar")  # Set the title of the Streamlit app

def show_query():
    title = st.text_input("Enter the title of the movie: ")  # Prompt the user to enter the title of the movie
    try:
        # Define the query parameters for the API request
        querystring = {"country": "in", "title": title, "series_granularity": "show", "show_type": "movie", "output_language": "en"}
        
        # Define the URL for the API endpoint
        url = "https://streaming-availability.p.rapidapi.com/shows/search/title"
        
        # Define the headers, including the API key and host
        headers = {
            "x-rapidapi-key": "e448bfa06emsh9053d11a8be63ddp188ae7jsnf440b6eadba1",
            "x-rapidapi-host": "streaming-availability.p.rapidapi.com"
        }
        
        # Make the GET request to the API
        response = requests.get(url, headers=headers, params=querystring)
        
        # Parse the response JSON data
        data = response.json()

        # Extract relevant information from the response data
        title = data[0].get("title")
        director = data[0]["directors"][0]
        overView = data[0].get("overview")
        cast = data[0]["cast"]
        relesed_year = data[0].get("releaseYear")
        rating = data[0].get("rating")
        images = data[0]["imageSet"]["horizontalPoster"].get("w1440")

        # Initialize streaming_options to "Not Available"
        streaming_options = "Not Available"
        
        # Loop through the streaming options to find the appropriate link
        for i in range(len(data[0]["streamingOptions"]["in"])):
            streaming_type = data[0]["streamingOptions"]["in"][i].get('type')
            
            if streaming_type in ["subscription", "buy", "rent"]:
                streaming_options = data[0]["streamingOptions"]["in"][i].get("link")
                break  # Exit the loop once a valid streaming option is found

        return title, director, overView, relesed_year, rating, images, streaming_options,cast

    except Exception as e:
        print(e)  # Print the exception if an error occurs
        return None  # Return None if an error occurs

# Call the show_query function and store the result in the movie variable
movie = show_query()

# Check if the movie variable is not None before accessing its elements
if movie:
    # Display the movie details using Streamlit
    st.title(f"{movie[0]}")
    st.write(f"Directed by : {movie[1]}")
    st.write(f"Overview: {movie[2]}")
    st.write(f"Cast: {movie[7]}")
    st.write(f"Released Year: {movie[3]}")
    st.write(f"Rating: {movie[4]}")
    if movie[6] == "Not Available":
        None  # Do nothing if the streaming option is not available
    else:
        st.link_button("Watch", movie[5])  # Display a button to watch the movie if the link is available
    st.image(movie[5])
else:
    st.write("Get details of any movie in one click.")  # Display an error message if no movie is found