from flask import Flask, config, render_template, request

import sqlite3

conn = sqlite3.connect('../agro_drone.db')
cursor = conn.cursor()
sql_query = """ CREATE TABLE book(
    id integer PRIMARY KEY,
    author text NOT NULL
) """

cursor.execute(sql_query)



  