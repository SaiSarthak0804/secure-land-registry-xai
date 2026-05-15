import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        database="land_registry_db",
        user="postgres",
        password="postgresgrp8"
    )

    cursor = connection.cursor()

    print("Database connected successfully!")

except Exception as error:
    print("Error while connecting to database:", error)