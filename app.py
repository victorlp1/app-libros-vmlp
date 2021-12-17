from logging import debug
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qbcgdxsrlyzewl:0070fd6aedee3c831c3001ff99cf11da64a89c1b7894a7a7d1cbf50f02bccb48@ec2-54-225-203-79.compute-1.amazonaws.com:5432/d60a3dvsnlj9p6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
####CLASES DATABASE ################################
class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __int__(self, email, password):
        self.email=email
        self.password=password


class Editorial(db.Model):
    __tablename__="editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(80))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(50))

    def __init__(self, nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    #Relacion
    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial, id_autor, id_genero):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_editorial = id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero


class Misfavoritos(db.Model):
    __tablename__ = "misfavoritos"
    id_favoritos = db.Column(db.Integer, primary_key=True)

    #Relacion
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))

    def __init__(self, id_libro, id_usuario):
        self.id_libro = id_libro
        self.id_usuario = id_usuario

####################################################################


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]

    consulta_usuario = Usuarios.query.filter_by(email=email).first()
    print(consulta_usuario.email)
    bcrypt.check_password_hash(consulta_usuario.password,password)

    return render_template("login.html")

@app.route("/registrar")
def registrar():
    return render_template("registro.html")



@app.route("/registrar_usuario", methods=['POST'])
def registrar_usuario():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)
    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)
    usuario = Usuarios(email = email, password=password_cifrado)
    db.session.add(usuario)
    db.session.commit()
    return render_template("login.html")


#######Registrar Editorial############
@app.route("/editorial")
def editorial():
    return render_template("editorial.html")

@app.route("/registrarEditorial", methods=['POST'])
def registrar_editorial():
    nombre_editorial = request.form["nombre_editorial"]

    editorial_nuevo = Editorial(nombre_editorial=nombre_editorial)
    db.session.add(editorial_nuevo)
    db.session.commit()
    return redirect("/leereditorial")


#######Registrar Autor############
@app.route("/autor")
def autor():
    return render_template("autor.html")

