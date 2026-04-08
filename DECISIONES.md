# Decisiones técnicas

> Documenten brevemente las decisiones que tomaron resolviendo el examen. No copien del enunciado: expliquen con sus palabras qué hicieron y por qué. La intención es que al revisar pueda entender el razonamiento, no que repitan el problema.

---

## Bugs arreglados (Tier 1)

### B1 — Routing key
**Qué encontré:**
El problema era que los dos servicios no estaban coordinados. El booking-api publicaba eventos al exchange hotel con el routing key "ooking.created" pero availability-service pedia "booking.requested". AL no coincidir rabbitmq  no enrutaba los mensaje hacia el consumidor.
Ademas aunque el routig key lo cambie  los mensajes seguian sin llegar porque booking-api cerraba la conexion de manera inmediata lo que el broker no tenia tiempo para procesar el enrutameinto

**Cómo lo arreglé:**
Cambie el routing key en rabbitmq.py en el servicio de booking-api de "booking.create" a "booking.requested"
Agregue un pequeño await de 0.1 justo después de la publicacion para mantener la conexion abierta el tiempo suficiente para que rabbitmq termine de enrutar el mensaje hacia la cola

**Por qué esto era un problema:**
sin el routing key correcto se pirde el mensaje y el avalibity-servicenunca recibia el evento rompiendo el flujo

---

### B2 — Manejo de error en publish

---

### B3 — Ack manual

---

### B6 — Credenciales en env vars

---

## notification-service completado

**Qué TODOs había:**

**Cómo los implementé:**

**Decisiones de diseño que tomé:**

---

## Bugs arreglados (Tier 2)

### B4 — Overlap de fechas

### B5 — Race condition con `with_for_update()`

### B7 — Idempotencia

---

## Bonus que implementé (si aplica)

---

## Cosas que decidí NO hacer

(Ej: "no agregué tests porque preferí enfocarme en el flujo end-to-end", "no implementé saga porque no me dio tiempo", etc.)

---

## Si tuviera más tiempo, lo siguiente que mejoraría sería:
