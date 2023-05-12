#!/bin/bash

# Change to working directory
cd /Users/BrendanInglis/PycharmProjects/MindfulNotis

# Activate virtual environment
source venv/bin/activate

# Run notification scripts
python3 SpotiMind.py >/tmp/stout2.log 2>/tmp/stderr2.log
wait

python3 MindfulNotis.py >/tmp/stdout.log 2>/tmp/stderr.log
wait

# Clean up
deactivate
cd ~
