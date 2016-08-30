from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route("/restaurants/<int:id>/menu/JSON")
def restaurantMenuJSON(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = item.serialize)

@app.route("/")
@app.route("/restaurants/<int:id>/menu")
def restaurantMenu(id):
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = id)

    return render_template("menu.html", restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/create", methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(name = request.form["name"], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New item created")
        return redirect(url_for('restaurantMenu', id = restaurant_id))
    else:
        return render_template("create.html", restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/edit/<int:menu_id>", methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        item.name = request.form["name"]
        session.add(item)
        session.commit()
        flash("Menu item edited")
        return redirect(url_for('restaurantMenu', id = restaurant_id))
    else:
        return render_template("edit.html", restaurant_id = restaurant_id, item = item)

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/delete/<int:menu_id>", methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('restaurantMenu', id = restaurant_id))
    else:
        return render_template("remove.html", restaurant_id = restaurant_id, item = item)



if __name__ == "__main__":
    app.debug = True
    app.secret_key = "sdfsdfsfd"
    app.run(host = "0.0.0.0", port = 5000)
