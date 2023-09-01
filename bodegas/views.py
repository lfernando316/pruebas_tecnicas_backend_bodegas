from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import Bodega, Producto
from .serializers import BodegaSerializer
import pdb


def listar_bodegas_ordenadas(request):
    bodegas = Bodega.objects.all().order_by('nombre')
    bodegas_data = [{'nombre': bodega.nombre,
                     'responsable': bodega.responsable.nombre} for bodega in bodegas]
    return JsonResponse({'bodegas': bodegas_data})


@api_view(['POST'])  # Especifica los métodos HTTP permitidos
def crear_bodega(request):
    if request.method == 'POST':
        # Usa el serializador para deserializar los datos de entrada
        serializer = BodegaSerializer(data=request.data)

        if serializer.is_valid():  # Valida los datos de entrada con el serializador
            serializer.save()  # Guarda la bodega en la base de datos
            # Devuelve la bodega creada en formato JSON
            return Response(serializer.data, status=201)

        # Devuelve errores de validación si los datos no son válidos
        return Response(serializer.errors, status=400)

    return Response({'error': 'Se esperaba una solicitud POST'}, status=400)

    # datos y ruta para ingresar una bodega
    # http://localhost:8000/crear_bodega/
    #     {
    #     "nombre": "Nombre de la Bodega2",
    #     "responsable": 1,
    #     "estado": true
    # }


def listar_productos_total_descendente(request):
    # obtener la lista de productos con la cantidad total
    productos = Producto.objects.annotate(
        total=Sum('inventario__cantidad')).order_by('-total')

    # Serializar los resultados en formato JSON
    productos_json = [{'nombre': producto.nombre,
                       'total': producto.total} for producto in productos]

    return JsonResponse({'productos': productos_json})
