from django.db import models
from django.contrib.auth.models import User
from datetime import date


ESTADOS_COMPRA = (
    ('0', 'Pendiente'),
    ('1', 'Registrado'),
    ('2', 'Aprobado Encargado'),
    ('3', 'Autorizado Gerencia'),
    ('4', 'Entregado'),
    ('5', 'Cerrado'),
    ('9', 'Rechazado')
)

def get_today():
    return date.today()

class TipoProducto(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

class Categoria(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
    
class  UsuarioEncargado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usuario")
    encargado = models.ForeignKey(User, on_delete=models.PROTECT, related_name="encargado")

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name} - {self.encargado.first_name} {self.encargado.last_name}'

class CategoriaUsuario(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.categoria} - ({self.usuario}) {self.usuario.first_name} {self.usuario.last_name}'
    class Meta:
        permissions = [('puede_ver_categoria', 'puede_ver_categoria')]


class CompraCabecera(models.Model):
    asignado_a = models.ForeignKey(User, on_delete=models.PROTECT, related_name='asignado_a')
    fecha_registro = models.DateField(null=True, blank=True, default=get_today)
    fecha_aprobado = models.DateField(null=True, blank=True,)
    fecha_autorizado = models.DateField(null=True, blank=True,)
    fecha_entrega = models.DateField(null=True, blank=True,)
    fecha_cerrado = models.DateField(null=True, blank=True,)
    categoria_id = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='categoria_id')
    usuario_registro = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usuario_registro')
    usuario_aprobado = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='usuario_aprobado')
    usuario_autorizado = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='usuario_autorizado')
    usuario_entrega = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='usuario_entrega')
    usuario_rechaza = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name='usuario_rechaza')
    observaciones = models.CharField(max_length=250, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_COMPRA, default='0')
    total = models.IntegerField(default=0)
    valor_entregado = models.IntegerField(default=0)
    valor_real = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id} - {self.asignado_a} - {self.fecha_registro} - {self.categoria_id} - {self.usuario_registro} - {self.estado}'


    class Meta:
        permissions = [('puede_aprobar_compra', 'puede_aprobar_compra'),
                       ('puede_entregar_compra', 'puede_entregar_compra'),
                       ('puede_cerrar_compra', 'puede_cerrar_compra'),
                       ('puede_ver_todas_las_compras', 'puede_ver_todas_las_compras'),
                       ('puede_ser_aprobador', 'puede_ser_aprobador'),
                       ('puede_ser_entregador', 'puede_ser_entregador'),]


class CompraDetalle(models.Model):
    compra_cabecera = models.ForeignKey(CompraCabecera, on_delete=models.PROTECT)
    producto = models.CharField(max_length=250, null=True, blank=True )
    tipo_producto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, null=True, blank=True)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
# Create your models here.
    def __str__(self) -> str:
        return f'{self.producto} - {self.tipo_producto} - {self.cantidad} - {self.precio} - {self.subtotal}'