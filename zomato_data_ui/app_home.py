from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Function to create a connection to MySQL database
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='P@ssw0rd',  # Replace with your MySQL password
        database='zomato'  # Database name
    )

