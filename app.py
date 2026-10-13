import os
from flask import Flask, render_template, request, jsonify
import stripe

app = Flask(__name__)

# Configurar la llave secreta de Stripe desde las variables de entorno de Railway
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
        cliente = data.get('cliente', {})

        line_items = []
        
        # Construir los elementos para la sesión de Stripe
        for item in carrito:
            line_items.append({
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': item['nombre'],
                    },
                    'unit_amount': int(item['precio'] * 100), # Stripe maneja centavos
                },
                'quantity': item['cantidad'],
            })

        # Agregar costo de envío si aplica a domicilio
        if tipo_entrega == 'domicilio':
            line_items.append({
                'price_data': {
                    'currency': 'mxn',
                    'product_data': {
                        'name': 'Servicio a Domicilio',
                    },
                    'unit_amount': 3500, # $35.00 MXN en centavos
                },
                'quantity': 1,
            })

        # Crear la sesión de pago en Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://' + request.host + '/exito',
            cancel_url='https://' + request.host + '/',
        )

        return jsonify({'url': checkout_session.url})

    except Exception as e:
        return jsonify({'error': str(e)}), 403

@app.route('/exito')
def exito():
    return "<h1 style='text-align:center; color:green; font-family:sans-serif; margin-top:50px;'>¡Pago exitoso! Gracias por tu pedido en la Carnicería El Buen Corte.</h1><p style='text-align:center; font-family:sans-serif;'>Puedes cerrar esta ventana y regresar al chat.</p>"

if __name__ == '__main__':
    # Leer el puerto de Railway, o usar 5000 como respaldo local
    port = int(os.environ.get('PORT', 5000))
    # host='0.0.0.0' es fundamental para escuchar peticiones de Railway
    app.run(host='0.0.0.0', port=port)
