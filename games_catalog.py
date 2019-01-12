from flask import Flask, render_template, url_for

app = Flask(__name__)

studios = [{'name':'Activision', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'},
{'name':'Naughty Dog', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'},
{'name':'Toys For Bob', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'}]

studio = {'name':'Activision', 'id':'1', 'founded_date':'1979', 'founder':'David Crane'}

games = [{'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'},
{'name':'Crash Bandicoot', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'},
{'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'}]

game = {'name':'Spyro', 'id':'1', 'description':'Spyro is a game about a purple dragon', 'release_date':'1994', 'quantity':'20', 'price':'50$'}

@app.route('/')
@app.route('/studios/')
def showStudios():

	return render_template('studios.html', studios=studios) # TODO: Accomedate for corner case here


@app.route('/studios/new')
def newStudio():

	return render_template('newStudio.html')


@app.route('/studios/<int:studio_id>/edit')
def editStudio(studio_id):

	return render_template('editStudio.html', studio=studio)


@app.route('/studios/<int:studio_id>/delete')
def deleteStudio(studio_id):

	return render_template('deleteStudio.html', studio=studio)


@app.route('/studios/<int:studio_id>')
@app.route('/studios/<int:studio_id>/games')
def studioGames(studio_id):

	return render_template('games.html', studio=studio, games=games)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/edit')
def editGame(studio_id, game_id):

	return render_template('editGame.html', game=game)


@app.route('/studios/<int:studio_id>/games/<int:game_id>/delete')
def deleteGame(studio_id, game_id):

	return render_template('deleteGame.html', game=game)


@app.route('/studios/<int:studio_id>/games/new')
def newGame(studio_id):

	return render_template('newGame.html', studio=studio)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)





