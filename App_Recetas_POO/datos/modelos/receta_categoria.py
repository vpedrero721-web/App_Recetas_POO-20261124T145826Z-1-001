from peewee import CompositeKey, ForeignKeyField

from datos.model_base import ModelBase
from datos.modelos.categoria import Categoria
from datos.modelos.receta import Receta


class RecetaCategoria(ModelBase):
    receta = ForeignKeyField(
        Receta,
        column_name="id_receta",
        backref="relaciones_categorias",
        on_delete="CASCADE",
    )
    categoria = ForeignKeyField(
        Categoria,
        column_name="id_categoria",
        backref="relaciones_recetas",
        on_delete="CASCADE",
    )

    class Meta:
        table_name = "RecetasCategorias"
        primary_key = CompositeKey("receta", "categoria")
