from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Item

engine = create_engine('sqlite:///catalog_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/json/')
def itemJSON(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify (item=item.serialize)

# Make JSON API endpoint request
@app.route('/catalogs/<int:catalog_id>/json/')
def catalogJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog_id).all()
    return jsonify (Item=[i.serialize for i in items])


@app.route('/')
@app.route('/catalogs/')
def showCatalogs():
    # return ("This should show the list of catalogs")
    catalogs = session.query(Catalog).all()
    return render_template('showCatalogs.html', catalogs = catalogs)

@app.route('/catalog/new/', methods=['GET','POST'])
def newCatalog():
    if request.method == 'POST':
        newCatalog = Catalog(name = request.form['name'])
        session.add(newCatalog)
        flash('New Catalog %s Successfully Created' % newCatalog.name)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html')

@app.route('/catalogs/<int:catalog_id>/')
def CatalogItems(catalog_id):
    catalog = session.query(Catalog).filter_by(id = catalog_id).one()
    items = session.query(Item).filter_by(catalog_id = catalog_id)
    return render_template('catalog.html', catalog=catalog, items=items)

@app.route('/catalogs/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], catalog_id = catalog_id)
        session.add(newItem)
        session.commit()
        flash("new catalog item %s created!" % (newItem.name))
        return redirect(url_for('CatalogItems', catalog_id = catalog_id))
    else:
        return render_template('newItem.html', catalog_id = catalog_id)

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/edit/',
            methods=['GET', 'POST'])
def editItem(catalog_id, item_id):
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("catalog item edited!")
        return redirect(url_for('CatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'editcatalogitem.html', catalog_id=catalog_id, item_id=item_id, item=editedItem)

@app.route('/catalogs/<int:catalog_id>/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(catalog_id, item_id):
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("catalog item deleted!")
        return redirect(url_for('CatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'deleteitem.html', catalog_id=catalog_id, item_id=item_id, item=deletedItem)




if __name__ == '__main__':
    app.secret_key = "Woosie"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
