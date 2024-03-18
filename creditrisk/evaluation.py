from flask import Blueprint, request, flash, redirect, url_for, g, render_template, jsonify, json, Response
from .auth import login_required
from .models import TipoVivienda, Evaluation, Finalidad, TipoPrestamo, NivelAcademico, EstadoCivil, ActividadSiti, Bien, Prediction
from creditrisk import db
import numpy as np

from .pdf import PDF
bp = Blueprint('evaluation', __name__, url_prefix = '/evaluation')
from flask_paginate import Pagination, get_page_parameter # esto según es para la pagination 


"""
    Vamos a cargar los modelos de machine learning
"""
import joblib
import pandas as pd
import tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
#from keras.wrappers.scikit_learn import KerasClassifier

from hyperopt import hp, fmin, tpe, STATUS_OK, Trials
from sklearn.model_selection import cross_val_score, StratifiedKFold

from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score

from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

scaler = joblib.load('./creditrisk/static/modeloml/scaler.save')
kmeans = joblib.load('./creditrisk/static/modeloml/kmeans.pkl')
pca = joblib.load('./creditrisk/static/modeloml/pca.pkl')


"""
    [
        'edad' = X                             'codigopostal' = X
        'tipovivienda' = X                     'dependientes' = X
        'estadocivil'  = X                     'genero' = X
        'claveactividad' =                     'nivelacademico' = X
        'telefono' =                           'ingreso' = X
        'egreso' = X                           'tipoprestamo' = X
        'tasanormal' = X                       'tasamoratoria' = X
        'monto' =  X                           'avales' =
        'creditostrabajados' =                'bien' =
        'montogarantia' =                     'finalidad' = X
        'remesas' = X                         'plazo' = X
    ]
"""

@bp.route('/evaluations')
@login_required
def evaluations():
    # esta es la primera versión ---> estoy revisando el apartado de mostrarlo por pagination
    """
        evaluations = Evaluation.query.all()
        for eval in evaluations:
            print("Nombre:   ", eval.nombrecompleto,   " ", eval.fechaevaluation )
            eval.fechaevaluation = str(eval.fechaevaluation)[:16]
        return render_template('evaluation/evaluations.html', evaluations = evaluations)
    """

    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    evaluations = Evaluation.query.filter_by(evaluador = g.user.id)
    total_evaluations = 0
    for eval in evaluations:
        print("Nombre:   ", eval.nombrecompleto,   " ", eval.fechaevaluation )
        eval.fechaevaluation = str(eval.fechaevaluation)[:16]
        total_evaluations = total_evaluations + 1

    print("Total Evaluaciones:    ------>  ", total_evaluations, "       ----------->    ", g.user.id )
    pagination = Pagination(page=page, total=total_evaluations, search=search, record_name='evaluations')
    # 'page' is the default name of the page parameter, it can be customized
    # e.g. Pagination(page_parameter='p', ...)
    # or set PAGE_PARAMETER in config file
    # also likes page_parameter, you can customize for per_page_parameter
    # you can set PER_PAGE_PARAMETER in config file
    # e.g. Pagination(per_page_parameter='pp')


    return render_template('evaluation/evaluations.html', evaluations = evaluations, pagination=pagination)
    

@bp.route('/evaluations_tipoprestamo/<tipoprestamoid>')
@login_required
def evaluations_tipoprestamo(tipoprestamoid):
    print("tipoprestamo impresion", tipoprestamoid)
    tipoprestamo = TipoPrestamo.query.filter_by(id = tipoprestamoid).all()

    TipoPrestamo_Filtrado = []
    for tipo in tipoprestamo:
        Obj = {}
        Obj['id'] = tipo.id
        Obj['finalidad'] = tipo.finalidad
        Obj['tasa_normal'] = tipo.tasa_normal
        Obj['tasa_mora'] = tipo.tasa_mora
        TipoPrestamo_Filtrado.append(Obj)

    print("TipoPrestamo:         ", TipoPrestamo_Filtrado)

    return jsonify(TipoPrestamo_Filtrado)

