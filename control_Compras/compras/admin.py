from django.contrib import admin
from .models import Categoria, CategoriaUsuario, CompraCabecera, CompraDetalle, TipoProducto, UsuarioEncargado

admin.site.register(Categoria)
admin.site.register(CategoriaUsuario)
admin.site.register(CompraCabecera)
admin.site.register(CompraDetalle)
admin.site.register(TipoProducto)
admin.site.register(UsuarioEncargado)

# Register your models here.
