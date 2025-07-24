from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_crud_db'

mysql = MySQL(app)


@app.route('/')
def dashboard():
    cursor = mysql.connection.cursor()

    # Total items
    cursor.execute("SELECT COUNT(*) FROM kitchen_utensils")
    total_items = cursor.fetchone()[0]

    # Items low in stock (you can adjust the threshold)
    cursor.execute("SELECT COUNT(*) FROM kitchen_utensils WHERE Quantity <= 5")
    low_stock_count = cursor.fetchone()[0]

    # Recent activity (last 2 items)
    cursor.execute("SELECT Item_name, Purchase_price FROM kitchen_utensils ORDER BY id DESC LIMIT 2")
    recent_items = cursor.fetchall()

    cursor.close()
    return render_template(
        'dashboard.html',
        total_items=total_items,
        low_stock_count=low_stock_count,
        recent_items=recent_items
    )
