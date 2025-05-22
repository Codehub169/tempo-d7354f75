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
    Currently returns a placeholder message indicating the search query.
    This route will eventually be expanded to fetch price comparison data
    and render a results page (e.g., results.html).
    """
    query = request.args.get('query', '') # Get the search query from form submission
    
    if not query.strip():
        # If query is empty or whitespace, return an informative message
        return "Please enter a product name to search.", 400 
    
    # Placeholder for actual search logic and rendering results.html
    # In a future step, this will involve:
    # 1. Fetching data from various e-commerce sites based on the 'query'.
    # 2. Scraping/parsing product information and prices.
    # 3. Compiling a list of comparative prices.
    # 4. Passing this data to a 'results.html' template.
    return f"Search initiated for: \"{query}\". Price comparison results will be displayed here soon!"

if __name__ == '__main__':
    # This block allows running the app directly with `python app.py`
    # Useful for development. The host and port settings here might be
    # overridden by command-line arguments if using `flask run` (as in startup.sh).
    app.run(debug=True, host='0.0.0.0', port=9000)
