#!/bin/bash

# Load the .env file from the specified path
if [ -f /home/preangel/Expenditure_bot/.env ]; then
    export $(grep -v '^#' /home/preangel/Expenditure_bot/.env | xargs)
else
    echo ".env file not found at /home/preangel/Expenditure_bot/.env"
    exit 1
fi

# Connect to MySQL
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -P $DB_PORT $DB_NAME
