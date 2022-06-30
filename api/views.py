from unicodedata import decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.http import JsonResponse
from datetime import datetime
# crud de tipo_producto


class TipoProductoApi(APIView):
    def get(self, request):
        tipo_producto = TipoProducto.objects.all().values()
        return Response(tipo_producto)

    def post(self, request):
        # validar que exista nombre y descripcion en el body
        if 'nombre' in request.data and 'descripcion' in request.data:
            nombre = request.data['nombre']
            descripcion = request.data['descripcion']
            tipo_producto = TipoProducto(
                nombre=nombre, descripcion=descripcion)
            tipo_producto.save()
            return Response({"message": "Tipo de producto creado"})
        else:
            return Response({"message": "Faltan datos"}, status=400)

    def put(self, request):
        # actualizar tipo de producto
        if 'id' in request.data and 'nombre' in request.data and 'descripcion' in request.data:
            id = request.data['id']
            nombre = request.data['nombre']
            descripcion = request.data['descripcion']
            tipo_producto = TipoProducto.objects.get(id=id)
            tipo_producto.nombre = nombre
            tipo_producto.descripcion = descripcion
            tipo_producto.save()
            return Response({"message": "Tipo de producto actualizado"})
        else:
            return Response({"message": "Faltan datos"}, status=400)


class ProductoApi(APIView):
    def get(self, request):
        print(request.query_params)
        if('id' in request.query_params):
            id = request.query_params['id']
            producto = Producto.objects.get(id=id)
            print(producto)
            print("entro aqui")
            #convertir producto a diccionario
            producto_dict = {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'tipo': producto.tipo.id,
                'stock': producto.stock,
                'precioOferta': producto.precioOferta,
            }
            return JsonResponse(producto_dict)
        if ('inOferta' in request.query_params):
            #Obtneer productos cuando precioOferta no sea 0
            producto = Producto.objects.filter(precioOferta__gt=0)
            return Response(producto.values())
            
        if('tipo' in request.query_params):
            tipo = request.query_params['tipo']
            tipo = TipoProducto.objects.get(id=tipo)
            producto = Producto.objects.filter(tipo=tipo)
            return Response(producto.values())
        
        producto = Producto.objects.all().values()
        return Response(producto)

    def post(self, request):
        # validar que exista nombre y descripcion en el body
        if 'nombre' in request.data and 'descripcion' in request.data and 'precio' in request.data and 'stock' in request.data and 'tipo' in request.data:
            nombre = request.data['nombre']
            descripcion = request.data['descripcion']
            precio = request.data['precio']
            stock = request.data['stock']
            tipo = TipoProducto.objects.get(id=request.data['tipo'])
            imagen = request.data['imagen']
            if 'oferta' in request.data:
                oferta = request.data['oferta']
            else:
                oferta = 0
            producto = Producto(imagen=imagen, nombre=nombre,
                                descripcion=descripcion, precio=precio, stock=stock, tipo=tipo, precioOferta=oferta)
            producto.save()
            return Response({"message": "Producto creado"})
        else:
            return Response({"message": "Faltan datos"}, status=400)

    def put(self, request):
        # actualizar producto
        if 'id' in request.data and 'nombre' in request.data and 'descripcion' in request.data and 'precio' in request.data and 'stock' in request.data and 'tipo' in request.data:
            id = request.data['id']
            nombre = request.data['nombre']
            descripcion = request.data['descripcion']
            precio = request.data['precio']
            stock = request.data['stock']
            tipo = request.data['tipo']
            oferta = request.data['oferta']
            print("========================")
            print(request.data)
            print("========================")

            if('imagen' in request.data):
                print("imagen en el body")
                imagen = request.data['imagen']
            else:
                print("imagen no  en el body")
                imagen = None
            producto = Producto.objects.get(id=id)
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.precio = precio
            producto.stock = stock
            producto.precioOferta = oferta
            tipo = TipoProducto.objects.get(id=tipo)
            producto.tipo = tipo
            if(imagen != None):
                producto.imagen = imagen
            producto.save()
            return Response({"message": "Producto actualizado"})
        else:
            return Response({"message": "Faltan datos"}, status=400)

# crud oferta



class TipoUsuarioApi(APIView):
    def get(self, request):
        tipo_usuario = TipoUsuario.objects.all().values()
        return Response(tipo_usuario)

    def post(self, request):
        # validar que exista nombre en el body
        if 'nombre' in request.data:
            nombre = request.data['nombre']
            tipo_usuario = TipoUsuario(nombre=nombre)
            tipo_usuario.save()
            return Response({"message": "Tipo usuario creado"})
        else:
            return Response({"message": "Faltan datos"}, status=400)

# crud usuario


