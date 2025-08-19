# ProductScan

ProductScan is a Django-based application that allows users to scan QR codes, upload them, and process the data. It serves as a backend API for handling product scanning and QR code uploads.

## Features

- **Scan QR Codes**: Scan QR codes and display the product details.
- **Upload QR Codes**: Upload QR codes for processing.
- **Admin Interface**: Built-in admin interface for managing data.

## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.x
- Django 3.x or higher
- Virtualenv (recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/username/ProductScan.git
   cd ProductScan
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
python manage.py runserver
Your application should now be running at http://127.0.0.1:8000/.

### URL Patterns

/admin/: Django admin interface

/scan/: Page to scan QR codes

/upload_qr/: Endpoint to upload QR codes

### Development

To contribute to this project, fork the repository and submit pull requests. Make sure to follow the coding standards and write tests for any new features.

License

This project is licensed under the MIT License - see the LICENSE
 file for details.

### Technologies Used

Django: Web framework for building the application.

SQLite: Default database (can be changed based on project needs).

Python: Programming language used for backend development.