@bp.route('/create_evaluation', methods=('GET','POST'))
@login_required
def create_evaluation():
    tipoviviendas = TipoVivienda.query.all()
    finalidades = Finalidad.query.all()
    #tipoprestamos = TipoPrestamo.query.all()
    tipoprestamos = TipoPrestamo.query.filter(TipoPrestamo.desc_tipoprestamo != None).all()
    nivelacademicos = NivelAcademico.query.all()
    estadociviles = EstadoCivil.query.all()
    ocupaciones = ActividadSiti.query.all()
    bienes = Bien.query.all()
    if request.method == 'POST':

        nombrecompleto = request.form.get('nombrecompleto')
        domicilio = request.form.get('domicilio')
        edad = request.form.get('edad')
        codigopostal = request.form.get('codigopostal')
        tipovivienda = request.form.get('tipovivienda')
        dependientes = request.form.get('dependientes')
        estadocivil = request.form.get('estadocivil')
        genero = request.form.get('genero')
        ocupacion = request.form.get('ocupacion')
        nivelacademico = request.form.get('escolaridad')
        telefono = request.form.get('telefono')
        ingreso = request.form.get('ingreso')
        egreso = request.form.get('egreso')
        tipoprestamo = request.form.get('tipoprestamo')
        tasanormal = request.form.get('interesnormal')
        tasamoratoria = request.form.get('interesmora')
        monto = request.form.get('monto')
        avales = request.form.get('avales') # falta agregar número de avales
        creditostrabajados = request.form.get('creditostrabajados')# falta agregar número de creditos trabajados
        bien = request.form.get('bien')
        montogarantia = request.form.get('montogarantia') # falta capturar montogarantía
        finalidad = request.form.get('finalidad')
        remesas = request.form.get('remesas')
        plazo = request.form.get('plazo')
        

        evaluacion = Evaluation(g.user.id, nombrecompleto, domicilio, edad, codigopostal, tipovivienda, dependientes, estadocivil, genero, ocupacion, nivelacademico, 
                                telefono, ingreso, egreso, tipoprestamo, tasanormal, tasamoratoria, monto, avales, creditostrabajados, bien, montogarantia, finalidad, 
                                remesas, plazo, None)
        print("ocupación:    ", ocupacion)
        print(evaluacion.__repr__)
        cad_evaluacion = np.array([[int(edad),int(codigopostal), int(tipovivienda), int(dependientes), int(estadocivil), int(genero), int(ocupacion), int(nivelacademico),
                         int(telefono), float(ingreso), float(egreso), int(tipoprestamo), float(tasanormal), float(tasamoratoria), float(monto), int(avales), int(creditostrabajados),
                         int(bien),float(montogarantia), int(finalidad),int(remesas), int(plazo)]])
        """
            "codigopostal","tipovivienda","dependientes","estadocivil","genero","claveactividad","nivelacademico",
            "telefono","ingreso","egreso","tipoprestamo","tasanormal","tasamoratoria","monto","avales","creditostrabajados",
            "bien","montogarantia","finalidad","remesas","plazo",
        """
        ## vamos a leer un registro para que lo podamos enviar a 
        # 2,7,2,0,2,1,9999999,4,1,0.0,1.0,0,0,5,1.0,2,0,1,10.0,2,0,0,0    --> malo
        # 2,7,2,0,2,2,9999999,2,1,0.0,1.0,190,4,5,3.0,1,12,1,10.0,2,0,0,1 --> bueno
        #persona = np.array([[2,7,2,0,2,1,9999999,4,1,0.0,1.0,0,0,5,1.0,2,0,1,10.0,2,0,0]])

        # ['codigopostal', 'tipovivienda', 'dependientes', 'claveactividad', 'tipoprestamo', 'tasanormal', 'avales', 'plazo']
        # Esto es para cuando usaba el cluster
        # columnas = ['codigopostal', 'tipovivienda', 'dependientes', 'claveactividad', 'tipoprestamo', 'tasanormal', 'avales', 'plazo']
        # persona = np.array([[int(codigopostal) ,int(tipovivienda), int(dependientes), int(ocupacion), int(tipoprestamo), float(tasanormal), int(avales), int(plazo)]])

        persona = cad_evaluacion
        print("Persona selección de caracaterísticas:    ",persona)
        print(persona.shape,len(persona) )
        persona_transform = scaler.transform(persona)[:1]  # normalizado de las variables
        print("Persona normalizada:    ",persona_transform)

        """
            # este apartado lo estaba ocupando con PCA para asignar grupos
            # convertir a pca el registro
            persona_pca = pca.transform(persona_transform)
            print("Persona PCA:     ",persona_pca)
            pca_persona = pd.DataFrame(data = persona_pca, columns=['pca1','pca2','pca3'])
            
            # Identificar el grupo al que pertenece la persona a evaluar
            grupo = kmeans.predict(persona_transform)
            grupo = pd.DataFrame(data= grupo)
            print("Grupo al que pertenece:    ",grupo)

            persona_transform = np.append(persona_transform,grupo[0][0])

            print("Grupo al que pertenece:    ",grupo[0][0])
            print("Persona a evaluar:         ",persona_transform)
        """

        #  Vamos a realizar la implementación con DT.
        # arbol = joblib.load("./creditrisk/static/modeloml/DecisionTree.pkl")
        linealregresion = joblib.load("./creditrisk/static/modeloml/RL.pkl")
        redesneuronales = keras.models.load_model('./creditrisk/static/modeloml/RNN.h5')
        svm = joblib.load("./creditrisk/static/modeloml/SVM.pkl")
        # xgboost = joblib.load("./creditrisk/static/modeloml/XGBoost.joblib")

        #pred_dt = arbol.predict(persona_transform.reshape(1,-1))
        pred_lr = linealregresion.predict(persona_transform.reshape(1,-1))
        #pred_rnn = redesneuronales.predict(persona_transform.reshape(1,-1))
        pred_svm = svm.predict(persona_transform.reshape(1,-1))
        # pred_xgboost = xgboost.predict(persona_transform.reshape(1,-1))


        #print("Predicción de la evaluación:     ", pred_dt, " " , pred_lr, " ", pred_rnn, " ", pred_svm, " ", pred_xgboost)
        # print("Predicción de la evaluación:     ", pred_dt, " " , pred_lr, " ", pred_svm, " ")
        print("Predicción de la evaluación:      " , pred_lr, " ", pred_svm, " ")
        # proba_dt = arbol.predict_proba(persona_transform.reshape(1,-1))
        proba_lr = linealregresion.predict_proba(persona_transform.reshape(1,-1))
        proba_rnn = redesneuronales.predict(persona_transform.reshape(1,-1))
        proba_svm = svm.predict(persona_transform.reshape(1,-1))
        # proba_xgboost = xgboost.predict_proba(persona_transform.reshape(1,-1))

        #print("Predicción de la evaluación:     ", pred_dt)
        #print("Predicción de la evaluación:     ", pred_dt[0], "    " , pred_svm[0], "    " , pred_lr[0])


        db.session.add(evaluacion)
        db.session.commit()
        # print("id nuevo de la alta    ------>  " + str(evaluacion.id_evaluation) , "     ", type(grupo[0][0]), "   ",grupo[0][0])
        print("id nuevo de la alta    ------>  " + str(evaluacion.id_evaluation) )
        new_evaluationid = evaluacion.id_evaluation

        new_prediction = Prediction.query.filter_by(idvalidacion = new_evaluationid).first()

        print(new_prediction.idvalidacion, new_prediction.id)

        group = 0
        #if grupo[0][0] == 1:
            #group = 1

        ### actualizar los campos para predicción
        prediction = Prediction.query.get_or_404(new_prediction.id)
        print("Imprimiendo prediccion -----> ",prediction)
        # prediction.dt_class0 = proba_dt[0][0]
        # prediction.dt_class1 = proba_dt[0][1]
        
        print("Probabilidad RNN:   ", proba_rnn[0][0], "     ", proba_rnn[0][1])
        print("Probabilidad SVM:   ", proba_svm, "     ", proba_svm)
        
        prediction.rnn_class0 = float(proba_rnn[0][0])
        prediction.rnn_class1 = float(proba_rnn[0][1])
        
        if proba_svm[0] == 0:
            prediction.svm_class0 = float(0)
            prediction.svm_class1 = float(1)
        else:
            prediction.svm_class1 = float(1)
            prediction.svm_class0 = float(0)

        prediction.rl_class0 = proba_lr[0][0]
        prediction.rl_class1 = proba_lr[0][1]
        prediction.grupo = group
        # prediction.xgboost_class0 = proba_xgboost[0][0]
        # prediction.xgboost_class1 = proba_xgboost[0][1]
        
        db.session.commit()
        return redirect(url_for('evaluation.evaluations'))

    return render_template('evaluation/create_evaluation.html', tipoviviendas = tipoviviendas, finalidades = finalidades, tipoprestamos = tipoprestamos, nivelacademicos = nivelacademicos, estadociviles = estadociviles, ocupaciones = ocupaciones, bienes = bienes)

