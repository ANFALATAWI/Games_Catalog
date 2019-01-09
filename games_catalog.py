from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/studios')
def showStudios():
	return "Here will be all the studios"


@app.route('/studios/new')
def newStudio():
	return "Here you can create a new studio"


@app.route('/studios/<int:studio_id>/edit')
def editStudio(studio_id):
	return "You can edit studio with id=%s" % studio_id


@app.route('/studios/<int:studio_id>/delete')
def deleteStudio(studio_id):
	return "You can delete studio with id=%s" % studio_id


@app.route('/studios/<int:studio_id>')
@app.route('/studios/<int:studio_id>/games')
def studioGames(studio_id):
	return "Here are all the games for studio id=%s" % studio_id


@app.route('/studios/<int:studio_id>/games/<int:game_id>/edit')
def editGame(studio_id, game_id):
	return "This will edit game id=%s, studio id=%s" % (game_id, studio_id)

@app.route('/studios/<int:studio_id>/games/<int:game_id>/delete')
def deleteGame(studio_id, game_id):
	return "This will delete game id=%s, studio id=%s" % (game_id, studio_id)

@app.route('/studios/<int:studio_id>/games/new')
def newGame(studio_id):
	return "This page will add a new game to studio %s" % studio_id



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)





