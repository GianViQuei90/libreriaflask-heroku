from flask import Flask, request
from flask_restful import Api
from config.base_datos import bd
#from models.autor import AutorModel
from controllers.autor import AutoresController, AutorController
from controllers.categoria import CategoriaController
from controllers.libro import LibrosController, LibroModel, RegistroLibroSedeController
from controllers.sede import LibroCategoriaController, SedesController, LibrosSedeController
#from models.sede import SedeModel
#from models.categoria import CategoriaModel
#from models.libro import LibroModel
#from models.sedeLibro import SedeLibroModel
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
SWAGGER_URL = ''
API_URL = '/static/swagger.json'
swagger_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':"Libreria Flask - Swagger Documentation"
    }
)
#mysql://root:root@localhost:3306/flasklibreria
app = Flask(__name__)
app.register_blueprint(swagger_blueprint)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://numjmbfsfzvdbzfp:f4xhk9fzmaayj85s@d6rii63wp64rsfb5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/t7pdjw13yz44k2hq'
api = Api(app)
CORS(app)  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bd.init_app(app)
#bd.drop_all(app=app)
bd.create_all(app=app)

@app.route('/buscar')
def buscarLibro():
    print(request.args.get('palabra'))
    
    palabra = request.args.get('palabra')
    if palabra:
        resultadoBusqueda = LibroModel.query.filter(LibroModel.libroNombre.like('%'+palabra+'%')).all()
        if resultadoBusqueda:
            resultado = []
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
            return{
                'success':True,
                'content':resultado,
                'message':None
            }
    return{
        'success':True,
        'content':None,
        'message':'No se encontro resultados'
    }, 400

#rutas de mi api restful
api.add_resource(AutoresController, '/autores')
api.add_resource(AutorController, '/autor/<int:id>')
api.add_resource(CategoriaController, '/categorias', '/categoria')
api.add_resource(LibrosController, '/libros', '/libro')
api.add_resource(SedesController, '/sedes', '/sede')
api.add_resource(LibrosSedeController, '/sedeLibros/<int:id_sede>')
api.add_resource(LibroCategoriaController, '/busquedaLibroSedeCat')
api.add_resource(RegistroLibroSedeController, '/registrarSedesLibro')

if __name__ == '__main__':
    app.run(debug=True)