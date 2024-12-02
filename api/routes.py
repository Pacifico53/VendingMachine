from flask import Blueprint, jsonify, request
from vending_machine.vending_machine import VendingMachine
from vending_machine.product import Product
from vending_machine.exceptions import InvalidProduct, InsufficientFunds, OutOfStock

# Initialize the Blueprint
api = Blueprint('api', __name__)

# Initialize the vending machine
vending_machine = VendingMachine()
vending_machine.load_products([
    Product("chips", 70, 10),
    Product("soda", 120, 5),
    Product("candy", 50, 15),
])
vending_machine.load_change({
    1: 50, 2: 50, 5: 20, 10: 20, 20: 10, 50: 10, 100: 10, 200: 5
})

@api.route('/products', methods=['GET'])
def get_products():
    """Get the list of products and their details."""
    products = {
        name: {"price": product.price, "quantity": product.quantity}
        for name, product in vending_machine.products.items()
    }
    return jsonify(products), 200

@api.route('/purchase', methods=['POST'])
def purchase():
    """Purchase a product."""
    data = request.json
    product_name = data.get("product", "").lower()
    payment = data.get("payment", [])

    if not product_name or not isinstance(payment, list):
        return jsonify({"error": "Invalid input. Provide 'product' and 'payment' fields."}), 400

    try:
        product = vending_machine.select_product(product_name)
        result = vending_machine.process_payment(product, payment)
        return jsonify({
            "message": "Purchase successful",
            "product": result["product"],
            "change_dispensed": result["change"]
        }), 200
    except InvalidProduct as e:
        return jsonify({"error": str(e)}), 404
    except OutOfStock as e:
        return jsonify({"error": str(e)}), 409
    except InsufficientFunds as e:
        return jsonify({"error": str(e)}), 402
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@api.route('/change', methods=['GET'])
def get_total_change():
    """Get the total change and the breakdown of coins."""
    total, breakdown = vending_machine.get_total_change()
    return jsonify({"total_change": total, "coin_breakdown": breakdown}), 200

@api.route('/reload', methods=['POST'])
def reload_machine():
    """Reload coins or restock products."""
    data = request.json
    coins = data.get("coins", {})
    products = data.get("products", {})

    if not isinstance(coins, dict) or not isinstance(products, dict):
        return jsonify({"error": "Invalid input. 'coins' and 'products' must be dictionaries."}), 400

    # Reload coins
    for denomination, quantity in coins.items():
        if denomination in vending_machine.change:
            vending_machine.change[denomination] += quantity

    # Restock products
    for name, quantity in products.items():
        if name in vending_machine.products:
            vending_machine.products[name].quantity += quantity

    return jsonify({"message": "Machine reloaded successfully."}), 200

@api.route('/warn-low-coins', methods=['GET'])
def warn_low_coins():
    """Warn if any coin denominations are running low."""
    low_coins = vending_machine.check_low_coins()
    if low_coins:
        return jsonify({"warning": "Low coin denominations", "details": low_coins}), 200
    return jsonify({"message": "All denominations are sufficiently stocked."}), 200
