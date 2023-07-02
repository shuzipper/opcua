from opcua import Client
import threading
import time
import logging

class UaClient:
    def __init__(self, server_url, node_ids):
        self.server_url = server_url
        self.node_ids = node_ids
        self.data = []
        self.lock = threading.Lock()
        self.is_running = False
       

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        thread = threading.Thread(target=self._run)
        thread.start()

    def stop(self):
        self.is_running = False

    def get_data(self):
        with self.lock:
            data = self.data.copy()
            logging.info(f"Read data : {data}")
            self.data.clear()   
            return data
            

    def _run(self):
        while self.is_running:
            try:
                with Client(self.server_url) as client:
                    timestamp = int(time.time() * 1_000_000_000)
                    data_dict = {"timestamp":timestamp}
                    #self.data.append(time.time())
                    for alias, node_id in self.node_ids.items():
                        node = client.get_node(node_id)
                        value = node.get_value()
                        data_dict[alias] = value
                        with self.lock:
                            self.data.append(data_dict)
            except Exception as e:
                logging.error(f"Error reading data from {self.server_url}: {e}")
            time.sleep(0.05)
