from peewee import AutoField, BooleanField, CharField

from datos.model_base import ModelBase


class Usuario(ModelBase):
    id_usuario = AutoField()
    nombre = CharField(max_length=100)
    email = CharField(max_length=100, unique=True)
    password_hash = CharField(max_length=255)
    activo = BooleanField(default=True)

    class Meta:
        table_name = "Usuarios"

    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"
        return f"[{self.id_usuario}] {self.nombre} ({self.email}) - {estado}"
