from flask import Blueprint, request, flash, redirect, url_for, g, render_template
from .auth import login_required
from .models import Post
from creditrisk import db

bp = Blueprint('cartera',__name__, url_prefix = '/cartera')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('cartera/dashboard.html')