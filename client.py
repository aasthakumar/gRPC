import grpc
import ping_pb2_grpc
from ping_pb2 import Request, Response 
import time
import sys

class PingClient():
    def __init__(self, port, host='0.0.0.0'):
        #print(port)
        self.channel = grpc.insecure_channel('%s:%d' % (host, int(port)))
        self.stub = ping_pb2_grpc.PingPongStub(self.channel)
        self.clientid = 0

    def ping(self, data):
        req = Request(data=str(data))
        return self.stub.ping(req)
    
    def coordinates(self, data):
        req = Request(data=str(data), id = self.clientid)
        #print("test1")
        reqs = self.stub.coordinates(req)                
        for req in reqs:
            yield req

    def callping(self):
        resp = self.ping("ping")
        print(resp.data)
        self.clientid = resp.id

    def call(self):
        res = self.coordinates("data")
        for r in res:
            if r.change == True:
                if self.clientid == r.id:
                    print("[received] Move To = {}".format(r.data))
       
def test(cmdargs):
    #print(sys.argv[1])
    client = PingClient(cmdargs)
    client.callping()
    while 1:
        try:
            client.call()
        except:
            continue
        time.sleep(0.1)
    
        
if __name__ == '__main__':
    cmdargs = str(sys.argv[1])
    test(cmdargs)