from peewee import CharField, CompositeKey, DecimalField, ForeignKeyField

from datos.model_base import ModelBase
from datos.modelos.ingrediente import Ingrediente
from datos.modelos.receta import Receta


class DetalleIngrediente(ModelBase):
    receta = ForeignKeyField(
        Receta,
        column_name="id_receta",
        backref="detalles_ingredientes",
        on_delete="CASCADE",
    )
    ingrediente = ForeignKeyField(
        Ingrediente,
        column_name="id_ingrediente",
        backref="detalles_recetas",
        on_delete="RESTRICT",
    )
    cantidad = DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = CharField(max_length=50)

    class Meta:
        table_name = "DetalleIngrediente"
        primary_key = CompositeKey("receta", "ingrediente")
