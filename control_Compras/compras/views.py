from django.shortcuts import render, redirect
from compras.models import Categoria, CategoriaUsuario, CompraCabecera, CompraDetalle, TipoProducto, UsuarioEncargado
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date


def crearCabecera(request):
        usuario = UsuarioEncargado.objects.filter(usuario=request.user)
        if len(usuario) > 0:
            categoria = Categoria.objects.filter(id=request.POST.get('icategoria'))
            observaciones = request.POST.get('iobservaciones')
            usuario_asignado = User.objects.filter(id=request.POST.get('iaprobador'))
            compracabera = CompraCabecera()
            compracabera.asignado_a = usuario_asignado[0]
            compracabera.categoria_id = categoria[0]
            compracabera.usuario_registro = request.user
            compracabera.observaciones = observaciones
            compracabera.save()
            return compracabera
        messages.info(request, 'No tiene a ningun encargado asociado para crear pedidos')
        return None

def __buscar_encargado(request):
    usuarios = UsuarioEncargado.objects.filter(encargado=request.user).values('usuario')
    print(f'usuarios: {usuarios} - {request.user}')
    if len(usuarios) > 0:
        print('entro aqui a encargados')
        return CompraCabecera.objects.filter(Q(usuario_registro__in = usuarios) | Q(usuario_registro = request.user)).order_by('estado','-id')
    return CompraCabecera.objects.filter(usuario_registro=request.user)


def __buscadores(request):
    categorias_usuarios = CategoriaUsuario.objects.filter(usuario = request.user).values('categoria')
    print(f'categorias_usuarios: {categorias_usuarios} - {request.user}')
    if len(categorias_usuarios) > 0:
        print('entro aqui a autorizaciones')
        return CompraCabecera.objects.filter(Q(categoria_id__in=categorias_usuarios, estado='2')| Q(usuario_registro=request.user)).order_by('-id')
    elif len(User.objects.filter(user_permissions__codename='puede_entregar_compra', id = request.user.id ))>0:
        print('entro aqui a entregas')
        return CompraCabecera.objects.filter(Q(usuario_entrega=request.user, estado='3')| Q(usuario_registro=request.user)).order_by('-id') 
    else:
        return __buscar_encargado(request)

# Create your views here.
@login_required
def compras(request):
    categorias = Categoria.objects.all()
    aprobadores = User.objects.filter(Q(user_permissions__codename='puede_entregar_compra'))
    pedidos = __buscadores(request)
    if request.method == 'POST':
        if request.POST.get('bcabecera'):
            cabecera = crearCabecera(request)
            if cabecera != None:
                return redirect('comprasDetalle', id=cabecera.id)
    return render(request, 'compras.html', {'categorias': categorias, 'aprobadores': aprobadores, 'pedidos': pedidos})


def crear_detalle(request, pedido):
    if pedido[0].estado == '0':
        tipo_producto = TipoProducto.objects.filter(id=request.POST.get('itipoproducto'))
        cantidad = int(request.POST.get('icantidad'))
        producto = request.POST.get('iproducto')
        precio = int(request.POST.get('iprecio'))
        detalle = CompraDetalle()
        detalle.producto = producto
        detalle.compra_cabecera = pedido[0]
        detalle.tipo_producto = tipo_producto[0]
        detalle.cantidad = cantidad
        detalle.precio = precio
        detalle.subtotal = cantidad * precio
        detalle.save()
    else:
        messages.warning(request, 'No se puede agregar un detalle a un pedido que ya fue finalizado')

def eliminar_detalle(request, id, pedido):
    if pedido[0].estado == '0':
        detalle = CompraDetalle.objects.filter(id=id)
        detalle.delete()
    else:
        messages.warning(request, 'No se puede eliminar un detalle de un pedido que ya fue finalizado')

def __finalizar_pedido(request, id):
    pedido = CompraCabecera.objects.get(id=id)
    if request.user.id == pedido.usuario_registro.id:
        if pedido.estado == '0':
            pedido.estado = '1'
            pedido.save()
            messages.success(request, 'Pedido finalizado con exito')
        else:
            messages.warning(request, 'No se puede finalizar un pedido que ya fue finalizado')
    else:
        messages.warning(request, 'No se puede finalizar un pedido que no fue creado por usted')

