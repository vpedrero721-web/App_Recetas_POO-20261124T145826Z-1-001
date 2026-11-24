from peewee import AutoField, CharField

from datos.model_base import ModelBase


class Categoria(ModelBase):
    id_categoria = AutoField()
    nombre = CharField(max_length=100, unique=True)
    descripcion = CharField(max_length=255)

    class Meta:
        table_name = "Categorias"

    def __str__(self) -> str:
        return f"[{self.id_categoria}] {self.nombre}"
