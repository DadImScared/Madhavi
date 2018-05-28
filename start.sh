#!/bin/bash

exec gunicorn run:app \
    --bind 0.0.0.0:8000 \
    --workers 3