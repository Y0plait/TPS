from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

from app import index_search, configuration, features
