import requests
from bs4 import BeautifulSoup
import logging

# It's good practice to use a User-Agent that mimics a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1' # Do Not Track Request Header
}

def search(query):
    """
    Scrapes Amazon.in for products based on the query.
    Returns a list of product dictionaries, with prices in INR.
    This is a placeholder and will need significant work to be robust.
    Amazon's structure changes frequently, and they have anti-scraping measures.
    """
    products = []
    # URL encode the query string for safety and correctness
    search_url = f"https://www.amazon.in/s?k={requests.utils.quote(query)}"
    
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10) # 10 seconds timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Placeholder: Amazon scraping logic --- 
        # This is highly dependent on Amazon's current HTML structure.
        # The selectors below are examples and WILL LIKELY BREAK.
        # You need to inspect Amazon's search results page to find the correct selectors.
        # Common product container selectors: 'div[data-component-type="s-search-result"]'
        # Name selector: 'span.a-text-normal'
        # Price selector: 'span.a-price-whole'
        # URL selector: 'a.a-link-normal'
        # Image selector: 'img.s-image'

        # Example (very simplified and likely to fail or be inaccurate):
        # Limiting product count to avoid excessive scraping during tests/development
        product_limit = 5 
        for item in soup.select('div[data-asin]'): # A common attribute for product items
            if not item.select_one('.a-price-whole'): # Skip items without a price (e.g., ads, accessories)
                continue

            name_element = item.select_one('h2 .a-link-normal span.a-text-normal')
            price_element = item.select_one('.a-price-whole')
            url_element = item.select_one('h2 .a-link-normal')
            image_element = item.select_one('.s-image')

            if name_element and price_element and url_element:
                name = name_element.get_text(strip=True)
                # Price needs careful parsing to get a number and format as INR
                price_str = price_element.get_text(strip=True).replace(',', '')
                # Ensure price is prefixed with ₹ (INR symbol)
                price = f"₹{price_str}" 
                
                product_url_path = url_element.get('href')
                if product_url_path:
                    url = "https://www.amazon.in" + product_url_path if product_url_path.startswith('/') else product_url_path
                else:
                    url = "#" # Fallback URL
                
                image_url = image_element.get('src') if image_element else None

                # Filter out sponsored products if possible/needed by checking for specific text or attributes
                # For example: if item.select_one('span.s-sponsored-label-text'): continue

                products.append({
                    "name": name,
                    "store": "Amazon.in",
                    "price": price,
                    "url": url,
                    "image_url": image_url
                })
                if len(products) >= product_limit:
                    break 
        # --- End Placeholder --- 

    except requests.exceptions.Timeout:
        logging.error(f"Timeout during Amazon request for query: {query}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error during Amazon request: {e.status_code} for query: {query}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during Amazon request: {e} for query: {query}")
    except Exception as e:
        logging.error(f"Error parsing Amazon results: {e} for query: {query}", exc_info=True)
        # In a real app, log this error more robustly

    return products

# Example usage (for testing this module directly):
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    test_query = "laptop"
    results = search(test_query)
    if results:
        for product in results:
            print(product)
    else:
        print(f"No products found for '{test_query}' on Amazon.in or scraper needs update.")
