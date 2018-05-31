from flask import render_template, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError

from wra import app
from wra import login_manager
from .models.Models import User, Exhibition, Artwork

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    exhibitions = Exhibition.query.limit(5).all()
    artworks = Artwork.query.all()
    return render_template('index.html', exhibitions=exhibitions, artworks=artworks)


@app.before_request
def before_request():
    g.user = current_user
