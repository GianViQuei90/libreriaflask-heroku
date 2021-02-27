from sqlalchemy.orm import backref
from config.base_datos import bd
#from sqlalchemy import types

class AutorModel(bd.Model):
     #para cambiar el nonmbre de la tabla a crearse
    __tablename__= "t_autor"
    autorId =  bd.Column(
                        name="autor_id", 
                        type_= bd.Integer,
                        primary_key=True, 
                        autoincrement=True, 
                        nullable= False, 
                        unique=True)

    autorNombre = bd.Column(
                        name="autor_nombre", 
                        type_= bd.String(45),)
    
    libros = bd.relationship('LibroModel', backref='autorLibro') 
    # en el caso de fk se apunta al nombre de la tabla, mientras que en los relationship
    

    def __init__(self, nombreAutor):
        self.autorNombre = nombreAutor

    def __str__(self):
        return '{}: {}'.format(self.autorId, self.autorNombre)

    def save(self):
        #el metodo add sirve para agregar toda mi instancia a un formato que sea valido para bd
        bd.session.add(self)
        bd.session.commit()

    def json(self):
        return{
            'autor_id': self.autorId,
            'autor_nombre': self.autorNombre
        }

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()