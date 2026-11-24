from peewee import CompositeKey, DateField, ForeignKeyField

from datos.model_base import ModelBase
from datos.modelos.receta import Receta
from datos.modelos.usuario import Usuario


class RecetaGuardada(ModelBase):
    usuario = ForeignKeyField(
        Usuario,
        column_name="id_usuario",
        backref="recetas_guardadas",
        on_delete="CASCADE",
    )
    receta = ForeignKeyField(
        Receta,
        column_name="id_receta",
        backref="guardada_por",
        on_delete="CASCADE",
    )
    fecha_guardado = DateField()

    class Meta:
        table_name = "RecetasGuardadas"
        primary_key = CompositeKey("usuario", "receta")
