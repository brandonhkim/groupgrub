import time
from fusion_repository import FusionRepository
from flask import Flask 

app = Flask(__name__)

@app.route('/time')
def get_current_time():
    fr = FusionRepository()
    return {'time': time.time()}

    