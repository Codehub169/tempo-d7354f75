from flask import Flask, render_template, request

# Initialize Flask application
app = Flask(__name__)

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
    Otherwise, it simulates a product search with dummy data based on keywords
    and renders the results.html template with the query and product list.
    """
    query = request.args.get('query', '').strip() # Get and strip query

    if not query:
        # If query is empty, render results page with a specific error message
        return render_template('results.html', query=query, products=None, error_message="Please enter a product name to search.")

    # Placeholder for actual search logic - using dummy data.
    # In a real application, this is where you'd call scraping/API functions.
    dummy_products = []
    query_lower = query.lower()

    # Simplified and more inclusive keyword matching for dummy data
    if "smart tv" in query_lower or "tv" in query_lower:
        dummy_products = [
            {
                "name": "Samsung 55-inch QLED 4K Smart TV",
                "store": "Best Buy",
                "price": "$799.99",
                "url": "https://www.example.com/samsung-tv",
                "image_url": "https://images.unsplash.com/photo-1593784915907-9ee00f08500a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            },
            {
                "name": "LG 65-inch OLED C1 Series Smart TV",
                "store": "Amazon",
                "price": "$1496.99",
                "url": "https://www.example.com/lg-tv",
                "image_url": "https://images.unsplash.com/photo-1601944177324-f23675000dea?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            },
            {
                "name": "Sony 75-inch BRAVIA XR X90J Smart TV",
                "store": "Target",
                "price": "$1298.00",
                "url": "https://www.example.com/sony-tv",
                "image_url": "https://images.unsplash.com/photo-1509281373149-e957c6296406?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            }
        ]
    elif "laptop" in query_lower:
        dummy_products = [
            {
                "name": "Apple MacBook Air M2 Chip",
                "store": "Apple Store",
                "price": "$1199.00",
                "url": "https://www.example.com/macbook-air",
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            },
            {
                "name": "Dell XPS 13 Laptop",
                "store": "Dell.com",
                "price": "$999.99",
                "url": "https://www.example.com/dell-xps",
                "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            },
            {
                "name": "HP Spectre x360",
                "store": "HP Store",
                "price": "$1049.99",
                "url": "https://www.example.com/hp-spectre",
                "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            }
        ]
    elif "coffee maker" in query_lower:
        dummy_products = [
            {
                "name": "Keurig K-Classic Coffee Maker",
                "store": "Walmart",
                "price": "$119.00",
                "url": "https://www.example.com/keurig-classic",
                "image_url": "https://images.unsplash.com/photo-1565452344010-870994816150?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            },
            {
                "name": "Nespresso VertuoPlus Coffee and Espresso Machine",
                "store": "Bed Bath & Beyond",
                "price": "$159.00",
                "url": "https://www.example.com/nespresso-vertuo",
                "image_url": "https://images.unsplash.com/photo-1507133750040-6511ba8443de?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=60"
            }
        ]
    # If no specific keyword matches, dummy_products remains empty.
    # results.html will then show the "No products found for 'query'" message.

    return render_template('results.html', query=query, products=dummy_products, error_message=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
