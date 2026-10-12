import os
from flask import Flask, jsonify, render_template, request
import stripe

app = Flask(__name__)

# Llave secreta de prueba de Stripe
stripe.api_key = os.getenv(
    "STRIPE_SECRET_KEY", "sk_test_tu_llave_aqui_de_prueba"
)


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/crear-sesion-pago", methods=["POST"])
def crear_sesion_pago():
  try:
    datos = request.json
    carrito = datos.get("carrito", [])
    tipo_entrega = datos.get("tipoEntrega", "recoger")
    cliente = datos.get("cliente", {})

    line_items = []
    for item in carrito:
      line_items.append({
          "price_data": {
              "currency": "mxn",
              "product_data": {
                  "name": item["nombre"],
              },
              "unit_amount": int(
                  item["precio"] * 100
              ),  # Convertir pesos a centavos
          },
          "quantity": item.get("cantidad", 1),
      })

    # Si es servicio a domicilio, agregamos la tarifa de envío de $35 MXN
    if tipo_entrega == "domicilio":
      line_items.append({
          "price_data": {
              "currency": "mxn",
              "product_data": {
                  "name": "Servicio a Domicilio",
              },
              "unit_amount": 3500,  # $35.00 MXN
          },
          "quantity": 1,
      })

    # Crear la sesión de pago en Stripe
    sesion = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.host_url + "?status=success",
        cancel_url=request.host_url + "?status=cancel",
    )

    return jsonify({"url": sesion.url})
  except Exception as e:
    return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))