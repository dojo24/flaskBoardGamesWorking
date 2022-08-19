from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.game import Game
from flask_app.models.user import User


@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        theGames = Game.allGamesWithUserAndLikes()
        theUsers = User.getAll()
        # print('theGames controller: ', theGames)
        return render_template('dashboard.html', user=theUser, games=theGames, users=theUsers)


@app.route('/addGame/')
def addGame():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        return render_template('addGame.html', user=theUser)

@app.route('/createGame/', methods=['post'])
def createGame():
    data = {
        'title': request.form['title'],
        'info': request.form['info'],
        'user_id': session['user_id'],
    }
    Game.save(data)
    return redirect('/dashboard/')

@app.route('/game/<int:game_id>/view/')
def viewGame(game_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        gameData = {
            'id': game_id
        }
        theUser = User.getOne(data)
        theGame = Game.getOne(gameData)
        return render_template('viewGame.html', user=theUser, game=theGame)

@app.route('/game/<int:game_id>/edit/')
def editGame(game_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        gameData = {
            'id': game_id
        }
        theGame = Game.getOne(gameData)
        return render_template('editGame.html', user=theUser, game=theGame)

@app.route('/game/<int:game_id>/update/', methods=['post'])
def updateGame(game_id):
    data = {
        'id': game_id,
        'title': request.form['title'],
        'info': request.form['info']
    }
    Game.update(data)
    return redirect(f'/game/{game_id}/view/')

@app.route('/game/<int:game_id>/delete/')
def deleteGame(game_id):
    data = {
        'id': game_id
    }
    Game.delete(data)
    return redirect('/dashboard/')