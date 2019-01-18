from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Studio, Game

# Flask configuration
app = Flask(__name__)

# Database configuration
engine = create_engine('sqlite:///studios.db')
Base.metadata.bind = engine
# Connecting to session
DBSession = sessionmaker(bind=engine)
session = DBSession()



# -------------------------------------------------------------
# studios = [{'name':'Activision', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'},
# {'name':'Naughty Dog', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'},
# {'name':'Toys For Bob', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'}]

# studio = {'name':'Activision', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'}

# games = [{'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'},
# {'name':'Crash Bandicoot', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'},
# {'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'}]

# game = {'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'}
# -------------------------------------------------------------

# JSON 

# Main landing page, showing a list of all studios
@app.route('/')
@app.route('/studios/')
def showStudios():
	studios = session.query(Studio).all()
	return render_template('studios.html', studios=studios)


@app.route('/studios/new', methods=['GET', 'POST'])
def newStudio():
	if request.method == 'POST':
		newStudio = Studio(name=request.form['name'], founded_date=request.form['founded_date'], founder=request.form['founder'])
		session.add(newStudio)
		session.commit()
		return redirect(url_for('showStudios'))
	else:
		return render_template('newStudio.html')


@app.route('/studios/<int:studio_id>/edit', methods=['GET', 'POST'])
def editStudio(studio_id):
	editedStudio = session.query(
		Studio).filter_by(id=studio_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedStudio.name = request.form['name']
			return redirect(url_for('showStudios'))
	else:
		return render_template('editStudio.html', studio=editedStudio)


@app.route('/studios/<int:studio_id>/delete', methods=['GET', 'POST'])
def deleteStudio(studio_id):
	studioToDelete = session.query(Studio).filter_by(id=studio_id).one()
	if request.method == 'POST':
		session.delete(studioToDelete)
		session.commit()
		return redirect(url_for('showStudios', studio_id=studio_id))
	else:
		return render_template('deleteStudio.html', studio=studioToDelete)


@app.route('/studios/<int:studio_id>')
@app.route('/studios/<int:studio_id>/games')
def studioGames(studio_id):
	studio = session.query(Studio).filter_by(id=studio_id).one()
	games = session.query(Game).filter_by(studio_id=studio_id).all()

	return render_template('games.html', studio=studio, games=games)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/edit', methods=['GET', 'POST'])
def editGame(studio_id, game_id):
	editedGame= session.query(Game).filter_by(id=game_id).one()
	if request.method == 'POST':
		# if request.form['quantity']:
		editedGame.quantity = request.form['quantity']
		session.add(editedGame)
		session.commit()
		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('editGame.html', studio_id=studio_id, game_id=game_id, game=editedGame)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/delete', methods=['GET', 'POST'])
def deleteGame(studio_id, game_id):
	gameToDelete = session.query(Game).filter_by(id=game_id).one()
	if request.method == 'POST':
		session.delete(gameToDelete)
		session.commit()
		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('deleteGame.html', game=gameToDelete)


@app.route('/studios/<int:studio_id>/games/new', methods=['GET', 'POST'])
def newGame(studio_id):
	if request.method == 'POST':
		newGame = Game(name=request.form['name'], description=request.form['description'], price=request.form['price'], release_date=request.form['release_date'],quantity=request.form['quantity'], studio_id=studio_id)
		session.add(newGame)
		session.commit()

		return redirect(url_for('studioGames', studio_id=studio_id))
	else:
		return render_template('newGame.html', studio_id=studio_id)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)





