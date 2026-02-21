A01703274_A6.2 - Reservation System with Unit Testing

1. Description

This project implements a file-based Reservation System in Python. The system includes CRUD operations for Hotels and Customers, as well as creation and cancellation of Reservations. Data persistence is handled through JSON files.

2. Project Structure

app/

- customer.py
- hotel.py
- reservation.py
- storage.py
- system.py

tests/

- test_customer.py
- test_hotel.py
- test_reservation.py
- test_storage_invalid_data.py

data/

- customers.json
- hotels.json
- reservations.json

3. Static Analysis

   PEP 8 compliance was verified using flake8 with strict 79 character line limit:
   python -m flake8 --max-line-length=79 app tests
   Code quality was verified using pylint:
   python -m pylint app tests

4. Unit Testing

   All unit tests were executed using:
   python -m unittest discover -s tests
   The test suite includes positive and negative test cases, including invalid inputs, missing entities, and invalid JSON data.

5. Code Coverage

   Coverage was measured using:
   python -m coverage run -m unittest discover -s tests
   python -m coverage report -m
   Total coverage achieved: 95%

6. Results Documentation

   Execution results from flake8, pylint, unittest, and coverage are documented in the file 'results.txt' included in the repository.

7. Repository Information

   Repository name: A01703274_A6.2
   This repository contains the complete implementation, tests, static analysis verification, and evidence files as required by the assignment instructions.
