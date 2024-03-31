from flask import Blueprint, request, flash, redirect, url_for, g, render_template
from .auth import login_required
from creditrisk import db
import pandas as pd
import os

bp = Blueprint('cartera',__name__, url_prefix = '/cartera')
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = "static/uploads"

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('cartera/dashboard.html')

@bp.route('/cargar_reporte', methods=('GET','POST'))
def cargar_reporte():
    if request.method == 'POST':
        print("vamos a mover el csv")
        uploaded_file = request.files['file']
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        print(uploaded_file)
        print("Dirección actual del archivo:      ", dir_actual)
        if uploaded_file:
            file_path = os.path.join(dir_actual+"/"+UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

        return render_template('cartera/cargar_reporte.html')
    
    return render_template('cartera/cargar_reporte.html')