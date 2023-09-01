from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    foto = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bodega(models.Model):
    nombre = models.CharField(max_length=30)
    responsable = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Inventario(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Historial(models.Model):
    cantidad = models.CharField(max_length=100)
    bodega_origen = models.ForeignKey(
        Bodega, on_delete=models.CASCADE, related_name='historiales_origen')
    bodega_destino = models.ForeignKey(
        Bodega, on_delete=models.CASCADE, related_name='historiales_destino')
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
