from creditrisk import db
from datetime import datetime
class Evaluation(db.Model):
    """
        "edad","codigopostal","tipovivienda","dependientes","estadocivil","genero","claveactividad","nivelacademico",
        "telefono","ingreso","egreso","tipoprestamo","tasanormal","tasamoratoria","monto","avales","creditostrabajados",
        "bien","montogarantia","finalidad","remesas","plazo","target"
    """
    __tablename__ = 'evaluation'
    id_evaluation = db.Column(db.Integer, primary_key=True)

    edad = db.Column(db.Integer, nullable = False)
    codigopostal = db.Column(db.Integer, nullable = False)
    tipovivienda = db.Column(db.Integer, nullable = False)
    dependientes = db.Column(db.Integer, nullable = False)
    estadocivil = db.Column(db.Integer, nullable = False)
    genero = db.Column(db.Integer, nullable = False)
    ocupacion = db.Column(db.String(12), nullable = False)
    nivelacademico = db.Column(db.Integer, nullable = False)
    telefono = db.Column(db.Integer, nullable = False)
    ingreso = db.Column(db.Numeric, nullable = False)
    egreso = db.Column(db.Numeric, nullable = False)
    tipoprestamo = db.Column(db.Integer, nullable = False)
    tasanormal = db.Column(db.Numeric, nullable = False)
    tasamoratoria = db.Column(db.Numeric, nullable = False)
    monto = db.Column(db.Numeric, nullable = False)
    avales = db.Column(db.Integer, nullable = False)
    creditostrabajados = db.Column(db.Integer, nullable = False)
    bien  = db.Column(db.Integer, nullable = False)
    montogarantia = db.Column(db.Numeric, nullable = False)
    finalidad = db.Column(db.Integer, nullable = False)
    remesas = db.Column(db.Integer, nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    # otros campos necesarios para la evaluación    
    evaluador = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    nombrecompleto = db.Column(db.String(200), nullable = False)
    domicilio = db.Column(db.String(200), nullable = False) 
    fechaevaluation = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    
    

    

    def __init__(self, evaluador, nombrecompleto, domicilio, edad,  codigopostal, tipovivienda, dependientes, estadocivil, genero,
                 ocupacion, nivelacademico, telefono, ingreso, egreso, tipoprestamo, tasanormal, tasamoratoria, monto, avales, creditostrabajados,
                 bien, montogarantia, finalidad, remesas, plazo, fechaevaluation):
        self.evaluador = evaluador
        self.nombrecompleto = nombrecompleto
        self.domicilio = domicilio
        self.fechaevaluation = fechaevaluation
        self.edad = edad
        self.codigopostal = codigopostal
        self.tipovivienda = tipovivienda
        self.dependientes = dependientes
        self.estadocivil = estadocivil
        self.genero = genero
        self.ocupacion = ocupacion
        self.nivelacademico = nivelacademico
        self.telefono = telefono
        self.ingreso = ingreso
        self.egreso = egreso
        self.tipoprestamo = tipoprestamo
        self.tasanormal = tasanormal
        self.tasamoratoria = tasamoratoria
        self.monto = monto
        self.avales = avales
        self.creditostrabajados = creditostrabajados
        self.bien = bien
        self.montogarantia = montogarantia
        self.finalidad = finalidad
        self.remesas = remesas
        self.plazo = plazo
        

    def __repr__(self):
        return f"Evaluation: '{self.evaluador}' '{self.nombrecompleto}' '{self.domicilio}' '{self.edad}' '{self.codigopostal}' '{self.tipovivienda}' '{self.dependientes}' '{self.estadocivil}' '{self.genero}' '{self.ocupacion}' '{self.nivelacademico}' '{self.telefono}' '{self.ingreso}' '{self.egreso}' '{self.tipoprestamo}' '{self.tasanormal}' '{self.tasamoratoria}' '{self.monto}' '{self.avales}' '{self.creditostrabajados}' '{self.bien}' '{self.montogarantia}' '{self.finalidad}' '{self.remesas}' '{self.plazo}'   "
class TipoPrestamo(db.Model):
    __tablename__ = 'dic_tipoprestamo'
    id = db.Column(db.Integer, primary_key=True)
    tipoprestamo = db.Column(db.String(10), nullable = False)
    desc_tipoprestamo = db.Column(db.String(150), nullable = False)
    tasa_normal = db.Column(db.Integer)
    tasa_mora = db.Column(db.Integer)
    finalidad = db.Column(db.String(20))

    def __init__(self, tipoprestamo, desc_tipoprestamo, tasa_normal, tasa_mora, finalidad):
        self.tipoprestamo = tipoprestamo
        self.desc_tipoprestamo = desc_tipoprestamo
        self.tasa_normal = tasa_normal
        self.tasa_mora = tasa_mora
        self.finalidad = finalidad

    def __repr__(self):
        return f"TipoPrestamo: '{self.tipoprestamo}' '{self.desc_tipoprestamo}"
class Finalidad(db.Model):
    __tablename__ = 'dic_finalidad'
    id = db.Column(db.Integer, primary_key=True)
    finalidad = db.Column(db.String(10), nullable = False)

    def __init__(self, finalidad):
        self.finalidad = finalidad

    def __repr__(self):
        return f"Finalidad: '{self.finalidad}'"
class TipoVivienda(db.Model):
    __tablename__ = 'dic_tipovivienda'
    id = db.Column(db.Integer, primary_key=True)
    tipovivienda = db.Column(db.String(20), nullable = False)

    def __init__(self, tipovivienda):
        self.tipovivienda = tipovivienda

    def __repr__(self):
        return f"tipovivienda: '{self.tipovivienda}'"
class NivelAcademico(db.Model):
    __tablename__ = 'dic_nivelacademico'
    id = db.Column(db.Integer, primary_key=True)
    nivelacademico = db.Column(db.String(20), nullable = False)

    def __init__(self, nivelacademico):
        self.nivelacademico = nivelacademico

    def __repr__(self):
        return f"NivelAcademico: '{self.nivelacademico}'"
class EstadoCivil(db.Model):
    __tablename__ = 'dic_estadocivil'
    id = db.Column(db.Integer, primary_key=True)
    estadocivil = db.Column(db.String(20), nullable = False)

    def __init__(self, estadocivil):
        self.estadocivil = estadocivil

    def __repr__(self):
        return f"User: '{self.estadocivil}'"
class Bien(db.Model):
    __tablename__ = 'dic_bien'
    id = db.Column(db.Integer, primary_key=True)
    bien = db.Column(db.String(20), nullable = False)

    def __init__(self, bien):
        self.bien = bien

    def __repr__(self):
        return f"bien: '{self.bien}'"
class Entidad(db.Model):
    __tablename__ = 'entidad'
    entidad_id = db.Column(db.Integer, primary_key=True)
    entidad_name = db.Column(db.String(150), unique = True, nullable = False)
    entidad_abre = db.Column(db.String(50), unique = True, nullable = False)
    entidad_photo = db.Column(db.String(200))
    entidad_domicilio = db.Column(db.Text, nullable = False)
    entidad_telefono = db.Column(db.Text, nullable = False)
    entidad_modelo = db.Column(db.String(200))

    def __init__(self, entidad_name, entidad_abre, entidad_domicilio, entidad_telefono, entidad_modelo, entidad_photo = None):
        self.entidad_name = entidad_name
        self.entidad_abre = entidad_abre
        self.entidad_domicilio = entidad_domicilio
        self.entidad_telefono = entidad_telefono
        self.entidad_photo = entidad_photo
        self.entidad_modelo = entidad_modelo

    def __repr__(self):
        return f"Entidad: '{self.entidad_name}'"
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    photo = db.Column(db.String(200))
    entidad = db.Column(db.Integer, db.ForeignKey('entidad.entidad_id'), nullable = True)

    def __init__(self, username, email, password, photo = None):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo

    def __repr__(self):
        return f"User: '{self.username}'"
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    url = db.Column(db.String(100), unique = True, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, author, url, title, info, content) -> None:
       self.author = author
       self.url = url
       self.title = title
       self.info = info
       self.content = content

    def __repr__(self) -> str:
        return f'Post: {self.title}'
class ActividadSiti(db.Model):
    __tablename__ = 'actividad_siti'
    actividadid = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(120))
    nivelriesgo = db.Column(db.Integer)

    def __init__(self, actividadid, nombre, siti_no, nivelriesgo):
        self.actividadid = actividadid
        self.nombre = nombre
        self.nivelriesgo = nivelriesgo

    def __repr__(self):
        return f"ActividadSiti: '{self.actividadid}' '{self.nombre}'"
