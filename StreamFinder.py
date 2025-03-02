import requests  # Import the requests library to make HTTP requests
import streamlit as st  # Import the streamlit library for creating web apps

st.title("StreamFinder")  # Set the title of the Streamlit app

def show_query(title):
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
        
        # Check if the response was successful
        if response.status_code != 200:
            st.error("😕 We couldn't connect to the movie database. Please try again later.")
            return None
            
        # Parse the response JSON data
        data = response.json()
    
        return data  # Return just the result array
    
    except requests.exceptions.ConnectionError:
        st.error("📶 Internet connection issue. Please check your connection and try again.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ The request timed out. The movie database might be busy. Please try again.")
        return None
    except Exception as e:
        st.error("🎬 Something went wrong while searching for movies. Please try again.")
        return None  # Return None if an error occurs

def movie_title(data):
    try:
        if not data or len(data) == 0:
            st.info("🔎 We couldn't find any movies matching your search. Please try a different title.")
            return None
            
        
        # Create buttons for each movie
        movieTitle = None
        for i, movie in enumerate(data):
            title = movie.get("title")
            year = movie.get("releaseYear")
            
            # Create a unique key for each button
            if st.button(f"{title} ({year})", key=f"title_{i}"):
                movieTitle = title
                
        return movieTitle
    except Exception as e:
        st.error("🎞️ There was a problem displaying the movie options. Please try your search again.")
        return None
        
def movieSearch(data, movieTitle):
    try:
        for movie in data:
            if movie.get("title") == movieTitle:
                return movie
                
        st.warning(f"🎭 We couldn't find details for '{movieTitle}'. Please try another selection.")
        return None
    except Exception as e:
        st.error("🎬 Something went wrong while retrieving movie details. Please try again.")
        return None

def display_movie_details(movie):
    try:
        # Get movie details with fallbacks for missing data
        title = movie.get("title", "Unknown Title")
        
        # Safely get director information
        directors = movie.get("directors", [])
        director = directors[0] if directors and len(directors) > 0 else "Unknown Director"
        
        overView = movie.get("overview", "No overview available")
        
        # Safely get cast information
        cast = movie.get("cast", [])
        
        relesed_year = movie.get("releaseYear", "Unknown")
        rating = movie.get("rating", "Not rated")
        
        # Safely get image URL
        images = None
        if "imageSet" in movie and "horizontalPoster" in movie["imageSet"]:
            images = movie["imageSet"]["horizontalPoster"].get("w1440")

        # Display the movie details using Streamlit
        if images:
            try:
                st.image(images)
            except Exception:
                st.info("🖼️ Could not load movie poster image")
        
        st.title(title)
        st.subheader(f"Directed by: {director}")
        
        # Movie details
        col1, col2 = st.columns(2)
        col1.write(f"**Released Year:** {relesed_year}")
        col2.write(f"**Rating:** {rating}/100")
        
        # Overview
        st.subheader("Overview")
        st.write(overView)
        
        # Cast
        if cast:
            st.subheader("Cast")
            st.write(", ".join(cast))

        # Streaming options
        streaming_available = False
        try:
            if "streamingOptions" in movie and "in" in movie["streamingOptions"]:
                streaming_options = movie["streamingOptions"]["in"]
                if streaming_options and len(streaming_options) > 0:
                    
                    for option in streaming_options:
                        streaming_type = option.get('type', 'Unknown')
                        link = option.get("link")
                        
                        if streaming_type in ["subscription", "buy", "rent"] and link:
                            service = option.get("service", "streaming service")
                            st.link_button(f"Watch", link)
                            streaming_available = True
                            break
            
            if not streaming_available:
                st.info("🎬 No streaming options available for this movie in your region")
        except Exception:
            st.info("🎞️ Could not retrieve streaming options at this time")
            
    except Exception:
        st.error("🎬 We encountered a problem showing movie details. Please try again.")

# State management
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'movie_data' not in st.session_state:
    st.session_state.movie_data = None

# Main function
def main():
    title = st.text_input("Enter the title of the movie:", key="search_input")
    search_button = st.button("Search", key="search_button")
    
    if search_button and title:
        # Clear previous selection
        st.session_state.selected_movie = None
        
        with st.spinner("Searching for movies..."):
            data = show_query(title)
            st.session_state.movie_data = data
            
        if st.session_state.movie_data:
            if len(st.session_state.movie_data) == 0:
                st.info("🔍 No movies found matching your search. Please try a different title.")
        else:
            st.error("🎬 Unable to connect to movie database. Please try again later.")
    
    # If we have movie data but no selection yet, show selection options
    if st.session_state.movie_data and not st.session_state.selected_movie:
        selected_title = movie_title(st.session_state.movie_data)
        if selected_title:
            st.session_state.selected_movie = movieSearch(st.session_state.movie_data, selected_title)
            # Force a rerun to update the UI
            st.rerun()
    
    # If we have a selected movie, display its details
    if st.session_state.selected_movie:
        display_movie_details(st.session_state.selected_movie)
        
        # Add a button to go back to search results
        if st.button("Back to search results"):
            st.session_state.selected_movie = None
            st.rerun()
    
    # Show welcome message if nothing has been searched yet
    if not st.session_state.movie_data and not search_button:
        st.write("Get details of any movie in one click.")

if __name__ == "__main__":
    main()