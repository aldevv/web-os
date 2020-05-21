#!/bin/bash

source env/bin/activate
cd backend
gunicorn run:api --log-level debug --worker-class gevent