class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key = True)
    idvalidacion = db.Column(db.Integer, db.ForeignKey('evaluation.id_evaluation'), nullable = False)
    dateevaluation = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    dt_class0 = db.Column(db.Numeric, nullable = False)
    dt_class1 = db.Column(db.Numeric, nullable = False)
    rnn_class0 = db.Column(db.Numeric, nullable = False)
    rnn_class1 = db.Column(db.Numeric, nullable = False)
    svm_class0 = db.Column(db.Numeric, nullable = False)
    svm_class1 = db.Column(db.Numeric, nullable = False)
    rl_class0 = db.Column(db.Numeric, nullable = False)
    rl_class1 = db.Column(db.Numeric, nullable = False)
    xgboost_class0 = db.Column(db.Numeric, nullable = False)
    xgboost_class1 = db.Column(db.Numeric, nullable = False)
    grupo = db.Column(db.Integer, default=0)
    
    def __init__(self, id, idvalidacion, dateevaluation, dt_class0, dt_class1, rnn_class0, rnn_class1, svm_class0, svm_class1, rl_class0, rl_class1, xgboost_class0, xgboost_class1, grupo):
        self.id = id
        self.idvalidacion = idvalidacion
        self.dateevaluation = dateevaluation
        self.dt_class0 = dt_class0
        self.dt_class1 = dt_class1
        self.rnn_class0 = rnn_class0
        self.rnn_class1 = rnn_class1
        self.svm_class0 = svm_class0
        self.svm_class1 = svm_class1
        self.rl_class0 = rl_class0
        self.rl_class1 = rl_class1
        self.xgboost_class0 = xgboost_class0
        self.xgboost_class1 = xgboost_class1
        self.grupo = grupo
    def __repr__(self):
        return f"prediction: '{self.id} {self.idvalidacion}' "

