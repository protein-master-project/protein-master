from app import app
from flask import Flask, jsonify, render_template
@app.route('/molstar')
def index():
    return render_template('molstar.html')


@app.route('/matrix')
def matrix():
    return render_template('matrix.html')