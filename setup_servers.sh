#!/bin/sh

# Set Session Name
SESSION="Server"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

PORT=$1
if [ "$PORT" = "1024"]
then
    IP=$(ifconfig eth2 | grep "inet " | awk '{print $2}')
else
    IP=$(ifconfig eth1 | grep "inet " | awk '{print $2}')
fi

# Only create tmux session if it doesn't already exist
if [ "$SESSIONEXISTS" = "" ]
then
    # Start New Session with our name
    tmux new-session -d -s $SESSION

    # Name first Pane and setup pane for server 1
    tmux rename-window -t 0 'Server1'
    tmux send-keys -t 'Server1' "python3 server/main.py $IP $PORT" C-m

    sleep 1

    # Create and setup pane for server 2
    tmux new-window -t $SESSION:1 -n 'Server2'
    tmux send-keys -t 'Server2' "python3 server/main.py $IP $((PORT + 1))" C-m
fi

# Attach Session, on the Main window
tmux attach-session -t $SESSION:0