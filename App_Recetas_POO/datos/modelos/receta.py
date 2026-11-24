from peewee import AutoField, CharField, ForeignKeyField, IntegerField, TextField

from datos.model_base import ModelBase
from datos.modelos.usuario import Usuario


class Receta(ModelBase):
    id_receta = AutoField()
    nombre = CharField(max_length=100)
    descripcion = TextField()
    tiempo_preparacion = IntegerField()
    dificultad = CharField(max_length=20)
    instrucciones = TextField()
    porciones = IntegerField(default=4)
    imagen_url = CharField(max_length=255, null=True)
    usuario = ForeignKeyField(
        Usuario,
        column_name="id_usuario",
        backref="recetas",
        on_delete="RESTRICT",
    )

    class Meta:
        table_name = "Recetas"

    def __str__(self) -> str:
        return f"[{self.id_receta}] {self.nombre} ({self.dificultad}, {self.tiempo_preparacion} min)"
