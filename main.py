from flask import Flask, jsonify, make_response, request, render_template, redirect, url_for, flash
from app import app

if __name__ == '__main__':
    app.run(debug=True)