import os
from flask import Flask, render_template, request, jsonify
import stripe

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_DIR)
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
            payment_method_types=['card'],
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
    return "<h1 style='text-align:center; color:green;'>¡Pago exitoso!</h1>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
