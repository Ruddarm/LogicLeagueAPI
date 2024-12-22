#!/bin/bash

# Run database migrations
python manage.py migrate

# Start the Django server in the background
python manage.py runserver 0.0.0.0:8000 &

# Start Node.js server (if applicable)
if [ -f "server.js" ]; then
    node server.js &
fi

# Keep the container running
tail -f /dev/null
