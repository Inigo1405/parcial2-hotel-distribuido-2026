"""notification-service – consumer que loggea notificaciones de pago.

ESTE SERVICIO ESTÁ INCOMPLETO. Tu trabajo es resolver los TODOs de abajo.

El servicio debe consumir eventos `payment.completed` y `payment.failed` del
exchange `hotel`, y por cada uno loggear de forma estructurada el "envío" de
la notificación. No se manda email real: solo se loggea con un formato
específico que se evalúa.

Formato del log esperado:
[NOTIFICATION] booking_id=<id> event=PAYMENT_COMPLETED guest=<name> channel=email status=SENT

Pista: copia el patrón de availability-service/app/main.py, pero adaptado a
los routing keys de pago. Usa ack manual.
"""

import json
import logging
import os
import time
import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("notification-service")

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


def main():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # TODO 1: declarar el exchange 'hotel' (tipo topic) y bindear una queue
    # llamada 'notifications' a los routing keys 'payment.completed' y
    # 'payment.failed'. Recuerda que un binding va de exchange → queue con
    # un routing key específico, y puedes hacer dos bindings sobre la misma
    # queue.result = channel.queue_declare(queue="notifications", durable=False)
    channel.exchange_declare(exchange="hotel", exchange_type="topic")
    result = channel.queue_declare(queue="notifications", durable=False)
    channel.queue_bind(exchange="hotel", queue=result.method.queue, routing_key="payment.completed")
    channel.queue_bind(exchange="hotel", queue=result.method.queue, routing_key="payment.failed")
    logger.info("notification-service TODO 1 listo, exchange y bindings listos")


    # TODO 2: implementar el callback que reciba (ch, method, properties, body),
    # parsee el JSON, y loggee con el formato exacto:
    #   [NOTIFICATION] booking_id=<id> event=<EVENT> guest=<name> channel=email status=SENT
    # No olvides hacer ack manual al final del callback (ch.basic_ack).
    logger.info("otification-service iniciado, pero los TODOs no están resueltos todavia")

    # TODO 3: iniciar el consumer con channel.basic_consume(...) usando ack
    # manual y luego channel.start_consuming().

    logger.info("notification-service iniciado, pero los TODOs no están resueltos todavia")
    # Mientras los TODOs no se resuelvan, este servicio no consume nada.
    # Reemplaza este loop infinito con tu lógica.
    import time
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
