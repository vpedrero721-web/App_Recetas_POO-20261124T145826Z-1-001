from peewee import AutoField, DateField, ForeignKeyField, SmallIntegerField, TextField

from datos.model_base import ModelBase
from datos.modelos.receta import Receta
from datos.modelos.usuario import Usuario


class Valoracion(ModelBase):
    id_valoracion = AutoField()
    puntuacion = SmallIntegerField()
    comentario = TextField(null=True)
    fecha = DateField()
    usuario = ForeignKeyField(
        Usuario,
        column_name="id_usuario",
        backref="valoraciones",
        on_delete="CASCADE",
    )
    receta = ForeignKeyField(
        Receta,
        column_name="id_receta",
        backref="valoraciones",
        on_delete="CASCADE",
    )

    class Meta:
        table_name = "Valoraciones"
        indexes = ((("usuario", "receta"), True),)
