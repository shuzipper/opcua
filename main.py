import threading
import time

from config import Config
from opcua_client import UaClient
from influxdb import InfluxDB

def read_data(ua_servers, node_ids, interval):
    ua_clients = [UaClient(server_url, node_ids) for server_url in ua_servers]
    for ua_client in ua_clients:
        ua_client.start()
    while True:
        data = []
        for ua_client in ua_clients:
            data += ua_client.get_data()
        influxdb_client.write_data(data)
        time.sleep(interval)


if __name__ == '__main__':
    config = Config('./test-accs-log/config.json')
    ua_servers = config.ua_servers
    node_ids = config.node_ids
    influxdb_config = config.influxdb
    influxdb_client = InfluxDB(
        url=influxdb_config['url'],
        token=influxdb_config['token'],
        org=influxdb_config['org'],
        bucket=influxdb_config['bucket']
    )
    interval = 0.1
    thread = threading.Thread(target=read_data, args=(ua_servers, node_ids, interval))
    thread.start()