@app.route("/registrarAutor", methods=['POST'])
def registrar_autor():
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]

    autor_nuevo = Autor(nombre_autor=nombre_autor, fecha_nac=fecha_nac, nacionalidad=nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    return redirect("/leerautores")


#######Registrar Genero############
@app.route("/genero")
def genero():
    return render_template("genero.html")

@app.route("/registrarGenero", methods=['POST'])
def registrar_genero():
    nombre_genero = request.form["nombre_genero"]

    genero_nuevo = Genero(nombre_genero=nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    return redirect("/leergenero")



#### CRUD LIBROS ###################################
@app.route("/libro")
def libro():
    consulta_editorial = Editorial.query.all()
    consulta_genero = Genero.query.all()
    consulta_autor = Autor.query.all()
    return render_template("libro.html", consulta_editorial=consulta_editorial, consulta_genero=consulta_genero, consulta_autor=consulta_autor)

@app.route("/registrarLibro", methods=["POST"])
def registrarLibro():
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    id_editorial=request.form["editorial"]
    id_genero=request.form["genero"]
    id_autor=request.form["autor"]

    numero_paginas_int = int(numero_paginas)
    libro_nuevo = Libro(titulo_libro=titulo_libro, fecha_publicacion=fecha_publicacion, numero_paginas=numero_paginas_int,formato=formato,volumen=volumen,id_editorial=id_editorial,id_genero=id_genero,id_autor=id_autor)
    db.session.add(libro_nuevo)
    db.session.commit()

    return redirect("/libro_lista")
    
##########funciones de libro######
@app.route("/eliminar_libro/<ID>")
def eliminar(ID):
    libro = Libro.query.filter_by(id_libro = int(ID)).delete()
    print(libro)
    db.session.commit()
    return redirect("/libro_lista")

@app.route("/editar_libro/<ID>")
def editar_libro(ID):
    libro = Libro.query.filter_by(id_libro=int(ID)).first()
    consulta_autor = Autor.query.all()
    consulta_editorial = Editorial.query.all()
    consulta_genero = Genero.query.all()
  
    return render_template("modificarlibro.html", libro = libro, consulta_autor=consulta_autor, consulta_editorial=consulta_editorial, consulta_genero=consulta_genero)


@app.route("/modificar_libro", methods=['POST'])
def modificarlibro():
    idlibro = request.form['idlibro']
    titulo_libro = request.form['titulo_libro']
    fecha_publicacion = request.form['fecha_publicacion']
    numero_paginas = request.form['numero_paginas']
    formato = request.form['formato']
    volumen = request.form['volumen']
    id_editorial=request.form['editorial']
    id_genero=request.form['genero']
    id_autor=request.form['autor']

    libro = Libro.query.filter_by(id_libro=int(idlibro)).first()
    libro.titulo_libro = titulo_libro
    libro.fecha_publicacion = fecha_publicacion
    libro.numero_paginas = numero_paginas
    libro.formato = formato
    libro.volumen = volumen
    libro.id_editorial = id_editorial
    libro.id_autor = id_autor
    libro.id_genero = id_genero
    db.session.commit()

    return redirect("/libro_lista")

@app.route("/libro_lista")
def libro_lista():
    consulta_libro = Libro.query.join(Genero, Libro.id_genero == Genero.id_genero).join(Autor, Libro.id_autor == Autor.id_autor).join(Editorial, Libro.id_editorial == Editorial.id_editorial).add_columns(Genero.nombre_genero, Libro.titulo_libro, Libro.numero_paginas, Libro.formato, Autor.nombre_autor, Editorial.nombre_editorial, Libro.fecha_publicacion, Libro.volumen, Libro.id_libro)   
    return render_template("listaLibro.html", consulta = consulta_libro)



#################### funciones de autor #############
@app.route("/leerautores")
def leerautores():
    autor = Autor.query.all()
    return render_template("leerAutores.html", autores = autor)

@app.route("/modificar_autor", methods=['POST'])
def modificar_autor():
    idautor = request.form['idautor']
    nombre_autor = request.form['nombre_autor']
    fecha_nac = request.form['fecha_nac']
    nacionalidad = request.form['nacionalidad']

    autor = Autor.query.filter_by(id_autor=int(idautor)).first()
    autor.nombre_autor = nombre_autor
    autor.fecha_nac = fecha_nac
    autor.nacionalidad = nacionalidad
    db.session.commit()
    return redirect("/leerautores")

@app.route("/editarautor/<ID>")
def editarautor(ID):
    autor = Autor.query.filter_by(id_autor = int(ID)).first()
    return render_template("modificarautor.html", autor = autor)

@app.route("/eliminarautor/<ID>")
def eliminarautor(ID):
    autor = Autor.query.filter_by(id_autor = int(ID)).delete()
    db.session.commit()
    return redirect("/leerautores")



###############funciones de genero#############
@app.route("/leergenero")
def leergenero():
    genero = Genero.query.all()
    return render_template("leerGenero.html", generos = genero)

@app.route("/modificar_genero", methods=['POST'])
def modificar_genero():
    idgenero = request.form['idgenero']
    nombre_genero = request.form["nombre_genero"]

    genero = Genero.query.filter_by(id_genero=int(idgenero)).first()
    genero.nombre_genero = nombre_genero
    db.session.commit()
    return redirect("/leergenero")

@app.route("/editargenero/<ID>")
def editargenero(ID):
    genero = Genero.query.filter_by(id_genero = int(ID)).first()
    return render_template("modificargenero.html", genero = genero)

@app.route("/eliminargenero/<ID>")
def eliminargenero(ID):
    genero = Genero.query.filter_by(id_genero = int(ID)).delete()
    db.session.commit()
    return redirect("/leergenero")




#############funciones de editorial#######################
@app.route("/leereditorial")
def leereditorial():
    editorial = Editorial.query.all()
    return render_template("leerEditorial.html", editoriales = editorial)

@app.route("/modificar_editorial", methods=['POST'])
def modificar_editorial():
    ideditorial = request.form['ideditorial']
    nombre_editorial = request.form["nombre_editorial"]

    editorial = Editorial.query.filter_by(id_editorial=int(ideditorial)).first()
    editorial.nombre_editorial = nombre_editorial
    db.session.commit()
    return redirect("/leereditorial")

@app.route("/editareditorial/<ID>")
def editareditorial(ID):
    editorial = Editorial.query.filter_by(id_editorial = int(ID)).first()
    return render_template("modificareditorial.html", editorial = editorial)

@app.route("/eliminareditorial/<ID>")
def eliminareditorial(ID):
    editorial = Editorial.query.filter_by(id_editorial = int(ID)).delete()
    db.session.commit()
    return redirect("/leereditorial")




@app.route("/iniciar_sesion")
def iniciar_sesion():
    redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)