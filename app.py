from flask import Flask, redirect, render_template, request, session, url_for
import os
import random
import secrets
import time

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

ROOMS = {'bedroom': 'Bedroom', 'kitchen': 'Kitchen', 'living': 'Living Room'}
MOSQUITO_COUNT = 20
SPOTS = [(x, y) for y in (16, 30, 44, 58, 72, 85)
         for x in (10, 22, 34, 46, 58, 70, 82, 92)]

@app.get('/')
def home():
    return render_template('index.html', page='home', rooms=ROOMS)

@app.post('/start')
def start():
    room = request.form.get('room', 'bedroom')
    if room not in ROOMS:
        room = 'bedroom'
    session.clear()
    session['room'] = room
    session['started_at'] = time.time()
    session['round_token'] = secrets.token_urlsafe(16)
    session['locations'] = random.sample(SPOTS, MOSQUITO_COUNT)
    return redirect(url_for('game'))

@app.get('/game')
def game():
    if 'round_token' not in session:
        return redirect(url_for('home'))
    mosquitoes = [
        {'id': i, 'x': xy[0], 'y': xy[1], 'delay': (i % 7) * -0.37}
        for i, xy in enumerate(session['locations'])
    ]
    return render_template('index.html', page='game', mosquitoes=mosquitoes,
                           total=MOSQUITO_COUNT, token=session['round_token'],
                           room=session['room'], room_name=ROOMS[session['room']])

@app.post('/stop')
def stop():
    if 'round_token' not in session or request.form.get('round_token') != session['round_token']:
        return redirect(url_for('home'))
    valid_ids = {str(i) for i in range(MOSQUITO_COUNT)}
    kills = len(set(request.form.getlist('killed')) & valid_ids)
    elapsed = max(0.001, time.time() - session['started_at'])
    room_name = ROOMS[session['room']]
    room = session['room']
    session.clear()
    return render_template('index.html', page='results', kills=kills,
                           total=MOSQUITO_COUNT, elapsed=round(elapsed, 1),
                           kpm=round(kills * 60 / elapsed, 1),
                           room_name=room_name, room=room)

if __name__ == '__main__':
    app.run(debug=True)
