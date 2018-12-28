#!/usr/bin/bash
ps aux | grep python | grep trans.py | grep -v grep | awk '{print $2}' | head -1 | xargs kill -9

