# Declaración de uso de IA

> Llenen este archivo si alguno de los dos usó alguna herramienta de IA generativa (Claude, ChatGPT, Copilot, Gemini, etc.) durante el examen. Hacerlo es **obligatorio** y se evalúa con honestidad: declarar correctamente no penaliza, lo que penaliza es **no declarar** y que se detecte uso.
>
> Indiquen también **quién** de los dos integrantes la usó (puede ser uno solo, ambos, o ninguno).

## ¿Usaron IA?

- [ ] Sí
- [ ] No

## ¿Quién la usó?

- [ ] Integrante 1
- [ ] Integrante 2
- [ ] Ambos

---

## Si la respuesta es "Sí":

### Herramientas usadas
(Ej: Claude.ai, ChatGPT-4, GitHub Copilot, Cursor, etc.)

-

### Prompts principales
Listen los 3-5 prompts más importantes que escribieron y para qué los usaron.

1. **Prompt:** Le mostré a la IA los logs de `docker compose up --build` donde el `booking-api` publicaba el evento pero el `availability-service` nunca mostraba "Recibido booking.requested". Le pegué los logs y le pregunté por qué pasaba eso.
   **Para qué:** Diagnosticar por qué el mensaje no llegaba al consumidor a pesar de haber cambiado el routing key.
   **Quién lo usó:** Integrante 2
   **Qué tan útil fue:** 5

2. **Prompt:** Le compartí el código de `booking-api/app/rabbitmq.py` y los logs de RabbitMQ donde aparecía "client unexpectedly closed TCP connection". Le pregunté si esos warnings eran graves y si podían estar causando la pérdida de mensajes.
   **Para qué:** Entender si el cierre abrupto de la conexión afectaba la entrega y cómo solucionarlo.
   **Quién lo usó:** Integrante 2
   **Qué tan útil fue:** 5

5. **Prompt:** Le pedí que me explicara cómo implementar idempotencia en `payment-service` para evitar cobros duplicados cuando RabbitMQ reenviara el mismo mensaje. Le mostré el código actual de `process_event` y le pedí una solución con tabla `processed_events`.
   **Para qué:** Resolver B7 de manera correcta y atómica.
   **Quién lo usó:** Integrante 2
   **Qué tan útil fue:** 5

### ¿En qué partes los apoyó?
- La IA me ayudo sobre todo a entender por que el mensaje no llegaba al availability-service: me explico que no bastaba con cambiar el routing key, sino que ademas habia que mantener la conexion abierta un poco mas con un sleep. Para la idempotencia, me dio la logica de la tabla processed_events y como usar transacciones atomicas para evitar cobros dobles. Ademas me enseño a probar todo con los comandos. Para la idempotencia, me dio la logica de la tabla processed_events y como usar transacciones atomicas para evitar cobros dobles. Ademas me enseño a probar todo con los comandos

### ¿Hubo cosas en las que la IA dio respuestas incorrectas o que tuvieron que corregir?
- La IA me sugirio el sleep(0.1) para el cierre de conexion, y aunque funciono, ella reconocio que no es la mejor practica. Tambien me dio un codigo de idempotencia con create_async_engine importado de sqlalchemy en lugar de sqlalchemy.ext.asyncio. En la primera version del notification-service, la IA me dijo que usara un while True con sleep,

### ¿Qué decidieron hacer manualmente sin IA y por qué?
- La logica del notification-service, el codigo de la conexion, el exchange, la cola, los bindings, el callback y el ack manual
