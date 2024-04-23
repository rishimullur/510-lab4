import requests
from bs4 import BeautifulSoup
import sqlite3
import streamlit as st

def scrape_books():
    base_url = "http://books.toscrape.com/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")

    book_data = {}

    # Find all the book containers
    book_containers = soup.select(".product_pod")

    # Iterate through each book container
    for book in book_containers:
        # Get the link for the book
        book_link = book.select_one("h3 a")["href"]
        book_url = base_url + book_link.replace("../", "")

        # Extract book details from the main page
        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").text
        rating_element = book.select_one(".star-rating")
        rating = rating_element["class"][1]

        # Fetch the book's product page
        # print(book_url)
        book_page = requests.get(book_url)
        book_page_soup = BeautifulSoup(book_page.content, "html.parser")

        # Extract the description from the product page
        description_element = book_page_soup.select_one("#product_description + p")
        if description_element:
            description = description_element.text.strip()
        else:
            description = ""

        # Create a dictionary for the book data
        book_info = {
            "title": title,
            "price": price,
            "rating": rating,
            "description": description
        }

        # Create a unique key for the book using the title and link
        book_key = f"{title}|{book_url}"

        # Add the book data to the dictionary using the unique key
        book_data[book_key] = book_info
        print(book_data)

    return book_data.values()

def create_database(book_data):
    conn = sqlite3.connect("books2.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (title TEXT, price REAL, rating REAL, description TEXT)""")

    for book in book_data:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?)",
                  (book["title"], book["price"], book["rating"], book["description"]))

    conn.commit()
    conn.close()

def query_database(query, params=None):
    conn = sqlite3.connect("books2.db")
    c = conn.cursor()
    if params:
        c.execute(query, params)
    else:
        c.execute(query)
    results = c.fetchall()
    conn.close()
    return results

def main():
    st.title("Book Search")

    # Scrape book data and create database
    book_data = scrape_books()
    create_database(book_data)

    # Search by name or description
    search_term = st.text_input("Search for a book")
    if search_term:
        query = "SELECT * FROM books WHERE title LIKE ? OR description LIKE ?"
        params = (f"%{search_term}%", f"%{search_term}%")
        search_results = query_database(query, params)

        # Store unique book titles
        unique_books = set()
        for book in search_results:
            title = book[0]
            if title not in unique_books:
                unique_books.add(title)
                st.write(f"Title: {book[0]}, Price: {book[1]}, Rating: {book[2]}, Description: {book[3]}")

    # Filter and order by rating or price
    order_by = st.selectbox("Order by", ["Rating", "Price"])
    if order_by == "Rating":
        query = "SELECT * FROM books ORDER BY rating DESC"
    else:
        query = "SELECT * FROM books ORDER BY price DESC"
    order_results = query_database(query)

    for book in order_results:
        st.write(f"Title: {book[0]}, Price: {book[1]}, Rating: {book[2]}, Description: {book[3]}")

if __name__ == "__main__":
    main()
