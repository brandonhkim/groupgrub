import os
import config as config

class FusionRepository:
    def __init__(self):
        self.headers = {
            'Authorization': config.fusion_key,
        }
    
        