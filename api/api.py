import time
from fusion_repository import FusionRepository
from flask import Flask 

app = Flask(__name__)

# TODO: Remove - only being used to test differet React Components
@app.route('/time')
def get_current_time():
    fusion_repo = FusionRepository()
    # tmp = fusion_repo.getRestaurants(['33.866669', '-117.566666'], ['mcdonalds'], 3)
    # for a in tmp: print(a.name)

    return {'time': time.time()}

# NOTE: research data persistence, keep logged in
@app.route('/login')
def login():
    raise NotImplementedError


@app.route('/register')
def register():
    raise NotImplementedError


@app.route('/lobby')
def host_join():
    # TODO: Part 1 - host or join
    # TODO: Part 2 - lobby
    raise NotImplementedError


# joining actual lobby
@app.route('/lobby<code>')
def lobby():
    raise NotImplementedError

# get categories, filter them, query yelp, begin
@app.route('/lobby<code>/game')
def game():
    raise NotImplementedError



    