class UsuarioApi(APIView):
    def get(self, request):
        usuario = Usuario.objects.all().values()
        if('id' in request.query_params):
            id = request.query_params['id']
            usuario = Usuario.objects.get(id=id)
            usuario_dict = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'password': usuario.password,
                'tipo_id': usuario.tipo.id,
            }
            usuario_dict["tipo"] = usuario.tipo.nombre
            return JsonResponse(usuario_dict)
        #añadir tipo de usuario 
        for u in usuario:
            print(u)
            tipo_usuario = TipoUsuario.objects.get(id=u["tipo_id"])
            u['tipo'] = tipo_usuario.nombre
        
        return Response(usuario)

    def post(self, request):
        if('email' in request.data and 'login' in request.data):
            print("entra aqui ")
            email = request.data['email']
            password = request.data['password']
            try:
                usuario = Usuario.objects.get(email=email, password=password)
            except Usuario.DoesNotExist:
                return Response({"message": "Usuario no existe"}, status=400)
            # usuario a json
            usuario_json = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'password': usuario.password,
                'tipo_usuario': usuario.tipo.nombre,
                'id_tipo': usuario.tipo.id,
                'suscrito': usuario.suscrito,
            }
            return Response(usuario_json)
        # validar que exista nombre y contraseña en el body
        try:
            verif = Usuario.objects.get(email=request.data['email'])
            print("Encontrado")
            return Response({"message": "Usuario ya existe"}, status=400)
        except Usuario.DoesNotExist:
            pass
        usuario = Usuario()
        usuario.nombre = request.data['nombre']
        usuario.apellido = request.data['apellido']
        usuario.email = request.data['email']
        usuario.password = request.data['password']
        if 'suscrito' in request.data:
            suscrito = request.data['suscrito']
        else:
            suscrito = False

        tipo_usuario = TipoUsuario.objects.get(id=request.data['tipo_usuario'])
        usuario.tipo = tipo_usuario
        usuario.suscrito = suscrito
        usuario.save()
        return Response({"message": "Usuario creado"})

    def put(self, request):
        # actualizar usuario
        if('suscribe' in request.data):
            usuario = Usuario.objects.get(id=request.data['id'])
            usuario.suscrito = True
            usuario.save()
            return Response({"message": "Usuario actualizado"})
        id = request.data['id']
        nombre = request.data['nombre']
        apellido = request.data['apellido']
        email = request.data['email']
        tipo_usuario = request.data['tipo_usuario']
        usuario = Usuario.objects.get(id=id)
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.email = email
        tipo_usuario = TipoUsuario.objects.get(id=tipo_usuario)
        usuario.tipo = tipo_usuario
        usuario.save()
        return Response({"message": "Usuario actualizado"})


class VentaApi(APIView):
    def get(self, request):
        venta = Venta.objects.all().values()
        return Response(venta)

    def post(self, request):
        # vali  dar que exista nombre en el body
        if 'idUsuario' in request.data:
            idUsuario = request.data['idUsuario']
            total = 0
            direccion = request.data['direccion']
            Tarjeta = request.data['Tarjeta']
            idCiudad = request.data['Ciudad']
            usuario = Usuario.objects.get(id=idUsuario)
            #obtener fecha actual en formato yyyy-mm-dd
            fecha = datetime.now().strftime("%Y-%m-%d")
            ciudad = Ciudad.objects.get(id=idCiudad)
            venta = Venta()
            venta.Ciudad = ciudad
            venta.usuario = usuario
            venta.fecha = fecha
            venta.total = total
            venta.direccion = direccion
            venta.Tarjeta = Tarjeta
            venta.save()
            #Obtener le id de la venta recien creada
            idVenta = venta.id
            return Response({"message": "Venta creada", "idVenta": idVenta})
        else:
            return Response({"message": "Faltan datos"}, status=400)

class CiudadApi(APIView):
    def get(self, request):
        idPais = request.query_params['idPais']
        pais = Pais.objects.get(id=idPais)
        ciudad = Ciudad.objects.filter(pais=pais).values()
        return Response(ciudad)

    
class PaisApi(APIView):
    def get(self, request):
        pais = Pais.objects.all().values()
        return Response(pais)


class ProductoVentaApi(APIView):
    def get(self, request):
        producto_venta = ProductoVenta.objects.all().values()
        return Response(producto_venta)

    def post(self, request):
        # vali  dar que exista nombre en el body
        if 'idVenta' in request.data and 'idProducto' in request.data:
            idVenta = request.data['idVenta']
            idProducto = request.data['idProducto']
            cantidad = request.data['cantidad']
            Ventas = Venta.objects.get(id=idVenta)
            Productos = Producto.objects.get(id=idProducto)
            producto_venta = ProductoVenta()
            producto_venta.venta = Ventas
            producto_venta.producto = Productos
            producto_venta.cantidad = cantidad
            producto_venta.save()
            Productos.stock = Productos.stock - int(cantidad)
            Productos.save()    
            Ventas.total = Ventas.total + Productos.precio * int(cantidad)
            Ventas.save()
            return Response({"message": "Producto agregado a la venta"})
        else:
            return Response({"message": "Faltan datos"}, status=400)