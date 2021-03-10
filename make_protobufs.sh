#!/bin/sh

protofile=client_services
python -m grpc_tools.protoc --proto_path=protobufs --python_out=./server/generated --grpc_python_out=./server/generated ${protofile}.proto
python -m grpc_tools.protoc --proto_path=protobufs --python_out=./client/generated --grpc_python_out=./client/generated ${protofile}.proto

# cp ${protofile}_pb2.py ./server/generated
# cp ${protofile}_pb2_grpc.py ./server/generated

# mv ${protofile}_pb2.py ./client
# mv ${protofile}_pb2_grpc.py ./client

protofile=node_services
python -m grpc_tools.protoc --proto_path=protobufs --python_out=./server/generated --grpc_python_out=./server/generated ${protofile}.proto

# mv ${protofile}_pb2.py ./server/generated
# mv ${protofile}_pb2_grpc.py ./server/generated