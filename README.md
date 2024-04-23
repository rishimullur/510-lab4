# 510-lab4
  # Book Search & Weather App - Readme

  ## Use the mode feature to switch funtionality!

  ## Features: 
  1. **Book Search:** Users can search for books by entering a search term. The app will display books matching the search term along with their price and rating. Users can expand each book to view its description.
  2. **Ordering:** Users can order the displayed books by either rating or price.
  3. **Weather App:** Users can access a weather app where they can enter a location and retrieve the current weather forecast.

 .
  ## Steps to Run Locally:
  1. **Clone the Repository:** Clone the repository containing the code for the Book Search App.  ```bash\n   git clone <repository-url>\n   ```
  2. **Navigate to the Directory:** Change your current directory to the cloned repository.  ```bash\n   cd <repository-folder>\n   ```
  3. **Install Dependencies:** Install the required Python packages using pip.   ```bash\n   pip install -r requirements.txt\n   ```
  4. **Set Environment Variables:** Create a `.env` file in the root directory of the project and set the necessary environment variables. For example:   ```\n   DATABASE_URL=your_database_url\n   ```
  5. **Run the App:** Execute the main Python script to run the Book Search App.   ```bash\n   streamlit run app.py\n   ```
