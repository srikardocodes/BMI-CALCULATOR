# BMI-CALCULATOR

Advanced BMI Health Tracker

A Python-based BMI Health Tracker with a modern Tkinter GUI that allows users to calculate, save, and monitor their Body Mass Index over time.

Features

Calculate BMI using weight and height

Automatically classify BMI as Underweight, Normal, Overweight, or Obese

Colour-coded BMI results

Support for multiple users

Store BMI records using SQLite

View historical BMI records in a table

Visualize BMI changes over time with Matplotlib

Input validation and helpful error messages

Database error handling

User-friendly graphical interface

Technologies Used

Python

Tkinter – GUI development

SQLite3 – Data storage

Matplotlib – BMI trend visualization

BMI Categories
BMI	Category
Below 18.5	Underweight
18.5 – 24.9	Normal
25 – 29.9	Overweight
30 or above	Obese
How to Run

Install Matplotlib:

pip install matplotlib


Run the application:

python bmi_tracker.py


The application automatically creates an SQLite database (bmi_records.db) to store BMI history.

Project Highlights

This project demonstrates Python GUI development, database management, input validation, CRUD-style data handling, and data visualization. It was developed as an advanced version of a command-line BMI calculator.
