from app import app
from flask import Flask, jsonify, render_template
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/matrix')
def matrix():
    return render_template('matrix.html')