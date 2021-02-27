from models.sede import SedeModel
from flask_restful import Resource, reqparse
#basico
#get all sede
#create sede
#vincula una sede con varios libros y viceversa(un libro cn varias sedes)
serializer = reqparse.RequestParser(bundle_errors=True)
serializer.add_argument(
    'sede_latitud',
    type=float,
    required=True,
    help='Falta la sede_latitud',
    dest='latitud'
)
serializer.add_argument(
    'sede_ubicacion',
    type=str,
    required=True,
    help='Falta la sede_ubicacion',
    dest='ubicacion'
)
serializer.add_argument(
    'sede_longitud',
    type=float,
    required=True,
    help='Falta la sede_longitud',
    dest='longitud'
)
class SedesController(Resource):
    def post(self):
        data = serializer.parse_args()
        print(data)
        #los tipos de datos que no son ni numericos ni strings=decimal, fecha, no puuede hacer la conversion automt
        nuevaSede = SedeModel(data['ubicacion'], data['latitud'], data['longitud'])
        nuevaSede.save()
        return{
            'success':True,
            'content': nuevaSede.json(),
            'message': 'Sede guardada con exito'
        }
    def get(self):
        sedes = SedeModel.query.all()
        #print(libros[0].autorLibro.json())
        resultado=[]
        for sede in sedes:
            resultado.append(sede.json())
        return{
            'success': True,
            'content': resultado,
            'message': None
        }

#busqueda de todos los libros de una sede
class LibrosSedeController(Resource):
    def get(self, id_sede):
        sede = SedeModel.query.filter_by(sedeId=id_sede).first()
        sedeLibros = sede.libros
        libros=[]
        #si el autor se encontro en el content su contenido pero si no se hallo dicho autor indicar que el id no existe
        for sedeLibro in sedeLibros:
            libro = sedeLibro.libroSede.json()
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
            libro['categoria'] = sedeLibro.libroSede.categoriaLibro.json()
            del libro['categoria']['categoria_id']
            del libro['autor_id']
            libros.append(libro)
            #print(sedeLibro.libroSede)
        resultado = sede.json()
        resultado['libros'] = libros
        return{
            'success':True,
            'content': resultado
        }
    
#busqueda de todos los libros de una sede segun su categoria
#categoria
#sede
#127.0.0.1:5000/buscarLibroCategoria?sede=1&categoria=2
class LibroCategoriaController(Resource):
    def get(self):
        serializer.remove_argument('sede_latitud')
        serializer.remove_argument('sede_ubicacion')
        serializer.remove_argument('sede_longitud')
        serializer.add_argument(
            'categoria',
            type=int,
            required=True,
            help='Falta la categoria',
            location='args'
        )
        serializer.add_argument(
            'sede',
            type=int,
            required=True,
            help='Falta la sede',
            location='args'
        )
        data = serializer.parse_args()
        sede = SedeModel.query.filter_by(sedeId = data['sede']).first()
        #print(sede.libros)
        libros=[]
        for sedelibro in sede.libros:
            print(sedelibro.libroSede)
            if (sedelibro.libroSede.categoria == data['categoria']):
                libros.append(sedelibro.libroSede.json())
        return{
            'success': True,
            'content': libros
        }
    