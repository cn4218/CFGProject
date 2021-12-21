from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from obf_db_utils import get_proper_ingredients_list, store_results,fetch_results, returning_products_in_pages


app = Flask(__name__)
CORS(app) #b Cross Origin Resource Sharing
list_ = []

## OBF PRODUCTS
##################################################################################################

@app.route("/")
def serve_home_page():
    return render_template("home.html")


@app.route("/Search", methods=['POST'])
def find_products():
    """
    We use a POST method and not a simple GET one because we want to be able to make a
    request containing the ingredient_input search from the front end UI.
    Returns a JSON file containing the list of products we asked for according to our request search
    criteria.
    """
    ingredient_input = request.get_json()
    print(ingredient_input)
    
    list_of_products = get_proper_ingredients_list(ingredient_input)
    if isinstance(list_of_products,Exception):
        return jsonify('Query returns no search results')
    list_.clear()
    list_.append(list_of_products)

    result = store_results(list_of_products)

    return jsonify(list_of_products)

@app.route("/Results", methods=['GET'])
def send_results():
    """
    Retrieves ssearch results for given search id
    """
    
    list_of_products = fetch_results(1)
    list_.clear()
    list_.append(list_of_products)

    
    return jsonify(list_of_products)


@app.route("/Search/<int:search_id>/page/<int:page_id>")
def page_results(search_id,page_id):
    """
    Retrieves search results with given page number, each page shows 25 results
    """
    list_of_products = fetch_results(search_id)
    list_page_products = returning_products_in_pages(list_of_products,page_id)
    list_.clear()
    list_.append(list_page_products)
    return jsonify(list_page_products)



if __name__ == '__main__':
    app.run(debug=True, port=5001)