def __totalizar_cabercera(total, id):
    pedido = CompraCabecera.objects.get(id=id)
    pedido.total = total
    pedido.save()

def __rechazar_pedido_encargado(request, id):
    usuario_encagado = UsuarioEncargado.objects.filter(encargado=request.user)
    if len(usuario_encagado) > 0:
        pedido = CompraCabecera.objects.get(id=id)
        pedido.usuario_rechaza = request.user
        pedido.estado = '9'
        pedido.save()
        messages.success(request, 'Pedido rechazado con exito')
    else:
        messages.warning(request, 'no puedes rechazar un pedido ya que no eres el encargado de el.')

def __aprobar_pedido_encargado(request, id):
    usuario_encagado = UsuarioEncargado.objects.filter(encargado=request.user)
    if len(usuario_encagado) > 0:
        pedido = CompraCabecera.objects.get(id=id)
        pedido.usuario_aprobado = request.user
        pedido.fecha_aprobado = date.today()
        pedido.estado = '2'
        pedido.save()
        messages.success(request, 'Pedido aprobado con exito')
    else:
        messages.warning(request, 'no puedes aprobar un pedido ya que no eres el encargado de el.')

def __autorizar_pedido(request, id):
    pedido = CompraCabecera.objects.get(id=id)
    usuario_categoria = CategoriaUsuario.objects.filter(usuario=request.user, categoria = pedido.categoria_id)
    if len(usuario_categoria) > 0: 
        pedido.usuario_autorizado = request.user
        pedido.fecha_autorizado = date.today()
        pedido.estado = '3'
        pedido.save()
        messages.success(request, 'Pedido autorizado con exito')
    else:
        messages.warning(request, 'no puedes autorizar un pedido ya que no tienes permisos sobre la categoria.')

def __rechazar_autorizacion_pedido(request, id):
    pedido = CompraCabecera.objects.get(id=id)
    usuario_categoria = CategoriaUsuario.objects.filter(usuario=request.user, categoria = pedido.categoria_id)
    if len(usuario_categoria) > 0: 
        pedido.usuario_rechaza = request.user
        pedido.estado = '9'
        pedido.save()
        messages.success(request, 'Pedido rechazado con exito')
    else:
        messages.warning(request, 'no puedes rechazar un pedido ya que no tienes permisos sobre la categoria.')

def __entregar_pedido(request, id , entregado):
    pedido = CompraCabecera.objects.get(id=id)
    if request.user.id == pedido.asignado_a.id:
        pedido.fecha_entrega = date.today()
        pedido.estado = '4'
        pedido.valor_entregado = entregado
        pedido.save()
        messages.success(request, 'Pedido entregado con exito')
    else:
        messages.warning(request, 'no puedes entregar un pedido ya que no eres el responsable de el.')

@login_required
def comprasDetalle(request, id):
    print(f'llego hasta aqui? {id}')
    pedido = CompraCabecera.objects.filter(id=id)
    tipo_productos = TipoProducto.objects.all()
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('bdetalle'):
            crear_detalle(request, pedido)
        if request.POST.get('bdelete'):
            eliminar_detalle(request, request.POST.get('bdelete'), pedido)
        if request.POST.get('bfinalizar'):
            __finalizar_pedido(request, id)
            return redirect('compras') 
        if request.POST.get('brechazarencargado'):
            __rechazar_pedido_encargado(request, id)
            return redirect('compras')
        if request.POST.get('baprobarencargado'):
            __aprobar_pedido_encargado(request, id)
            return redirect('compras')
        if request.POST.get('bautorizar'):
            __autorizar_pedido(request, id)
            return redirect('compras')
        if request.POST.get('brechazarautorizacion'):
            __rechazar_autorizacion_pedido(request, id)
            return redirect('compras') 
        if request.POST.get('bentrega'):
            entregado = int(request.POST.get('ientrega'))
            __entregar_pedido(request, id, entregado)
            return redirect('compras')
    detalle = CompraDetalle.objects.filter(compra_cabecera=id)
    total = 0 if len(detalle)== 0 else sum(i.subtotal for i in detalle)
    __totalizar_cabercera(total, id)
    return render(request, 'comprasDetalle.html', {'pedido': pedido, 'detalle': detalle, 'tipo_productos': tipo_productos, 'total': total})


