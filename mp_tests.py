import time
import signal
from multiprocessing import Process
from multiprocessing.connection import Listener, Client

class Service(object):
    @classmethod
    def server_init(cls, address):
        server = cls(False)
        server.run_forever(address)

    def __init__(self, init_client=True):
        self.exited = False
        self.server = None
        self.connection = None

        if init_client:
            self.client_init()
    
    def is_server(self):
        return self.server == None

    def send(self, data):
        self.connection.send(data)

    def send_message(self, mtype, data=None):
        self.send({
            "type": mtype,
            "data": data
        })
    
    def recv(self):
        if self.connection.poll():
            return self.connection.recv()

        return None

    def run_forever(self, address):
        self.connection = Client(address)
        
        while self.is_running():
            self.tick()
            time.sleep(0)

    def tick(self):
        data = self.recv()

        if data != None:
            if self.is_server():
                self.handle_cli_cmd(data["type"], data["data"])
            else:
                self.handle_svr_cmd(data["type"], data["data"])

    def handle_cli_cmd(self, mtype, data):
        if mtype == "exit":
            self.exited = True
        else:
            self.handle_client_msg(mtype, data)

    def handle_svr_cmd(self, mtype, data):
        self.handle_server_msg(mtype, data)
    
    def client_init(self):
        listener = Listener(family='AF_INET')
        self.server = Process(target=self.__class__.server_init, args=(listener.address,))
        self.server.start()
        self.connection = listener.accept()
        listener.close()

    def exit(self):
        self.exited = True
        self.send_message("exit")
        self.server.join()
    
    def is_running(self):
        return not self.exited

    def handle_server_msg(self, mtype, data):
        raise NotImplementedError("Please Implement this method")

    def handle_client_msg(self, mtype, data):
        raise NotImplementedError("Please Implement this method")