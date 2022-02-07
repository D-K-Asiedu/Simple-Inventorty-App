from itertools import chain
from unicodedata import name
from xml.dom.minidom import Identified
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'coded'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Inventory {self.id}'

@app.route('/')
def home():
    inventories = Inventory.query.all()
    print(inventories)
    return render_template('index.html', inventories=inventories)

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        data = request.form
        name = data['name']
        quantity = data['quantity']
        
        inventory = Inventory(item=name, quantity=quantity)
        db.session.add(inventory)
        db.session.commit()

    return render_template('add.html')

@app.route('/delete/<id>')
def delete(id):
    inventory = Inventory.query.get(int(id))
    db.session.delete(inventory)
    db.session.commit()
    return redirect('/')

@app.route('/update/<id>', methods=["GET", "POST"])
def update(id):
    inventory = Inventory.query.get(int(id))
    if request.method == "GET":   
        return render_template('update.html', inventory=inventory)

    elif request.method == "POST":
        data = request.form
        inventory.item = data['name']
        inventory.quantity = data['quantity']
        db.session.commit()

        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)