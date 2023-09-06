from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Sum
from .models import Bodega, Producto, Inventario, Historial
from .serializers import BodegaSerializer, ProductoSerializer, InventarioSerializer, HistorialSerializer
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


@api_view(['POST'])  # Especifica los métodos HTTP permitidos
def agregar_producto(request):
    if request.method == 'POST':
        try:
            # Obtiene los datos de la solicitud
            data = request.data

            # Serializa los datos de la solicitud utilizando el serializador ProductoSerializer
            serializer = ProductoSerializer(data=data)

            # Verifica si los datos son válidos
            if serializer.is_valid():
                # Guarda el producto en la base de datos
                producto = serializer.save()

                # Crea el registro con el inventario inicial
                Inventario.objects.create(
                    producto=producto, cantidad=1, bodega_id=1)

                # Devuelve una respuesta de éxito
                return Response({"mensaje": "Producto agregado correctamente"}, status=status.HTTP_201_CREATED)
            else:
                # Devuelve errores de validación si los datos no son válidos
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Maneja excepciones generales y devuelve una respuesta de error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Devuelve una respuesta de error si no se recibe una solicitud POST
        return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)

        # datos y ruta para ingresar un producto
    # http://localhost:8000/agregar_producto/
    # {
    #     "nombre": "Producto 4",
    #     "descripcion": "Descripción del producto 4",
    #     "estado": true
    # }

# punto 9


@api_view(['POST'])
def insertar_actualizar_inventario(request):
    try:
        # Obtener los parámetros de entrada
        producto_id = request.data.get('producto_id')
        bodega_id = request.data.get('bodega_id')
        cantidad = request.data.get('cantidad')

        # Verificar si ya existe una combinación producto/bodega en el inventario
        inventario_existente = Inventario.objects.filter(
            producto_id=producto_id, bodega_id=bodega_id).first()

        if inventario_existente:
            # Si existe, actualizar el registro existente sumando la cantidad nueva
            inventario_existente.cantidad += cantidad
            inventario_existente.save()
        else:
            # Si no existe, crear un nuevo registro en el inventario
            Inventario.objects.create(
                producto_id=producto_id, bodega_id=bodega_id, cantidad=cantidad)

        return Response({"mensaje": "Operación exitosa"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # datos y ruta para insertar en la tabla inventarios
    # http://localhost:8000/insertar_actualizar_inventario/
    # {
    #     "producto_id": 2,
    #     "bodega_id": 4,
    #     "cantidad": 10
    # }


@api_view(['POST'])
def trasladar_producto(request):
    try:
        # Obtén los datos de la solicitud POST
        data = request.data
        producto_id = data.get('producto_id')
        bodega_origen_id = data.get('bodega_origen_id')
        bodega_destino_id = data.get('bodega_destino_id')
        cantidad = data.get('cantidad')

        # Valida que la cantidad a trasladar no sea mayor que la cantidad en la bodega de origen
        inventario_origen = Inventario.objects.get(
            producto_id=producto_id, bodega_id=bodega_origen_id)
        if cantidad > inventario_origen.cantidad:
            return Response({"error": "La cantidad a trasladar es mayor que la cantidad en la bodega de origen"}, status=status.HTTP_400_BAD_REQUEST)

        # Resta la cantidad de la bodega de origen
        inventario_origen.cantidad -= cantidad
        inventario_origen.save()

        # Suma la cantidad a la bodega de destino o crea un nuevo registro si no existe
        inventario_destino, _ = Inventario.objects.get_or_create(
            producto_id=producto_id, bodega_id=bodega_destino_id)
        inventario_destino.cantidad += cantidad
        inventario_destino.save()

        # Registra el historial del traslado
        historial = Historial.objects.create(
            cantidad=cantidad,
            bodega_origen_id=bodega_origen_id,
            bodega_destino_id=bodega_destino_id,
            inventario=inventario_origen
        )

        # Serializa y devuelve el historial
        serializer = HistorialSerializer(historial)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Inventario.DoesNotExist:
        return Response({"error": "El producto o bodega especificados no existen"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # datos y ruta para insertar en la tabla inventarios
    # http://localhost:8000/trasladar_producto/
    # {
    #     "producto_id": 1,
    #     "bodega_origen_id": 2,
    #     "bodega_destino_id": 3,
    #     "cantidad": 5
    # }
