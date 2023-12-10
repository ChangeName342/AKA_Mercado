class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def agregar(self, producto):
        idProd = str(producto.idProd)
        if idProd not in self.carrito.keys():
            self.carrito[idProd]={
                "producto_id": producto.idProd,
                "nombre": producto.nombre,
                "acumulado": producto.precio,
                "cantidad": 1,
            }
        else:
            self.carrito[idProd]["cantidad"] += 1
            self.carrito[idProd]["acumulado"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto):
        idProd = str(producto.idProd)
        if idProd in self.carrito:
            del self.carrito[idProd]
            self.guardar_carrito()

    def restar(self, producto):
        idProd = str(producto.idProd)
        if idProd in self.carrito.keys():
            self.carrito[idProd]["cantidad"] -= 1
            self.carrito[idProd]["acumulado"] -= producto.precio
            if self.carrito[idProd]["cantidad"] <= 0: self.eliminar(producto)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True