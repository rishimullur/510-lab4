import requests
from bs4 import BeautifulSoup
import sqlite3
import streamlit as st

def scrape_books():
    url = "http://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # TODO:Extract book data from the HTML using BeautifulSoup


    return book_data

def create_database(book_data):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS books
                 (title TEXT, price REAL, rating REAL, description TEXT)""")

    for book in book_data:
        c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", book)

    conn.commit()
    conn.close()

def query_database(query):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

def main():
    st.title("Book Search")

    # Scrape book data and create database
    book_data = scrape_books()
    create_database(book_data)

    # Search by name or description
    search_term = st.text_input("Search for a book")
    if search_term:
        query = f"SELECT * FROM books WHERE title LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"
        results = query_database(query)
        for book in results:
            st.write(f"Title: {book[0]}, Price: {book[1]}, Rating: {book[2]}, Description: {book[3]}")

    # Filter and order by rating or price
    order_by = st.selectbox("Order by", ["Rating", "Price"])
    if order_by == "Rating":
        query = "SELECT * FROM books ORDER BY rating DESC"
    else:
        query = "SELECT * FROM books ORDER BY price DESC"
    results = query_database(query)
    for book in results:
        st.write(f"Title: {book[0]}, Price: {book[1]}, Rating: {book[2]}, Description: {book[3]}")

if __name__ == "__main__":
    main()
