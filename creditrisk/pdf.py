from fpdf import FPDF
from .models import TipoVivienda, Evaluation, Finalidad, TipoPrestamo, NivelAcademico, EstadoCivil, ActividadSiti, Bien
import locale
title = 'Reporte solicitud - recomendación'
analisisG0 = "Analisis para el grupo 0"
analisisG1 = "Analisis para el grupo 1"

class PDF(FPDF):
    analisis = ""
    estadocivil = ""
    genero = ""
    tipovivienda = ""
    telefono = ""
    remesas = ""
    ocupacion = ""
    escolaridad = ""
    tipoprestamo = ""
    finalidad = ""
    bien = ""
    grupo = 0
    moroso = 0
    nomoroso = 0
    def getEstadocivill(self, estadocivil):
        self.estadocivil = estadocivil
    def getGenero(self, genero):
        self.genero = genero
    def getTipovivienda(self,tipovivienda):
        self.tipovivienda= tipovivienda
    def getTelefono(self, telefono):
        self.telefono = telefono
    def getRemesas(self, remesas):
        self.remesas = remesas
    def getOcupacion(self, ocupacion):
        self.ocupacion = ocupacion
    def getEscolaridad(self, escolaridad):
        self.escolaridad = escolaridad
    def getTipoprestamo(self, tipoprestamo):
        self.tipoprestamo = tipoprestamo
    def getFinalidad(self, finalidad):
        self.finalidad = finalidad
    def getBien(self, bien):
        self.bien = bien
    def getGrupo(self, grupo):
        self.grupo = grupo
    def getMoroso(self, moroso):
        self.moroso = moroso
    def getNoMoroso(self, nomoroso):
        self.nomoroso = nomoroso

    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calcular ancho del texto (title) y establecer posición
        w = self.get_string_width(title) + 6
        self.set_xy((210 - w) / 2, 20)
        # Colores del marco, fondo y texto
        self.set_draw_color(103,  51,   0)
        self.set_fill_color(255, 255, 255)
        self.set_text_color( 29, 137,  20)
        # Grosor del marco (1 mm)
        self.set_line_width(1)
        # Titulo
        self.cell(w, 9, title, 1, 1, 'C', 1)
        # Salto de línea
        self.ln(20)
        self.image('./creditrisk/static/img/yolo.png',20, 10, 22);

        # Moroso
        # Times 12
        self.set_text_color( 0, 0, 0)
        self.set_font('Times', '', 12)
        y = self.get_y() - 10 
        self.text(45, y , "Moroso:")
        self.set_xy(62, y - 5 )
        self.set_fill_color(206, 251, 248)
        self.cell(15, 6, str(self.truncate(self.moroso, 4)), 0, 1, 'L', 1)

        self.text(85, y , "No moroso:")
        self.set_xy(108, y - 5 )
        self.set_fill_color(206, 251, 248)
        self.cell(15, 6, str(self.truncate(self.nomoroso, 4)), 0, 1, 'L', 1)
        self.set_y(y+10)

    def footer(self):
        # Posición a 1.5 cm desde abajo
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Color de texto en gris
        self.set_text_color(128)
        # Numero de pagina
        self.cell(0, 10, 'Pág. ' + str(self.page_no()), 0, 0, 'C')
    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Color de fondo
        self.set_fill_color(29, 137, 20)
        # Titulo
        #self.cell(0, 6, 'Chapter %d : %s' % (num, label), 0, 1, 'L', 1)
        self.cell(0, 6, "Datos del solicitante", 0, 1, 'L', 1)
        # Salto de línea
        self.ln(4)
    def chapter_body(self, name):
        # Leer archivo de texto
        """
        with open(name, 'rb') as fh:
            txt = fh.read().decode('latin-1')
        """
        # Times 12
        self.set_font('Times', '', 12)
        # Emitir texto justificado
        self.multi_cell(0, 5, name)
        # Salto de línea
        self.ln()
        # Mención en italic -cursiva-
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')
    def DatosPersonales(self, evaluation):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Color de fondo
        self.set_fill_color(29, 137, 20)
        # Titulo
        self.cell(0, 6, "Datos del solicitante", 0, 1, 'L', 1)
        # Salto de línea
        self.ln(4)

        #Nombre del solicitante
        self.text(15, 65, "Nombre:")
        self.set_xy(35, 61)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, evaluation[0].nombrecompleto, 0, 1, 'L', 1)

        #Domicilio del solicitante
        self.text(15, 75, "Domicilio:")
        self.set_xy(35, 71)
        self.set_fill_color(206, 251, 248)
        self.multi_cell(0, 6, evaluation[0].domicilio + ", C.P. " + str(evaluation[0].codigopostal), fill=1)

        # Edad 
        self.text(15, 90, "Edad:")
        self.set_xy(35, 86)
        self.set_fill_color(206, 251, 248)
        self.cell(25, 6, str(evaluation[0].edad) + " años", 0, 1, 'L', 1)

        #  Estado civil
        self.text(65, 90, "Estado civil:")
        self.set_xy(90, 86)
        self.set_fill_color(206, 251, 248)
        self.cell(40, 6, self.estadocivil, 0, 1, 'L', 1)

        #  Género
        self.text(135, 90, "Género:")
        self.set_xy(155, 86)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, self.genero, 0, 1, 'L', 1)

        #  Tipo vivienda
        self.text(15, 100, "Tipo vivienda:")
        self.set_xy(42, 96)
        self.set_fill_color(206, 251, 248)
        self.cell(40, 6, self.tipovivienda, 0, 1, 'L', 1)

        #  Dependientes
        self.text(85, 100, "Dependientes:")
        self.set_xy(115, 96)
        self.set_fill_color(206, 251, 248)
        self.cell(10, 6, "   " + str(evaluation[0].dependientes), 0, 1, 'L', 1)

        #  Teléfono
        self.text(128, 100, "Teléfono:")
        self.set_xy(148, 96)
        self.set_fill_color(206, 251, 248)
        self.cell(10, 6, "   " +  self.telefono , 0, 1, 'L', 1)

        #  Remesas
        self.text(162, 100, "Remesas:")
        self.set_xy(185, 96)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, "   " +  self.remesas , 0, 1, 'L', 1)

        # Ocupacion
        self.text(15, 110, "Ocupación:")
        self.set_xy(38, 106)
        self.set_fill_color(206, 251, 248)
        self.multi_cell(70, 6, self.ocupacion.strip(), fill=1)

        #  Escolaridad
        self.text(114, 110, "Escolaridad:")
        self.set_xy(138, 106)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, " " +  self.escolaridad , 0, 1, 'L', 1)
    def DatosCredito(self, evaluation):
        self.ln(8)
        self.set_font('Arial', '', 12)
        self.set_fill_color(29, 137, 20)
        self.cell(0, 6, "Datos crediticio", 0, 1, 'L', 1)
        print("Valor de la posición y:    ", self.get_y())

        # Tipo prestamo
        y = self.get_y() + 8
        self.text(15, y , "Tipo préstamo:")
        self.set_xy(45, y - 5 )
        self.set_fill_color(206, 251, 248)
        self.cell(65, 6, self.tipoprestamo, 0, 1, 'L', 1)

        # Finalidad del crédito
        self.text(113, y , "Finalidad:")
        self.set_xy(133, y - 5 )
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, self.finalidad, 0, 1, 'L', 1)

        # Interes normal
        y = y + 8
        self.text(15, y, "Interes normal:")
        self.set_xy(45, y - 5)
        self.set_fill_color(206, 251, 248)
        self.cell(10, 6, " " + str(evaluation[0].tasanormal), 0, 1, 'L', 1)

        #  Interes moratorio
        self.text(60, y, "Interes moratorio:")
        self.set_xy(95, y -5)
        self.set_fill_color(206, 251, 248)
        self.cell(10, 6, " " +  str( evaluation[0].tasamoratoria ) , 0, 1, 'L', 1)

        # Monto
        self.text(108, y, "Monto:")
        self.set_xy(122, y - 5)
        self.set_fill_color(206, 251, 248)
        self.cell(30, 6, " " + str(locale.currency( evaluation[0].monto, grouping=True) ), 0, 1, 'L', 1)

        #  Plazo
        self.text(157, y, "Plazo:")
        self.set_xy(170, y -5)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, " " +  str(evaluation[0].plazo) + " mes (es)", 0, 1, 'L', 1)

        # Ingreso
        y = y + 8
        self.text(15, y, "Ingreso:")
        self.set_xy(33, y - 5)
        self.set_fill_color(206, 251, 248)
        self.cell(32, 6, " " + str(locale.currency( evaluation[0].ingreso, grouping=True) ), 0, 1, 'L', 1)

        # Egreso
        self.text(70, y, "Egreso:")
        self.set_xy(87, y -5)
        self.set_fill_color(206, 251, 248)
        self.cell(32, 6, " " +  str(locale.currency( evaluation[0].egreso, grouping=True) ) , 0, 1, 'L', 1)

        # Avales
        self.text(121, y, "Avales:")
        self.set_xy(137, y - 5)
        self.set_fill_color(206, 251, 248)
        self.cell(10, 6, " " + str(evaluation[0].avales), 0, 1, 'L', 1)

        # Historial
        self.text(150, y, "Historial:")
        self.set_xy(170, y -5)
        self.set_fill_color(206, 251, 248)
        self.cell(0, 6, " " + str(evaluation[0].creditostrabajados) + " créditos", 0, 1, 'L', 1)

        # Bien
        y = y + 8
        self.text(15, y, "Bien:")
        self.set_xy(28, y - 5)
        self.set_fill_color(206, 251, 248)
        self.multi_cell(70, 6, self.bien.strip(), fill=1)

        # Monto garantía
        self.text(105, y, "Valor garantía:")
        self.set_xy(134, y - 5)
        self.set_fill_color(206, 251, 248)
        self.cell(30, 6, "   " + str(locale.currency(evaluation[0].montogarantia, grouping=True) ), 0, 1, 'L', 1)
    def AnalisisCredito(self, evaluation):
        self.ln(4)
        self.set_font('Arial', '', 12)
        self.set_fill_color(29, 137, 20)
        self.cell(0, 6, "Análisis del socio", 0, 1, 'L', 1)
        print("Valor de la posición y:    ", self.get_y())
        # Salto de línea
        y = self.get_y()
        self.ln(20)
        if self.grupo == 0:
            self.image('./creditrisk/static/img/grupo0.png', 10, y + 5, 100);
            self.analisis = analisisG0
        else:
            self.image('./creditrisk/static/img/grupo1.png', 10, y + 5, 100);
            self.analisis = analisisG1

        y = y + 5
        # Analisis 
        self.text(140, y, "Analisis:")
        self.set_xy(110, y+2)
        self.set_fill_color(206, 251, 248)
        self.multi_cell(0, 6, self.analisis, fill=1)



    def ReporteSocio(self, evaluation):
        # Imprimir encabezado del reporte
        self.add_page()
        self.DatosPersonales(evaluation)
        self.DatosCredito(evaluation)
        #self.AnalisisCredito(evaluation)



    def print_chapter(self, num, title, name):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(name)

    def truncate(self, number: float, max_decimals: int) -> float:
        int_part, dec_part = str(number).split(".")
        return float(".".join((int_part, dec_part[:max_decimals])))