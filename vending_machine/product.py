class Product:
    def __init__(self, name: str, price: int, quantity: int):
        """
        Represents a product in the vending machine.

        :param name: Name of the product.
        :param price: Price of the product in pence.
        :param quantity: Quantity of the product available.
        """
        self.name = name
        self.price = price
        self.quantity = quantity

    def reduce_quantity(self, amount: int = 1):
        """
        Reduces the quantity of the product by the specified amount.
        Raises an exception if the quantity is insufficient.
        """
        if self.quantity < amount:
            raise ValueError(f"Insufficient quantity of {self.name}")
        self.quantity -= amount

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price}, quantity={self.quantity})"
