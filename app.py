import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import psycopg2
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Function to geocode location using OpenStreetMap API
def geocode_location(location):
    url = f"http://nominatim.openstreetmap.org/search?q={location}&format=json"
    print(url)
    response = requests.get(url)
    data = response.json()
    if data:
        # Extract latitude and longitude from the response
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    else:
        return None, None

# Function to retrieve weather data using weather.gov API
def get_weather(lon, lat):
    url = f"https://api.weather.gov/points/{lat},{lon}/forecast"
    response = requests.get(url)
    data = response.json()
    if "properties" in data:
        return data["properties"]["periods"][0]["detailedForecast"]
    else:
        return None

def weather_app():
    st.title("Weather App")
    location = st.text_input("Enter Location Name")
    if st.button("Get Weather"):
        lon, lat = geocode_location(location)
        if lon is not None and lat is not None:
            weather = get_weather(lon, lat)
            if weather:
                st.write("Weather Forecast:")
                st.write(weather)
            else:
                st.write("Weather data not available")
        else:
            st.write("Invalid location")

# Function to establish connection to PostgreSQL database
def connect_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

def scrape_books():
    base_url = "https://books.toscrape.com/catalogue/"
    book_data = {}

    for page_number in range(1, 2):  # Loop through pages 1 to 50
        page_url = f"{base_url}page-{page_number}.html"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        book_containers = soup.select(".product_pod")

        for book in book_containers:
            book_link = book.select_one("h3 a")["href"]
            book_url = base_url + book_link.replace("../", "")

            title = book.select_one("h3 a")["title"]
            price_text = book.select_one(".price_color").text

            # Extracting numeric part from price text
            price = float(price_text.replace("£", ""))

            rating_element = book.select_one(".star-rating")
            rating_text = rating_element["class"][1]
            rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating = rating_mapping.get(rating_text, None)

            book_page = requests.get(book_url)
            book_page_soup = BeautifulSoup(book_page.content, "html.parser")

            description_element = book_page_soup.select_one("#product_description + p")
            if description_element:
                description = description_element.text.strip()
            else:
                description = ""

            book_info = {
                "title": title,
                "price": price,
                "rating": rating,
                "description": description
            }

            book_key = f"{title}|{book_url}"
            book_data[book_key] = book_info

    return book_data.values()

def create_database(book_data):
    conn = connect_db()
    c = conn.cursor()

    # Drop existing books table if it exists
    c.execute("DROP TABLE IF EXISTS books")

    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (title TEXT, price REAL, rating REAL, description TEXT)""")

    for book in book_data:
        c.execute("INSERT INTO books VALUES (%s, %s, %s, %s)",
                  (book["title"], book["price"], book["rating"], book["description"]))

    conn.commit()
    conn.close()

def query_database(query, params=None):
    conn = connect_db()
    c = conn.cursor()
    if params:
        c.execute(query, params)
    else:
        c.execute(query)
    results = c.fetchall()
    conn.close()
    return results

def main():
    app_mode = st.sidebar.selectbox("Choose the App Mode", ["Book Search", "Weather App"])

    if app_mode == "Book Search":
        st.title("Book Search")
    

        book_data = scrape_books()
        create_database(book_data)

        search_term = st.text_input("Search for a book")
        if search_term:
            query = "SELECT * FROM books WHERE title LIKE %s OR description LIKE %s"
            params = (f"%{search_term}%", f"%{search_term}%")
            search_results = query_database(query, params)

            unique_books = {}
            for book in search_results:
                title = book[0]
                if title not in unique_books:
                    unique_books[title] = book

            count = 0
            for title, book in unique_books.items():
                with st.expander(title):
                    st.write(f"Price: {book[1]}, Rating: {book[2]}")
                    if st.button("Show description", key=count):
                        st.write(book[3])
                count += 1

        order_by = st.selectbox("Order by", ["Rating", "Price"])
        if order_by == "Rating":
            query = "SELECT * FROM books ORDER BY rating DESC"
        else:
            query = "SELECT * FROM books ORDER BY price DESC"
        order_results = query_database(query)

        unique_books = {}
        for book in order_results:
            title = book[0]
            if title not in unique_books:
                unique_books[title] = book

        for title, book in unique_books.items():
            with st.expander(title):
                st.write(f"Price: {book[1]}, Rating: {book[2]}")
                if st.button("Show description", key=title):
                    st.write(book[3])

    elif app_mode == "Weather App":
        weather_app()

if __name__ == "__main__":
    main()

