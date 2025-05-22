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

# Configure logging for this module if used standalone
# In a larger application, logging might be configured centrally
logger = logging.getLogger(__name__)

def search(query):
    """
    Scrapes Flipkart for products based on the query.
    Returns a list of product dictionaries, with prices in INR.
    This is a placeholder and will need significant work to be robust.
    Flipkart's structure changes frequently, and they have anti-scraping measures.
    """
    products = []
    # URL encode the query string for safety and correctness
    search_url = f"https://www.flipkart.com/search?q={requests.utils.quote(query)}"

    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10) # 10 seconds timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- Placeholder: Flipkart scraping logic --- 
        # This is highly dependent on Flipkart's current HTML structure.
        # The selectors below are examples and WILL LIKELY BREAK.
        # You need to inspect Flipkart's search results page to find the correct selectors.
        # Common product container selectors: '_1AtVbE', 'div._2kHMtA', 'div._4ddWXP', 'div._1xHGtK._373qXS'
        # Name selector: 'div._4rR01T', 'a.s1Q9rs', 'a.IRpwTa'
        # Price selector: 'div._30jeq3'
        # URL selector: 'a._1fQZEK', 'a.s1Q9rs', 'a.IRpwTa', 'a._2Uzu6v'
        # Image selector: 'img._396cs4', 'img._2r_T1I'

        # Example (very simplified and likely to fail or be inaccurate):
        # Limiting product count to avoid excessive scraping during tests/development
        product_limit = 5
        
        # Attempting a common structure often seen (may need adjustment)
        # Note: Flipkart's classes can be very dynamic (_1xHGtK _373qXS, _2kHMtA, _4ddWXP etc.)
        # The following selectors are illustrative and likely need frequent updates.
        for item in soup.select('div._1xHGtK._373qXS, div._2kHMtA, div._4ddWXP'): 
            name_element = item.select_one('a.IRpwTa, div._4rR01T, a.s1Q9rs')
            price_element = item.select_one('div._30jeq3')
            # URL is often on the same anchor as the name or a dedicated link element
            url_element = item.select_one('a.IRpwTa, a._2Uzu6v, a._1fQZEK, a.s1Q9rs') 
            image_element = item.select_one('img._2r_T1I, img._396cs4')

            if name_element and price_element and url_element:
                name = name_element.get_text(strip=True)
                
                price_str_raw = price_element.get_text(strip=True)
                # Clean price: remove currency symbol (₹), commas, and extraneous characters
                # Ensure it's a numeric value before formatting.
                cleaned_price_str = ''.join(filter(str.isdigit, price_str_raw.split('.')[0])) # Take integer part before decimal
                if cleaned_price_str:
                    price = f"\u20b9{cleaned_price_str}" # \u20b9 is the INR symbol
                else:
                    logger.warning(f"Could not parse price for product: {name} from '{price_str_raw}'")
                    continue # Skip product if price cannot be parsed

                product_url_path = url_element.get('href')
                if product_url_path:
                    if product_url_path.startswith('http'):
                        url = product_url_path
                    elif product_url_path.startswith('/'):
                        url = "https://www.flipkart.com" + product_url_path
                    else:
                        url = "https://www.flipkart.com/" + product_url_path # Fallback for unexpected relative URLs
                else:
                    url = "#" # Fallback URL if href is missing
                
                image_url = image_element.get('src') if image_element else None
                if image_url and image_url.startswith('//'): # Handle protocol-relative URLs
                    image_url = 'https:' + image_url

                products.append({
                    "name": name,
                    "store": "Flipkart",
                    "price": price,
                    "url": url,
                    "image_url": image_url
                })
                if len(products) >= product_limit:
                    break
            # else: # Optionally log if essential elements are missing for a potential item
                # logger.debug(f"Skipping item, missing one or more elements: Name:{bool(name_element)}, Price:{bool(price_element)}, URL:{bool(url_element)}")

        # --- End Placeholder --- 

    except requests.exceptions.Timeout:
        logger.error(f"Timeout during Flipkart request for query: {query}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {e.response.status_code} during Flipkart request for query: {query}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error during Flipkart request: {e} for query: {query}")
    except Exception as e:
        logger.error(f"Error parsing Flipkart results: {e} for query: {query}", exc_info=True)

    if not products:
        logger.info(f"No products found on Flipkart for query: '{query}'. Scraper might need an update.")

    return products

# Example usage (for testing this module directly):
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    test_query = "gaming laptop"
    logger.info(f"Testing Flipkart scraper with query: '{test_query}'")
    results = search(test_query)
    if results:
        logger.info(f"Found {len(results)} products:")
        for i, product in enumerate(results):
            print(f"  Product {i+1}:")
            print(f"    Name: {product['name']}")
            print(f"    Price: {product['price']}")
            print(f"    URL: {product['url']}")
            print(f"    Image URL: {product['image_url']}")
    else:
        logger.warning(f"No products found for '{test_query}' on Flipkart or scraper needs update.")
