import time
from mp_tests import Service

class MyService(Service):
    def do_stuff(self):
        self.send_message("step1")

    def handle_client_msg(self, mtype, data):
        if mtype == "step1":
            print("Server got step 1")
            self.send_message("step2")
        elif mtype == "step3":
            print("Server got step 3")
            self.send_message("step4")

    def handle_server_msg(self, mtype, data):
        if mtype == "step2":
            print("Client got step 2")
            self.send_message("step3")
        elif mtype == "step4":
            print("Client got step 4")
            self.exit()

if __name__ == "__main__":
    service = MyService()
    service.do_stuff()

    while service.is_running():
        service.tick()
        time.sleep(0)