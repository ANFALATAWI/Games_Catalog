from flask import Flask, render_template, url_for, request, redirect, jsonify, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Studio, Game, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# Flask configuration
app = Flask(__name__)
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

# Database configuration
engine = create_engine('sqlite:///studios.db')
Base.metadata.bind = engine

# Connecting to session
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	return render_template('login.html', STATE=state)
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
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

    # Check if user has a name
    print data
    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = 'null'
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
    	user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User functions:

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
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
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON generating functions:

# JSON for a specific studio
@app.route('/studios/<int:studio_id>/games/JSON')
def studioJSON(studio_id):
	studio = session.query(Studio).filter_by(id=studio_id).one()
	games = session.query(Game).filter_by(studio_id=studio_id).all()

	return jsonify(Games=[i.serialize for i in games])

# JSON for a spesefic game
@app.route('/studios/<int:studio_id>/games/<int:game_id>/JSON')
def gameJSON(studio_id, game_id):
	game = session.query(Game).filter_by(id=game_id).one()
	return jsonify(Game=game.serialize)

# JSON for all studios
@app.route('/studios/JSON')
def studiosJSON():
	studios = session.query(Studio).all()
	return jsonify(Studios=[s.serialize for s in studios])


# Website Pages functions:

# Main landing page, showing a list of all studios
@app.route('/')
@app.route('/studios/')
def showStudios():
	# Show all studios
	studios = session.query(Studio).all()
	return render_template('studios.html', studios=studios)


@app.route('/studios/new', methods=['GET', 'POST'])
def newStudio():
	# Verify user is logged in to have creating new functionality
	if 'username' not in login_session:
		return redirect('/login')

	if request.method == 'POST':
		newStudio = Studio(name=request.form['name'], founded_date=request.form['founded_date'], founder=request.form['founder'], user_id=login_session['user_id'])
		session.add(newStudio)
		session.commit()
		flash("New studio created!")
		return redirect(url_for('showStudios'))
	else:
		return render_template('newStudio.html')


@app.route('/studios/<int:studio_id>/edit', methods=['GET', 'POST'])
def editStudio(studio_id):
	# Verify user is logged in to have editing new functionality
	if 'username' not in login_session:
		return redirect('/login')

	editedStudio = session.query(Studio).filter_by(id=studio_id).one()
	if request.method == 'POST':
		# Check if current user is owner of the studio:
		if request.form['name']:
			editedStudio.name = request.form['name']
			flash("Studio edited!")
			return redirect(url_for('showStudios'))
	else:
		if login_session['user_id'] == editedStudio.user_id:
			print "This user is the owner of this studio"
			return render_template('editStudio.html', studio=editedStudio)
		else:
			return render_template('editStudio.html', studio=editedStudio)


@app.route('/studios/<int:studio_id>/delete', methods=['GET', 'POST'])
def deleteStudio(studio_id):
	# Verify user is logged in to have creating new functionality
	if 'username' not in login_session:
		return redirect('/login')

	studioToDelete = session.query(Studio).filter_by(id=studio_id).one()
	if request.method == 'POST':
		session.delete(studioToDelete)
		session.commit()
		flash("Studio deleted!")
		return redirect(url_for('showStudios', studio_id=studio_id))
	else:
		return render_template('deleteStudio.html', studio=studioToDelete)


@app.route('/studios/<int:studio_id>')
@app.route('/studios/<int:studio_id>/games')
def studioGames(studio_id):
	studio = session.query(Studio).filter_by(id=studio_id).one()
	games = session.query(Game).filter_by(studio_id=studio_id).all()
	# Viewdifferent pages based on ownership status
	# View edit & delete options if thisuser is the owner of the studio
	if login_session['user_id'] == studio.user_id:
		print "This user is the owner of this game"
		return render_template('games.html', studio=studio, games=games)
	# if this user isnot the owner, dont view edit & delete options
	else:
		"This user is NOT the owner of this game"
		return render_template('publicGames.html', studio=studio, games=games)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/edit', methods=['GET', 'POST'])
def editGame(studio_id, game_id):
	# Verify user is logged in to have editing functionality
	if 'username' not in login_session:
		return redirect('/login')

	editedGame= session.query(Game).filter_by(id=game_id).one()
	if request.method == 'POST':
		# if request.form['quantity']:
		editedGame.quantity = request.form['quantity']
		session.add(editedGame)
		session.commit()
		flash("Game edited!")
		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('editGame.html', studio_id=studio_id, game_id=game_id, game=editedGame)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/delete', methods=['GET', 'POST'])
def deleteGame(studio_id, game_id):
	# Verify user is logged in to have creating new functionality
	if 'username' not in login_session:
		return redirect('/login')

	gameToDelete = session.query(Game).filter_by(id=game_id).one()
	if request.method == 'POST':
		session.delete(gameToDelete)
		session.commit()
		flash("Game Deleted!")
		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('deleteGame.html', game=gameToDelete)


@app.route('/studios/<int:studio_id>/games/new', methods=['GET', 'POST'])
def newGame(studio_id):
	# Verify user is logged in to have creating new functionality
	if 'username' not in login_session:
		return redirect('/login')
		
	if request.method == 'POST':
		newGame = Game(name=request.form['name'], description=request.form['description'], price=request.form['price'], release_date=request.form['release_date'],quantity=request.form['quantity'], studio_id=studio_id, user_id=login_session['user_id'])
		user_id = login_session['user_id']
		session.add(newGame)
		session.commit()
		flash("Game created!")
		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('newGame.html', studio_id=studio_id)



if __name__ == '__main__':
	app.secret_key = "super_secret_key"
	app.debug = True
	app.run(host='0.0.0.0', port=5000)





