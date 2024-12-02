import pytest
from vending_machine.vending_machine import VendingMachine
from vending_machine.product import Product
from vending_machine.exceptions import InvalidProduct, InsufficientFunds, OutOfStock


@pytest.fixture
def setup_vending_machine():
    """Fixture to create a vending machine with initial products and coins."""
    vm = VendingMachine()
    products = [
        Product("chips", 70, 10),
        Product("soda", 120, 5),
        Product("candy", 50, 15)
    ]
    coins = {1: 50, 2: 50, 5: 20, 10: 20, 20: 10, 50: 10, 100: 10, 200: 5}
    vm.load_products(products)
    vm.load_change(coins)
    return vm


def test_select_product_success(setup_vending_machine):
    vm = setup_vending_machine
    product = vm.select_product("chips")
    assert product.name == "chips"
    assert product.price == 70


def test_select_product_invalid(setup_vending_machine):
    vm = setup_vending_machine
    with pytest.raises(InvalidProduct):
        vm.select_product("water")


def test_select_product_out_of_stock(setup_vending_machine):
    vm = setup_vending_machine
    vm.products["chips"].quantity = 0
    with pytest.raises(OutOfStock):
        vm.select_product("chips")


def test_process_payment_success(setup_vending_machine):
    vm = setup_vending_machine
    product = vm.select_product("chips")
    result = vm.process_payment(product, [100])
    assert result["product"] == "chips"
    assert result["change"] == 30
    assert vm.products["chips"].quantity == 9  # Stock reduced


def test_process_payment_insufficient_funds(setup_vending_machine):
    vm = setup_vending_machine
    product = vm.select_product("chips")
    with pytest.raises(InsufficientFunds):
        vm.process_payment(product, [50])


def test_dispense_change_exact(setup_vending_machine):
    vm = setup_vending_machine
    vm._dispense_change(70)
    assert vm.change[50] == 9
    assert vm.change[20] == 9


def test_check_low_coins(setup_vending_machine):
    vm = setup_vending_machine
    vm.change[10] = 2
    low_coins = vm.check_low_coins()
    assert low_coins == {10: 2}