@bp.route('/generarPDF/<int:id_evaluation>', methods = ('GET','POST'))
def generarPDF(id_evaluation):
    print("vamos a generar pdf")
    evaluation = Evaluation.query.filter_by(id_evaluation = id_evaluation)
    estadocivil = EstadoCivil.query.filter_by(id = evaluation[0].estadocivil)
    tipovivienda = TipoVivienda.query.filter_by(id = evaluation[0].tipovivienda) 
    actividadsiti = ActividadSiti.query.filter_by(actividadid = evaluation[0].ocupacion)
    escolaridad = NivelAcademico.query.filter_by(id = evaluation[0].nivelacademico)
    tipocredito = TipoPrestamo.query.filter_by(id = evaluation[0].tipoprestamo)
    finalidad = Finalidad.query.filter_by(id = evaluation[0].finalidad)
    bien = Bien.query.filter_by(id = evaluation[0].bien)
    prediction = Prediction.query.filter_by(idvalidacion = id_evaluation)

    genero = None
    telefono = None
    remesas = None
    nivelacademico = None
    if evaluation[0].genero == 1:
        genero = "Femenino"
    else: 
        genero = "Masculino"
    if evaluation[0].telefono == 0:
        telefono = "No"
    else:
        telefono = "Si"
    if evaluation[0].remesas == 0:
        remesas = "No"
    else:
        remesas = "Si"
    #### Generación del PDF
    pdf = PDF()

    # pasar variables
    pdf.getGenero(genero)
    pdf.getEstadocivill(estadocivil[0].estadocivil)
    pdf.getTipovivienda(tipovivienda[0].tipovivienda)
    pdf.getTelefono(telefono)
    pdf.getRemesas(remesas)
    pdf.getOcupacion(actividadsiti[0].nombre)
    pdf.getEscolaridad(escolaridad[0].nivelacademico)
    pdf.getTipoprestamo(tipocredito[0].desc_tipoprestamo)
    pdf.getFinalidad(finalidad[0].finalidad)
    pdf.getBien(bien[0].bien)
    pdf.getGrupo(prediction[0].grupo)
    class0 = (prediction[0].rl_class0 + prediction[0].svm_class0 + prediction[0].rnn_class0)/3
    class1 = (prediction[0].rl_class1 + prediction[0].svm_class1 + prediction[0].rnn_class1)/3
    pdf.getMoroso(class0)
    pdf.getNoMoroso(class1)


    pdf.set_title("Reporte de solicitud")
    pdf.set_author('Jules Verne')
    pdf.ReporteSocio(evaluation)
    #pdf.print_chapter(1, 'A RUNAWAY REEF', evaluation[0].nombrecompleto)
    #pdf.print_chapter(2, 'THE PROS AND CONS', evaluation[0].domicilio)
    #pdf.output('tuto3.pdf', 'F')
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=' + evaluation[0].nombrecompleto + '.pdf'})






















































    