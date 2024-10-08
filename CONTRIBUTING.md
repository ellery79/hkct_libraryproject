# Contributing to ABC Library System

This project is a homework assignment for CT290DS003 Python網站框架開發助理證書課程 at 港專職業訓練學院

## Setup and Running the Project

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt` and python-decouple package is needed.
3. Create a database using postgresql
4. Provide necessary credentials using a `.env` file
5. Run migrations: `python manage.py migrate`
6. Import the necessary data (`UML and db backup/librarydb1_backup_20241001.backup`) using PGAdmin.
7. Start the server: `python manage.py runserver`

For any questions, please contact 阿銓 at shrill-wiring-foe@duck.com