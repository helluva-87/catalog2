#!/usr/bin/python3
from database_setup import Base, Catalog, Item
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine
from flask import Flask, render_template, url_for, request, redirect
from flask import flash, jsonify
from flask import session as login_session
from flask import make_response
# Imports for GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests
app = Flask(__name__)


# Declare Client ID by referencing the client_secrets copied from
# Google developer Console
CLIENT_ID = json.loads(
    open('/var/www/catalog2/catalog2/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"


engine = create_engine('sqlite:////var/www/catalog2/catalog2/catalog_database.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login3.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Confirm that the  state token that the client sent to the server matches
    # The  state token sent from the server to the client
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already\
                                 connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += " style = width: 300px; height: 300px; border-radius: 150px;"
    output += "-webkit-border-radius: 150px;"
    output += "-moz-border-radius: 150px;  > "
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

@app.route('/disconnect')
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('No Access Token available for this session...')
        response = make_response(json.dumps('Current user not\
                                 connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s'), access_token
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token\
                                 for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalogs/<int:catalog_id>/<int:item_id>/json/')
def itemJSON(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

# Make JSON API endpoint request
@app.route('/catalogs/<int:catalog_id>/json/')
def catalogJSON(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog_id).all()
    return jsonify(Item=[i.serialize for i in items])


@app.route('/')
@app.route('/catalogs/')
def showCatalogs():
    # return ("This should show the list of catalogs")
    catalogs = session.query(Catalog).all()
    return render_template('showCatalogs.html', catalogs=catalogs)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalog = Catalog(name=request.form['name'])
        session.add(newCatalog)
        flash('New Catalog %s Successfully Created' % newCatalog.name)
        session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html')


@app.route('/catalogs/<int:catalog_id>/')
def CatalogItems(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Item).filter_by(catalog_id=catalog_id)
    return render_template('catalog.html', catalog=catalog, items=items)


@app.route('/catalogs/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       type=request.form['type'], price=request.form['price'],
                       catalog_id=catalog_id)
        session.add(newItem)
        session.commit()
        flash("new catalog item %s created!" % (newItem.name))
        return redirect(url_for('CatalogItems', catalog_id=catalog_id))
    else:
        return render_template('newItem.html', catalog_id=catalog_id)


@app.route('/catalogs/<int:catalog_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['type']:
            editedItem.type = request.form['type']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("catalog item edited!")
        return redirect(url_for('CatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'editcatalogitem.html', catalog_id=catalog_id, item_id=item_id,
            item=editedItem)


@app.route('/catalogs/<int:catalog_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("catalog item deleted!")
        return redirect(url_for('CatalogItems', catalog_id=catalog_id))
    else:
        return render_template(
            'deleteitem.html', catalog_id=catalog_id, item_id=item_id,
            item=deletedItem)


if __name__ == '__main__':
    app.secret_key = "Woosie"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
