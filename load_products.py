import os
import sys
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crissstore.settings')
django.setup()

from tienda.models import Producto

productos = [
    {
        'nombre': 'Logitech G733',
        'descripcion': 'Audífonos con micrófono inalámbricos LIGHTSPEED RGB para juegos.',
        'precio': 150000,
        'imagen': 'Logitech G733.jpg'
    },
    {
        'nombre': 'Logitech Lightspeed G305',
        'descripcion': 'Mouse inalámbrico para juegos LIGHTSPEED',
        'precio': 80000,
        'imagen': 'Logitech Lightspeed G305.jpg'
    },
        {
        'nombre': 'Teclado Logitech G Pro RGB',
        'descripcion': 'Teclado Ergonomico con RGB',
        'precio': 110000,
        'imagen': 'Teclado Logitech G Pro RGB.jpg'
    },
        {
        'nombre': 'Logitech G335',
        'descripcion': 'Audifonos con micrófono inalámbricos para juegos',
        'precio': 60000,
        'imagen': 'Logitech G335.jpg'
    },
        {
        'nombre': 'Logitech LightspeedG502',
        'descripcion': 'Mouse con cable para juegos competitivos.',
        'precio': 100000,
        'imagen': 'Logitech LightspeedG502.jpg'
    },
        {
        'nombre': 'Razer Ornata V3 X Teclado',
        'descripcion': 'Mouse con cable para juegos competitivos.',
        'precio': 45000,
        'imagen': 'Razer Ornata V3 X Teclado.jpg'
    },
]

for producto_data in productos:
    Producto.objects.create(**producto_data)

print("Productos añadidos exitosamente.")