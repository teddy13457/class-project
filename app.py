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


    
    @app.route('/create')
def create_page():
    return render_template('create.html')


@app.route('/add', methods=['POST'])
def add_utensil():
    if request.method == "POST":
        Item_name = request.form['Item_name']
        Material = request.form['Material']
        Quantity = request.form['Quantity']
        Sales_price = request.form['Sales_price']
        Purchase_price = request.form['Purchase_price']

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO kitchen_utensils (Item_name, Material, Quantity, Sales_price, Purchase_price) VALUES (%s, %s, %s, %s, %s)",
            (Item_name, Material, Quantity, Sales_price, Purchase_price))

        mysql.connection.commit()
        return redirect(url_for('dashboard'))


@app.route('/inventory')
def view_inventory():
    search_query = request.args.get('search', '')

    cursor = mysql.connection.cursor()

    if search_query:
        query = "SELECT * FROM kitchen_utensils WHERE Item_name LIKE %s"
        cursor.execute(query, ('%' + search_query + '%',))
    else:
        query = "SELECT * FROM kitchen_utensils"
        cursor.execute(query)

    utensils = cursor.fetchall()
    return render_template('inventory.html', utensils=utensils, search_query=search_query)


@app.route('/edit/<int:id>', methods=['GET'])
def edit_item(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM kitchen_utensils WHERE id = %s", (id,))
    utensil = cursor.fetchone()
    return render_template('update.html', utensil=utensil)


@app.route('/update/<int:id>', methods=['POST'])
def update_item(id):
    Item_name = request.form['Item_name']
    Material = request.form['Material']
    Quantity = request.form['Quantity']
    Sales_price = request.form['Sales_price']
    Purchase_price = request.form['Purchase_price']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE kitchen_utensils
        SET Item_name = %s, Material = %s, Quantity = %s, Sales_price = %s, Purchase_price = %s
        WHERE id = %s
    """, (Item_name, Material, Quantity, Sales_price, Purchase_price, id))
    mysql.connection.commit()
    return redirect(url_for('view_inventory'))
