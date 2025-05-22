from flask import Flask, render_template, request
import logging

# Attempt to import scraper modules.
class DummyScraper:
    def __init__(self, scraper_name):
        self.scraper_name = scraper_name

    def search(self, query):
        logging.warning(f"Scraper for {self.scraper_name} not found or failed to import. Returning empty list.")
        return []

try:
    from scrapers import amazon_scraper
except ImportError:
    amazon_scraper = DummyScraper("Amazon.in")
try:
    from scrapers import flipkart_scraper
except ImportError:
    flipkart_scraper = DummyScraper("Flipkart")
try:
    from scrapers import chroma_scraper # Corrected variable name if it was 'croma_scraper' previously in imports
except ImportError:
    chroma_scraper = DummyScraper("Croma")
try:
    from scrapers import reliance_scraper
except ImportError:
    reliance_scraper = DummyScraper("Reliance Digital")
try:
    from scrapers import vijay_sales_scraper
except ImportError:
    vijay_sales_scraper = DummyScraper("Vijay Sales")

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
    Otherwise, it calls scraper functions for Amazon, Flipkart, Croma, 
    Reliance Digital, and Vijay Sales, combines their results, 
    and renders the results.html template.
    Prices are expected to be returned in INR by the scrapers.
    """
    query = request.args.get('query', '').strip() # Get and strip query

    if not query:
        # If query is empty, render results page with a specific error message
        return render_template('results.html', query=query, products=None, error_message="Please enter a product name to search.")

    all_products = []
    error_messages = []

    scrapers_to_run = [
        {"name": "Amazon.in", "instance": amazon_scraper},
        {"name": "Flipkart", "instance": flipkart_scraper},
        {"name": "Croma", "instance": chroma_scraper},
        {"name": "Reliance Digital", "instance": reliance_scraper},
        {"name": "Vijay Sales", "instance": vijay_sales_scraper},
    ]

    for scraper_info in scrapers_to_run:
        try:
            logging.info(f"Searching {scraper_info['name']} for: {query}")
            products = scraper_info['instance'].search(query)
            # Ensure products have the store name, especially if the scraper might forget
            # (though well-behaved scrapers should set this themselves)
            for p in products:
                if 'store' not in p or not p['store']:
                    p['store'] = scraper_info['name']
            all_products.extend(products)
            logging.info(f"Found {len(products)} products on {scraper_info['name']}.")
        except Exception as e:
            logging.error(f"Error scraping {scraper_info['name']}: {e}", exc_info=True)
            error_messages.append(f"Could not retrieve results from {scraper_info['name']}.")

    final_error_message = None
    if error_messages and not all_products:
        # Consolidate error messages if all scrapers failed
        final_error_message = "Could not retrieve results from any shopping sites. Please try again later. Details: " + " ".join(error_messages)
    elif error_messages:
        # Log warnings if some scrapers failed but others succeeded
        logging.warning("Partial success in scraping: " + " ".join(error_messages))
        # Optionally, you could pass these partial error messages to the template if needed
        # For now, we only show a major error if ALL fail and NO products are found.

    # Security: Ensure query is properly escaped by Jinja2 by default in template.
    # No direct HTML construction with query here.
    return render_template('results.html', query=query, products=all_products, error_message=final_error_message)

if __name__ == '__main__':
    # FLASK_DEBUG environment variable is respected by app.config['DEBUG']
    # Default to False if not set, which is safer for accidental production runs.
    is_debug_mode = app.config.get('DEBUG', False) 
    app.run(debug=is_debug_mode, host='0.0.0.0', port=9000)
