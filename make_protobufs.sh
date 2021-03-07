#!/bin/sh

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protobufs/node_messages.proto

cp protobufs/node_messages_pb2_grpc.py ./server
mv protobufs/node_messages_pb2_grpc.py ./client

cp protobufs/node_messages_pb2.py ./server
mv protobufs/node_messages_pb2.py ./client