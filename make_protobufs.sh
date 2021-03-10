#!/bin/sh

protofile=client_services
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protobufs/${protofile}.proto

cp protobufs/${protofile}_pb2.py ./server/generated
cp protobufs/${protofile}_pb2_grpc.py ./server/generated

mv protobufs/${protofile}_pb2.py ./client
mv protobufs/${protofile}_pb2_grpc.py ./client

protofile=node_services
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protobufs/${protofile}.proto

mv protobufs/${protofile}_pb2.py ./server/generated
mv protobufs/${protofile}_pb2_grpc.py ./server/generated