# ABC Library Management System

## Project Overview

ABC Library Management System is a Django-based web application developed as a group project for CT290DS003 Python網站框架開發助理證書課程. This system is designed to manage library operations for external users, allowing them to browse books, make reservations, view borrowings, and process overdue fines.

## Features

- User Authentication and Authorization
- Book Catalog Management
- Reservation System
- View borrows
- Fine Calculation and Payment Processing
- Library Information Display
- Search Functionality

## Tech Stack

- Python 3.11.9
- Django 4.2.16
- PostgreSQL
- Stripe for Payment Processing
- HTML/CSS/JavaScript for Frontend
- Bootstrap 4.2

## Project Structure

The project consists of several Django apps:

- `accounts`: Handles user authentication and profile management
- `books`: Manages book catalog and search functionality
- `borrows`: Borrows database
- `libraries`: Manages library information
- `pages`: Handles index, about pages and global context
- `reserves`: Reserves database
- `infos`: Stores global information

## Key Functionalities

1. **User Management**: Users can register, log in, and manage their profiles.
2. **Book Search**: Advanced search functionality to find books by title, author, or library.
3. **Reservations**: Users can reserve available books.
4. **Borrowing System**: Tracks book checkouts and returns.
5. **Fine Management**: Calculates and processes fines for overdue books.
6. **Library Information**: Displays details about different library branches.

## Group Members (in no particular order)

- 鄧岳鳴（學號︰1）
- 洪餘暉（學號︰6）
- 陳耀豐（學號︰12）
- 潘浩銓（學號︰15）

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on starting the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django documentation and community resources
- 衛龍老師 for project guidance