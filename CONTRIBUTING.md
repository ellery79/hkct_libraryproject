# Contributing to ABC Library System

This project is a homework assignment for CT290DS003 Python網站框架開發助理證書課程 at 港專職業訓練學院

## Setup and Running the Project

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt` and python-decouple package is needed.
3. Create a database using postgresql
4. Environment Configuration:
- Create a `.env` file in the root directory.
- Add the following variables (replace with your actual values):
```
DEBUG = 
ALLOWED_HOSTS = 
EMAIL_PASSWORD = 
MY_EMAIL = 
DB_NAME = 
DB_USER = 
DB_PASSWORD = 
SECRET_KEY = 
STRIPE_SECRET_KEY = 
STRIPE_PUBLISHABLE_KEY = 
```
5. Run migrations: `python manage.py migrate`
6. Import the necessary data (`UML and db backup/librarydb1_backup_20241001.backup` or `/home/poon/Documents/django_lib/UML and db backup/dbbackup_20241009.backup`) using PGAdmin.
7. Start the server: `python manage.py runserver`

For any questions, please contact 阿銓 at shrill-wiring-foe@duck.com