# 510-lab4
  # Book Search App - Readme\n\n
  
  ## Features:\n\n
  1. **Book Search:** Users can search for books by entering a search term. The app will display books matching the search term along with their price and rating. Users can expand each book to view its description.\n
  2. **Ordering:** Users can order the displayed books by either rating or price.\n
  3. **Weather App:** Users can access a weather app where they can enter a location and retrieve the current weather forecast.\n\n
  ## Steps to Run Locally:\n\n
  1. **Clone the Repository:** Clone the repository containing the code for the Book Search App.\n   ```bash\n   git clone <repository-url>\n   ```\n\n
  2. **Navigate to the Directory:** Change your current directory to the cloned repository.\n   ```bash\n   cd <repository-folder>\n   ```\n\n
  3. **Install Dependencies:** Install the required Python packages using pip.\n   ```bash\n   pip install -r requirements.txt\n   ```\n\n
  4. **Set Environment Variables:** Create a `.env` file in the root directory of the project and set the necessary environment variables. For example:\n   ```\n   DATABASE_URL=your_database_url\n   ```\n\n
  5. **Run the App:** Execute the main Python script to run the Book Search App.\n   ```bash\n   streamlit run app.py\n   ```\n