############ vamos a checar conexión con la base de datos de EIZ
class eiz_Tipocredito(db.Model):
    __bind_key__ = 'eiz001'
    __tablename__ = 'tipocredito'
    tipoprestamoid = db.Column(db.String(3), primary_key=True)
    desctipoprestamo = db.Column(db.String(30))
    finalidad = db.Column(db.Integer)
    tasa_normal = db.Column(db.Integer)
    tasa_mora = db.Column(db.Integer)

    def __init__(self, tipoprestamoid, desctipoprestamo, finalidad, tasa_normal, tasa_mora):
        self.tipoprestamoid = tipoprestamoid
        self.desctipoprestamo = desctipoprestamo
        self.finalidad = finalidad
        self.tasa_normal = tasa_normal
        self.tasa_mora = tasa_mora
class eiz_Finalidades(db.Model):
    __bind_key__ = 'eiz001'
    __tablename__ = 'finalidades'
    finalidadid = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text)

    def __init__(self, finalidadid, descripcion):
        self.finalidadid = finalidadid
        self.descripcion = descripcion
class eiz_Estadocivil(db.Model):
    __bind_key__ = 'eiz001'
    __tablename__ = 'estadocivil'
    estadocivilid = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(15), nullable = False)

    def __init__(self, estadocivilid, descripcion):
        self.estadocivilid = estadocivilid
        self.descripcion = descripcion
class eiz_Actividadsiti(db.Model):
    __bind_key__ = 'eiz001'
    __tablename__ = 'actividades_economicas_siti'
    actividadid = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(120))
    siti_no = db.Column(db.Integer)
    nivelriesgo = db.Column(db.Integer)

    def __init__(self, actividadid, nombre, siti_no, nivelriesgo):
        self.actividadid = actividadid
        self.nombre = nombre
        self.siti_no = siti_no
        self.nivelriesgo = nivelriesgo

    def __repr__(self):
        return f"ActividadSiti: '{self.actividadid}' '{self.nombre}'"
class eiz_Nivelacademico(db.Model):
    __bind_key__ = 'eiz001'
    __tablename__ = 'nivelacademico'
    nivelacademicoid = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(20), nullable = False)

    def __init__(self, nivelacademicoid, descripcion):
        self.nivelacademicoid = nivelacademicoid
        self.descripcion = descripcion

    def __repr__(self):
        return f"NivelAcademico: '{self.nivelacademicoid}'"
