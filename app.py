import os
from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__, template_folder='.')

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crear-sesion-pago', methods=['POST'])
def crear_sesion_pago():
    try:
        data = request.get_json()
        carrito = data.get('carrito', [])
        tipo_entrega = data.get('tipoEntrega', 'recoger')

        line_items = []
        for item in carrito:
            line_items.append({
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {'name': item['nombre']},
                    'unit_amount': int(item['precio'] * 100),
                },
                'quantity': item['cantidad'],
            })

        if tipo_entrega == 'domicilio':
            line_items.append({
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {'name': 'Servicio a Domicilio'},
                    'unit_amount': 3500,
                },
                'quantity': 1,
            })

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url='https://' + request.host + '/exito',
            cancel_url='https://' + request.host + '/',
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/exito')
def exito():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>¡Pago Exitoso! - Carnicería El Buen Corte</title>
        <meta http-equiv="refresh" content="3;url=/">
        <style>
            body { background-color: #121212; color: #fff; font-family: sans-serif; text-align: center; padding-top: 100px; }
            .card { background: #1e1e1e; max-width: 400px; margin: auto; padding: 30px; border-radius: 10px; border: 1px solid #333; }
            h1 { color: #27ae60; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>¡Pago Exitoso! 🥩</h1>
            <p>Muchas gracias por tu compra en El Buen Corte.</p>
            <p style="font-size: 0.9rem; color: #aaa;">Te estamos redirigiendo de regreso a la tienda...</p>
        </div>
        <script>
            // Limpia el carrito almacenado localmente al completarse el pago
            localStorage.removeItem('carrito');
            setTimeout(function() {
                window.location.href = '/';
            }, 3000);
        </script>
    </body>
    </html>
    """
