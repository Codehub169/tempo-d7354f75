from flask import Flask, render_template, request
import logging

# Attempt to import scraper modules.
# These files (scrapers/amazon_scraper.py, scrapers/flipkart_scraper.py)
# will contain the actual web scraping logic.
try:
    from scrapers import amazon_scraper, flipkart_scraper
    SCRAPERS_AVAILABLE = True
except ImportError:
    SCRAPERS_AVAILABLE = False
    # Provide a fallback or log a warning if scrapers are not found/implemented
    class DummyScraper:
        def __init__(self, scraper_name):
            self.scraper_name = scraper_name

        def search(self, query):
            logging.warning(f"Scraper for {self.scraper_name} not found or failed to import. Returning empty list.")
            return []
    amazon_scraper = DummyScraper("Amazon")
    flipkart_scraper = DummyScraper("Flipkart")

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the route for the home page
@app.route('/')
def home():
    """
    Renders the home page.
    """
    return render_template('home.html')

# Define the route for search results
@app.route('/search')
def search():
    """
    Handles product search requests.
    Retrieves the search query from the URL parameters (GET request).
    If the query is empty, it renders the results page with an error message.
    Otherwise, it calls scraper functions for Amazon and Flipkart,
    combines their results, and renders the results.html template.
    Prices are expected to be returned in INR by the scrapers.
    """
    query = request.args.get('query', '').strip() # Get and strip query

    if not query:
        # If query is empty, render results page with a specific error message
        return render_template('results.html', query=query, products=None, error_message="Please enter a product name to search.")

    all_products = []
    error_messages = []

    # Call Amazon scraper
    try:
        logging.info(f"Searching Amazon for: {query}")
        amazon_products = amazon_scraper.search(query)
        all_products.extend(amazon_products)
        logging.info(f"Found {len(amazon_products)} products on Amazon.")
    except Exception as e:
        logging.error(f"Error scraping Amazon: {e}", exc_info=True)
        error_messages.append(f"Could not retrieve results from Amazon.") # User-friendly message

    # Call Flipkart scraper
    try:
        logging.info(f"Searching Flipkart for: {query}")
        flipkart_products = flipkart_scraper.search(query)
        all_products.extend(flipkart_products)
        logging.info(f"Found {len(flipkart_products)} products on Flipkart.")
    except Exception as e:
        logging.error(f"Error scraping Flipkart: {e}", exc_info=True)
        error_messages.append(f"Could not retrieve results from Flipkart.") # User-friendly message

    # In a real application, you might want to sort or filter `all_products`
    # e.g., by price, relevance, etc.
    # For now, we just combine them.

    final_error_message = None
    if error_messages and not all_products:
        final_error_message = "Could not retrieve results from one or more shopping sites. Please try again later. Details: " + " ".join(error_messages)
    elif error_messages:
        # Optionally, inform user about partial success if some products were found
        logging.warning("Partial success in scraping: " + " ".join(error_messages))
        # Potentially pass a non-critical message to the template if desired for partial failures

    return render_template('results.html', query=query, products=all_products, error_message=final_error_message)

if __name__ == '__main__':
    # When running with `python app.py`, debug should ideally be False if FLASK_ENV is production
    # However, for direct execution, debug=True is common for development.
    # The startup.sh script uses `flask run` which respects FLASK_ENV.
    is_debug_mode = app.config.get('DEBUG', False) # Respect FLASK_DEBUG or FLASK_ENV=development
    app.run(debug=is_debug_mode, host='0.0.0.0', port=9000)
