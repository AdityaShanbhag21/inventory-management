# Inventory Management System (Warehouse MVP)

A minimal yet production-ready **Inventory Tracking System** built with **Django** and **Django REST Framework**.  
Tracks **stock movements** in a warehouse (IN / OUT transactions) and provides real-time inventory levels per product.  
Designed for **clean API design**, **maintainability**, and **easy deployment** (tested on Render).

---

# Features

- **Product Management**  
  Create, update, delete, and list products with pricing.

- **Transaction Management**  
  Log **IN** (stock received) and **OUT** (stock issued) transactions with multiple product details.

- **Inventory Calculation**  
  Real-time aggregated inventory at any point based on all transactions.

- **RESTful API**  
  Clean, versionable endpoints built with DRF for easy integration.

- **Validation**  
  Strong backend validation for quantities, prices, and transaction dates.

- **Deployment Ready**  
  Includes `Procfile`, static file config, and PostgreSQL compatibility for Render deployment.

---

# Tech Stack

- **Backend:** Django 4.x, Django REST Framework
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Static Files:** WhiteNoise
- **Deployment:** Render (Gunicorn + Whitenoise)
- **Language:** Python 3.10+

---
##  Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/inventory-management.git
cd inventory-management
```
### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```
### 6. Run development server
``` bash
python manage.py runserver
```

---

### API Endpoints

| Method | Endpoint                       | Description                         |
| ------ | ------------------------------ | ----------------------------------- |
| GET    | `/api/products/`               | List products                       |
| POST   | `/api/products/`               | Create product                      |
| GET    | `/api/transactions/`           | List transactions                   |
| POST   | `/api/transactions/`           | Create transaction (nested details) |
| GET    | `/api/transactions/inventory/` | Get current inventory               |

---

## License
This project is licensed under the [MIT License](LICENSE).

