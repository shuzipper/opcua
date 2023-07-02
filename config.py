import json
import logging

class Config:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            config = json.load(f)
        try:
            self.ua_servers = config['ua_servers']
            self.node_ids = config['node_ids']
            self.influxdb = config['influxdb']
        except KeyError as e:
            logging.error(f"Invalid configuration file: {e}")
            raise
