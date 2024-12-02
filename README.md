# Vending Machine API
This is a Python project that simulates a vending machine with an API interface built using Flask. The project includes functionalities for managing products, processing purchases, handling change, and reloading the machine.

## Features
- **View Products**: Get a list of products available in the vending machine, including their prices and quantities.
- **Purchase Product**: Simulate purchasing a product, including payment processing and change dispensing.
- **Change Management**: View the total change and its breakdown by denomination.
- **Reload Machine**: Restock products or add more coins to the machine.
- **Low Coin Warning**: Check for coin denominations that are running low.

## Setup and Installation
### Prerequisites
- Python 3.10+
- `pip`

### Installing
 1. Clone the repository:
```bash
git clone https://github.com/Pacifico53/VendingMachine.git
cd vendingMachine
```  
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. The API will be accessible at `http://127.0.0.1:5000/`.


## Endpoints
### 1. Get Products
**URL**: `/api/products`  
**Method**: `GET`  
**Description**: Retrieve a list of available products with their prices and quantities.  
**Response**:
```json
{
  "chips": {"price": 70, "quantity": 10},
  "soda": {"price": 120, "quantity": 5},
  "candy": {"price": 50, "quantity": 15}
}
```

### 2. Purchase Product
**URL**: `/api/purchase`  
**Method**: `POST`  
**Description**: Purchase a product from the vending machine. 
**Request Body**:
```json
{
  "product": "chips",
  "payment": [100]
}
```
**Response**:
```json
{
  "message": "Purchase successful",
  "product": "chips",
  "change_dispensed": 30
}
```

### 3. Get Total Change
**URL**: `/api/change`  
**Method**: `GET`  
**Description**: Get the total change in the machine and its coin breakdown.  
**Response**:
```json
{
  "total_change": 9850,
  "coin_breakdown": {
    "1": 50,
    "2": 50,
    "5": 20,
    "10": 20,
    "20": 10,
    "50": 10,
    "100": 10,
    "200": 5
  }
}
```

### 4. Reload Machine
**URL**: `/api/reload`  
**Method**: `POST`  
**Description**: Reload coins or restock products. 
**Request Body**:
```json
{
  "coins": {
    "1": 10,
    "50": 5
  },
  "products": {
    "chips": 5,
    "soda": 2
  }
}
```
**Response**:
```json
{
  "message": "Machine reloaded successfully."
}
```

### 5. Warn Low Coins
**URL**: `/api/warn-low-coins`  
**Method**: `GET`  
**Description**: Check if any coin denominations are running low.  
**Response**:
```json
{
  "warning": "Low coin denominations",
  "details": {
    "200": 2
  }
}
```

## Running Tests
### Unit Tests
To run unit and api tests:

`python -m pytest`
