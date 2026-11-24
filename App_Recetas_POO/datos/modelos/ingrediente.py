from peewee import AutoField, CharField

from datos.model_base import ModelBase


class Ingrediente(ModelBase):
    id_ingrediente = AutoField()
    nombre = CharField(max_length=100, unique=True)
    categoria_ingrediente = CharField(max_length=100)

    class Meta:
        table_name = "Ingredientes"

    def __str__(self) -> str:
        return f"[{self.id_ingrediente}] {self.nombre} ({self.categoria_ingrediente})"
