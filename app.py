import datetime
import os

from flask import Flask, session, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
import re

from app import app

from flask_cors import CORS

CORS(app)

@app.before_request
def make_session_permanent():
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)

if __name__ == '__main__':
    app.run(debug=True)
