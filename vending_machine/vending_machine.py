from vending_machine.product import Product
from vending_machine.exceptions import InsufficientFunds, OutOfStock, InvalidProduct


class VendingMachine:
    def __init__(self):
        """
        Initializes the vending machine with empty inventory and change.
        """
        self.products = {}
        self.change = {1: 0, 2: 0, 5: 0, 10: 0, 20: 0, 50: 0, 100: 0, 200: 0}  # Denominations in pence

    def load_products(self, products: list[Product]):
        for product in products:
            self.products[product.name] = product

    def load_change(self, change_dict: dict[int, int]):
        for denom, count in change_dict.items():
            self.change[denom] += count

    def select_product(self, product_name: str) -> Product:
        if product_name not in self.products:
            raise InvalidProduct(f"{product_name} is not available.")
        product = self.products[product_name]
        if product.quantity <= 0:
            raise OutOfStock(f"{product_name} is out of stock.")
        return product

    def process_payment(self, product: Product, payment: list[int]) -> dict:
        total_inserted = sum(payment)
        if total_inserted < product.price:
            raise InsufficientFunds(f"Insufficient funds. Insert {product.price - total_inserted}p more.")
        
        change_to_return = total_inserted - product.price
        self._dispense_change(change_to_return)
        product.reduce_quantity()
        self._update_change(payment)
        return {"product": product.name, "change": change_to_return}

    def _dispense_change(self, amount: int):
        """
        Dispense change by reducing the machine's change inventory.
        Raises an error if exact change cannot be returned.
        """
        change_given = {}
        for denom in sorted(self.change.keys(), reverse=True):
            if amount <= 0:
                break
            num_coins = min(amount // denom, self.change[denom])
            if num_coins > 0:
                change_given[denom] = num_coins
                amount -= denom * num_coins
        if amount > 0:
            raise ValueError("Unable to return exact change.")
        for denom, count in change_given.items():
            self.change[denom] -= count

    def _update_change(self, payment: list[int]):
        """
        Add the inserted coins to the machine's change inventory.
        """
        for denom in payment:
            self.change[denom] += 1

    def get_total_change(self):
        """Calculate the total value of all change in the machine and display coin breakdown."""
        total_value = sum(denomination * quantity for denomination, quantity in self.change.items())
        breakdown = {denomination: quantity for denomination, quantity in self.change.items() if quantity > 0}
        return total_value, breakdown

    # Threshold for low coins warning
    COIN_THRESHOLD = 5

    def check_low_coins(self):
        """Check for coins below the threshold and return warnings."""
        low_coins = {denomination: quantity for denomination, quantity in self.change.items() if quantity < self.COIN_THRESHOLD}
        return low_coins

    def __repr__(self):
        return f"VendingMachine(products={self.products}, change={self.change})"
