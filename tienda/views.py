from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido
from .forms import PedidoForm, ContactoForm, ProductoForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio') 
    return render(request, 'tienda/login.html')


def perfil(request):
    return render(request, 'tienda/perfil.html')

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio') 
    else:
        form = UserCreationForm()
    return render(request, 'tienda/registro.html', {'form': form})


def inicio(request):
    productos_destacados = Producto.objects.all()[:3]
    return render(request, 'tienda/inicio.html', {'productos_destacados': productos_destacados})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tienda/detalle_producto.html', {'producto': producto})

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Mensaje enviado con éxito.')
            return redirect('inicio')
    else:
        form = ContactoForm()
    return render(request, 'tienda/contacto.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('inicio')

@login_required
def carrito(request):
    carrito = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })
    return render(request, 'tienda/carrito.html', {'productos_carrito': productos_carrito, 'total': total})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    carrito[str(producto_id)] = carrito.get(str(producto_id), 0) + 1
    request.session['carrito'] = carrito
    messages.success(request, f'{producto.nombre} añadido al carrito.')
    return redirect('carrito')

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
    return redirect('carrito')

@login_required
def resumen_pedido(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('carrito')

    productos_carrito = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos_carrito.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        rut = request.POST.get('rut')
        direccion = request.POST.get('direccion')
        formaPago = request.POST.get('formaPago')

        pedido = Pedido.objects.create(
            usuario=request.user,
            nombre=nombre,
            apellido=apellido,
            rut=rut,
            direccion=direccion,
            total=total,
            forma_pago=formaPago
        )

        for item in productos_carrito:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=item['producto'],
                cantidad=item['cantidad'],
                precio_unitario=item['producto'].precio
            )

        del request.session['carrito']

        messages.success(request, 'Pedido realizado con éxito.')
        return redirect('confirmacion_pedido', pedido_id=pedido.id)

    return render(request, 'tienda/resumen_pedido.html', {'productos_carrito': productos_carrito, 'total': total})

    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            
            total = 0
            for producto_id, cantidad in carrito.items():
                producto = get_object_or_404(Producto, id=producto_id)
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )
                total += producto.precio * cantidad
            
            pedido.total = total
            pedido.save()
            
            del request.session['carrito']
            
            messages.success(request, 'Pedido realizado con éxito.')
            return redirect('confirmacion_pedido', pedido_id=pedido.id)
    else:
        form = PedidoForm()
    
    return render(request, 'tienda/resumen_pedido.html', {'form': form})

@login_required
def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'tienda/confirmacion_pedido.html', {'pedido': pedido})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/agregar_producto.html', {'form': form})