<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carnicería El Buen Corte | Bobol Technologies</title>
    <style>
        :root { --primary: #d32f2f; --bg: #121212; --card-bg: #1e1e1e; --text: #ffffff; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 15px; }
        h1, h2, h3 { text-align: center; margin-bottom: 10px; }
        .categories { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
        .cat-btn { background: #333; color: white; border: none; padding: 10px 15px; border-radius: 20px; cursor: pointer; font-weight: bold; }
        .cat-btn.active { background: var(--primary); }
        .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 15px; max-width: 800px; margin: 0 auto; }
        .product-card { background: var(--card-bg); border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .product-card button { background: var(--primary); color: white; border: none; padding: 8px 12px; border-radius: 4px; cursor: pointer; margin-top: 10px; width: 100%; font-weight: bold; }
        
        /* Carrito y Formulario */
        .cart-section { max-width: 600px; margin: 30px auto; background: var(--card-bg); padding: 20px; border-radius: 10px; }
        .form-group { margin-bottom: 15px; text-align: left; }
        .form-group label { display: block; margin-bottom: 5px; font-size: 14px; }
        .form-group input, .form-group select { width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #444; background: #2a2a2a; color: white; box-sizing: border-box; }
        .btn-pay { background: #28a745; color: white; border: none; padding: 12px; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; margin-top: 10px; }
        .btn-cash { background: #ff9800; color: white; border: none; padding: 12px; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; margin-top: 10px; }
        .hidden { display: none; }
    </style>
</head>
<body>

    <h1>🥩 Carnicería El Buen Corte</h1>
    <p style="text-align:center; color: #aaa;">Pide en línea y recibe en tu domicilio o recoge en tienda</p>

    <!-- Filtro de Categorías -->
    <div class="categories">
        <button class="cat-btn active" onclick="filtrar('res')">Res</button>
        <button class="cat-btn" onclick="filtrar('cerdo')">Cerdo</button>
        <button class="cat-btn" onclick="filtrar('pollo')">Pollo</button>
        <button class="cat-btn" onclick="filtrar('especialidades')">Especialidades</button>
    </div>

    <!-- Rejilla de Productos -->
    <div class="product-grid" id="contenedor-productos"></div>

    <!-- Sección de Carrito y Checkout -->
    <div class="cart-section">
        <h2>🛒 Tu Pedido</h2>
        <div id="items-carrito"><p style="color: #888;">No has agregado productos.</p></div>
        <hr style="border-color: #333; margin: 15px 0;">
        
        <!-- Opciones de Entrega -->
        <div class="form-group">
            <label>Tipo de Entrega:</label>
            <select id="tipo-entrega" onchange="actualizarTotal()">
                <option value="recoger">Recoger en Sucursal ($0 MXN)</option>
                <option value="domicilio">Servicio a Domicilio (+$35 MXN)</option>
            </select>
        </div>

        <!-- Campos de Dirección (Solo si es a Domicilio) -->
        <div id="campos-direccion" class="hidden">
            <div class="form-group">
                <label>Nombre Completo:</label>
                <input type="text" id="nombre-cliente" placeholder="Ej. Miguel Angulo">
            </div>
            <div class="form-group">
                <label>Dirección Completa (Calle, #, Colonia):</label>
                <input type="text" id="direccion-cliente" placeholder="Ej. Av. Hidalgo #123, Col. Centro">
            </div>
            <div class="form-group">
                <label>Teléfono de Contacto:</label>
                <input type="tel" id="telefono-cliente" placeholder="Ej. 4611234567">
            </div>
        </div>

        <h3>Total: <span id="total-precio">$0.00</span> MXN</h3>

        <!-- Métodos de Pago -->
        <button class="btn-pay" onclick="procesarPago('tarjeta')">💳 Pagar con Tarjeta (Link Seguro)</button>
        <button class="btn-cash" onclick="procesarPago('efectivo')">💵 Pagar en Efectivo (WhatsApp)</button>
    </div>

    <script>
        const productos = [
            // RES
            { id: 1, categoria: 'res', nombre: 'Bisteck de Bola', precio: 180 },
            { id: 2, categoria: 'res', nombre: 'Chambarete', precio: 140 },
            { id: 3, categoria: 'res', nombre: 'Costilla de Res', precio: 160 },
            { id: 4, categoria: 'res', nombre: 'Falda', precio: 170 },
            { id: 5, categoria: 'res', nombre: 'Suadero', precio: 150 },
            { id: 6, categoria: 'res', nombre: 'Cocido', precio: 130 },
            { id: 7, categoria: 'res', nombre: 'Filete', precio: 260 },
            { id: 8, categoria: 'res', nombre: 'Molida de Res', precio: 150 },
            
            // CERDO
            { id: 9, categoria: 'cerdo', nombre: 'Maciza / Pierna', precio: 110 },
            { id: 10, categoria: 'cerdo', nombre: 'Costilla de Cerdo', precio: 130 },
            { id: 11, categoria: 'cerdo', nombre: 'Chuleta de Cerdo', precio: 120 },
            { id: 12, categoria: 'cerdo', nombre: 'Cabeza', precio: 80 },
            { id: 13, categoria: 'cerdo', nombre: 'Lomo', precio: 135 },
            { id: 14, categoria: 'cerdo', nombre: 'Molida de Cerdo', precio: 100 },
            { id: 15, categoria: 'cerdo', nombre: 'Tocineta (Natural/Adobada)', precio: 140 },

            // POLLO
            { id: 16, categoria: 'pollo', nombre: 'Pierna y Muslo (Kg)', precio: 65 },
            { id: 17, categoria: 'pollo', nombre: 'Pechuga (Kg)', precio: 110 },
            { id: 18, categoria: 'pollo', nombre: 'Pollo Entero', precio: 180 },
            { id: 19, categoria: 'pollo', nombre: 'Huevo (Kilo)', precio: 45 },

            // ESPECIALIDADES
            { id: 20, categoria: 'especialidades', nombre: 'Chuleta Ahumada', precio: 140 },
            { id: 21, categoria: 'especialidades', nombre: 'Alambre', precio: 170 },
            { id: 22, categoria: 'especialidades', nombre: 'Carne p/ Hamburguesa', precio: 150 },
            { id: 23, categoria: 'especialidades', nombre: 'Arrachera', precio: 240 },
            { id: 24, categoria: 'especialidades', nombre: 'Tomahawk', precio: 320 },
            { id: 25, categoria: 'especialidades', nombre: 'Rib Eye', precio: 310 },
            { id: 26, categoria: 'especialidades', nombre: 'Bisteck Taquero', precio: 160 },
            { id: 27, categoria: 'especialidades', nombre: 'Chorizo', precio: 120 },
            { id: 28, categoria: 'especialidades', nombre: 'Chistorra', precio: 180 },
            { id: 29, categoria: 'especialidades', nombre: 'Longaniza', precio: 120 }
        ];

        let carrito = [];

        function renderProductos(cat) {
            const container = document.getElementById('contenedor-productos');
            container.innerHTML = '';
            const filtrados = productos.filter(p => p.categoria === cat);
            
            filtrados.forEach(p => {
                container.innerHTML += `
                    <div class="product-card">
                        <h3>${p.nombre}</h3>
                        <p>$${p.precio}.00 MXN / kg</p>
                        <button onclick="agregarAlCarrito(${p.id})">+ Agregar</button>
                    </div>
                `;
            });
        }

        function filtrar(cat) {
            document.querySelectorAll('.cat-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            renderProductos(cat);
        }

        function agregarAlCarrito(id) {
            const prod = productos.find(p => p.id === id);
            const existe = carrito.find(item => item.id === id);
            if(existe) {
                existe.cantidad++;
            } else {
                carrito.push({...prod, cantidad: 1});
            }
            actualizarTotal();
        }

        function actualizarTotal() {
            const container = document.getElementById('items-carrito');
            const tipoEntrega = document.getElementById('tipo-entrega').value;
            const camposDireccion = document.getElementById('campos-direccion');
            
            if(tipoEntrega === 'domicilio') {
                camposDireccion.classList.remove('hidden');
            } else {
                camposDireccion.classList.add('hidden');
            }

            if(carrito.length === 0) {
                container.innerHTML = '<p style="color: #888;">No has agregado productos.</p>';
                document.getElementById('total-precio').innerText = '0.00';
                return;
            }

            let subtotal = 0;
            container.innerHTML = '';
            carrito.forEach(item => {
                subtotal += item.precio * item.cantidad;
                container.innerHTML += `<p>• ${item.nombre} x${item.cantidad} - $${item.precio * item.cantidad} MXN</p>`;
            });

            let costoEnvio = (tipoEntrega === 'domicilio') ? 35 : 0;
            let total = subtotal + costoEnvio;

            document.getElementById('total-precio').innerText = total.toFixed(2);
        }

        async function procesarPago(metodo) {
            if(carrito.length === 0) return alert("Agrega al menos un producto al carrito.");
            
            const tipoEntrega = document.getElementById('tipo-entrega').value;
            const nombre = document.getElementById('nombre-cliente').value;
            const direccion = document.getElementById('direccion-cliente').value;
            const telefono = document.getElementById('telefono-cliente').value;

            if(tipoEntrega === 'domicilio' && (!nombre || !direccion || !telefono)) {
                return alert("Por favor llena todos los datos de envío.");
            }

            if(metodo === 'tarjeta') {
                // Pago con Stripe en Railway
                const res = await fetch('/crear-sesion-pago', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        carrito: carrito,
                        tipoEntrega: tipoEntrega,
                        cliente: { nombre, direccion, telefono }
                    })
                });
                const data = await res.json();
                if(data.url) window.location.href = data.url;
                else alert("Error al conectar con Stripe: " + data.error);
            } else {
                // Pago en Efectivo -> Redirección limpia a WhatsApp
                let mensaje = `*NUEVO PEDIDO - CARNICERÍA EL BUEN CORTE*\n\n`;
                carrito.forEach(i => mensaje += `• ${i.nombre} x${i.cantidad} ($${i.precio * i.cantidad} MXN)\n`);
                mensaje += `\n*Tipo de Entrega:* ${tipoEntrega.toUpperCase()}`;
                if(tipoEntrega === 'domicilio') {
                    mensaje += ` (+$35 MXN Envío)\n`;
                    mensaje += `*Cliente:* ${nombre}\n*Dirección:* ${direccion}\n*Teléfono:* ${telefono}\n`;
                }
                mensaje += `\n*TOTAL A PAGAR (EFECTIVO):* $${document.getElementById('total-precio').innerText} MXN`;
                
                window.location.href = `https://wa.me/5214610000000?text=${encodeURIComponent(mensaje)}`;
            }
        }

        // Cargar primera categoría por defecto
        renderProductos('res');
    </script>
</body>
</html>
