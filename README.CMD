python3 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. ping.proto 

python3 server.py 0,0,0 10,0,0

Server started at 3000.
Enter New Cooridnate[x, y, z] > 

python3 client.py 3000 

Client id [xxxx] connected to the server.
[received] moving to [0, 0, 0]

Client id [xxxx] connected to the server.
[received] moving to [10, 0, 0]