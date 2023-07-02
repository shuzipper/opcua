from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

class InfluxDB:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        

    def write_data(self, data):
        try:
            for datapoint in data:
                timestamp = int(datapoint.pop("timestamp"))
                #point = {"time":int(timestamp),"measurement":"test_table","tag":"Crane001",}
                point = "test_table,crane_num=crane001 "
                for alias, value in datapoint.items():
                    #point.update({alias : value})
                    point += f'{alias}="{value}"'
                point += f' {timestamp}'
                    
            self.write_api.write(bucket=self.bucket, record=point)
        except Exception as e:
            logging.error(f"Error writing data to InfluxDB: {e}")
