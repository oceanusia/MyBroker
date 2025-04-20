# Streamlit Application

This is a simple Streamlit application that demonstrates the capabilities of the Streamlit library for building interactive web applications in Python.

## Project Structure

```
streamlit-app
├── mybroker.py             # Root folder for Streamlit app
├── app_functions/          # All page‑specific modules
│   ├── __init__.py         # (optional) makes this a Python package
│   ├── verify_email.py     # Email verification page logic
│   ├── create_account.py   # Account creation page logic
│   ├── login_page.py       # Login page logic
│   ├── post_listing.py     # “Post a Listing” page
│   ├── browse_listings.py  # “Browse Listings” page
│   ├── saved_listings.py   # “Saved Listings” page
│   ├── my_listings.py      # “My Listings” page
│   ├── landing_page.py     # Landing (pre‑login) page
│   └── logout.py           # Logout handler
```

## Installation

To run this application, you need to have Python installed on your machine. Follow these steps to set up the project:

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the Streamlit application, run the following command in your terminal:

```
streamlit run app.py
```

This will open the application in your default web browser.

## Features

- Interactive widgets for user input
- Dynamic data visualization
- User-friendly layout

## License

This project is licensed under the MIT License - see the LICENSE file for details.
