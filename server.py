import time
import grpc
import ping_pb2
import ping_pb2_grpc
import sys

from concurrent import futures

index_client_counter = 1

class PingServer(ping_pb2_grpc.PingPongServicer):
    def __init__(self):
        self.client_dict = {}
        self.distance = 0
        self.cord_update = {}
        self.dic_count = 0

    def serverstart(self,cord):
        self.dic_count = self.dic_count + 1
        self.client_dict[self.dic_count] = str(cord)
        if self.dic_count == 2:
            dist = self.client_dict[self.dic_count].split(",")
            self.distance = dist[0]
        
        self.cord_update[self.dic_count] = False
        #print(self.cord_update)

    def updateCoordinates(self,cord1):
        self.client_dict[1] = str(cord1) 
        self.cord_update[1] = True  
        cnt = 2        
        while cnt < (len(self.client_dict)+1):
            #print(self.distance)
            self.cord_update[cnt] = True
            cord = str(self.client_dict[cnt-1]).split(",")
            #print(cord)
            x = int(cord[0]) + int(self.distance)
            y = cord[1]
            z = cord[2]
            s = ""
            s += str(x) + ',' + y + ',' + z
            self.client_dict[cnt] = s
            cnt = cnt+1
            #print(self.cord_update[cnt])     
        

    def ping(self,request, context):
        global index_client_counter

        if index_client_counter == 1:           
            ret = "Client id {} connected to server.\n[received] moving to {}".format(index_client_counter, str(self.client_dict[index_client_counter]))
            id = index_client_counter
        else :
            ret = "Client id {} connected to server.\n[received] moving to {}".format(index_client_counter, self.client_dict[index_client_counter])
            id = index_client_counter
        index_client_counter = index_client_counter + 1
         
        return ping_pb2.Response(data=ret,id=id)
    
    def coordinates(self, request, context):       
        for x in self.client_dict:
            if(x == request.id):
                yield ping_pb2.Response(data = str(self.client_dict[x]),change = self.cord_update[x], id = x)
                self.cord_update[x] = False
    
def run(host, port, coordinates):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ps = PingServer() 
    ping_pb2_grpc.add_PingPongServicer_to_server(ps, server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    try:
        while True:
            
            print("Server started at %d." % port)
            
            parmeter = 1
            for cnt in range(1, len(sys.argv)):
                #print(sys.argv[parmeter])
                ps.serverstart(sys.argv[parmeter])
                parmeter = parmeter + 1

            #print("started")
            while 1 :
                val = input("Enter new Coordinates[x,y,z]>")
                if val == "quit" :
                    break
                try :
                    ps.updateCoordinates(val)                                  
                except:
                    continue
                time.sleep(0.1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    cmdargs = str(sys.argv)
    run('0.0.0.0', 3000, cmdargs)