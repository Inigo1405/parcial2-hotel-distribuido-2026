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
**Qué encontré:**

Se encontró que el `booking-api/app/main.py` no tenia un manejo de errores adecuado para el publisher de RabbitMQ, ya que este continuaba indicando "202 Accepted" al cliente a pesar de que el servicio estaba caido.

**Cómo lo arreglé:**

Se le aplico un try-except al publisher de RabbitMQ, que en caso de error hace un logger al contenedor con las especificaciones del error y mientras que al cliente le manda un error 503 indicando que el servicio no se encuentra disponible.

**Por qué esto era un problema:**
* Tener falsos positivos en el sistema puede ocasionar problemas de confianza al cliente, ya que recibe una respuesta positiva a su solicitud mientras el sistema no responde a esta.
* Dificulta la detecció y respuesta a errores por parte del equipo de programación al no capturar los errores que se produzcan.


---

### B3 — Ack manual
**Qué encontré:**
En avalability-service usaba "autotrack=True" etro provoca que rabbitmq reciba el mesnaje como entrgado inmediatamente despues de enviarlo al consumidor sin esperar el callback terminara de procesarlo. 

**Cómo lo arreglé:**
Se cambio el "uto_ack=True" a "auto_ack=False" en en main.py de availability-service.
Al final del bloque del bloque del try se llama a ch.basic_ack(delivery_tag=method.delivery_tag)
En el bloque del except se llama a ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) para devolver el mensaje a la cola e intentarlo despues

**Por qué esto era un problema:**
SIn un acuse de recibo manuel cualquier fallo podira causar la perdida definitiva de la solicitud de la reserva. El cliente recibia un "202 Accepted" pero la reserva nunca se procesaba, con el ack manual se garantiza que solamente se considera cuando el trabajo esta realemnte hecho

---

### B6 — Credenciales en env vars
**Qué encontré:**

Se encontró en `payment-service/app/db.py` la conexión a la BD hardcodeada (DATABASE_URL), además de revuelto el archivo.

**Cómo lo arreglé:**

Se mando a llamar los componentes de la conexión desde las variables de entorno `.env` para construir el string de conexión con estas. Además se dividió el archivo en dos: `db.py` con la lógica de conexión y `models.py` con la definición de tablas.

**Por qué esto era un problema:**

* Esto representa un riesgo de seguridad, ya que al tener en código plano las credenciales de conexión a la BD, cualquier persona que lograra acceder al código podría obtenerlas y compremeter el sistema.
* Dificulta la escalabilidad y flexibilidad del sistema, al cerrar la configuraciones a datos específicos.
* Afecta la legibilidad y mantenimiento del código al mezclar la lógicas.

---

## notification-service completado

**Qué TODOs había:**

* TODO 1: Declarar el exchange hotel de tipo topic, crear la cola llamada notificaciones y enlazar a routing keys payment .completed y .failed
* TODO 2: implementar el callback que recibira el mensaje y xtraera los campos booking_id guest y event lo que generara un log estructurado
* TODO 3: Iniciar el consumidor usando basic_consume con auto_ack=False y luego start_consuming(), asegurando el recibo manual


**Cómo los implementé:**

* TODO 1: En la función main() se delaraa el exchange hotel, luego se declara la cola notifications, finalmente de enlaza la cola 2 veces una con payment.completed y otra con payment.failed. Tambien se creo el docker-compose.yml copiando el patron de availability-servic
* TODO 2: SE define la funcion callback y se analiza el JSON del cuerpo con .get se extrae booking_id, guest y event, se construyo el log segun las intruciones 
* TODO 3: En el main() despues de bidings e configura el consumidor, luego se llama a channel.start_consuming() para que el servicio quedde a la espera de mensaje


**Decisiones de diseño que tomé:**

Se uso el auto_ack=False y confirmo manualmente  solo despues de haber generado el log exitosamente. En caso de error se reencola l mensaje.
Cola no durable, se siguio el critero de los otros servicios ya que se requiere persisencia al reiniciar rabbitmq las colas se recrean
Uso de pika sincronico, se esocgio la misma librearia sincronica que avilitiby-service por simplificidad
Manejo de errores genericos con el callback captura cualquier excepcion, loguea el error y reencola el mensjae 

---

## Bugs arreglados (Tier 2)

### B4 — Overlap de fechas
**Qué TODOs había:**
* Detectar razón por la que el sistema no detectaba el solapamiento de fechas de reservación.
* Implementar formulas correspondientes para prevension del solapamiento de reservaciones.
* Dectar posibles casos de solapamiento de fechas de reservación y probar que el sistema los detecta correctamente.
* Probar funcionalidad del bloque implementado.

**Cómo los implementé:**
* Se integró una comparación de las fechas para detectar los posibles casos de solapamiento, y se remplazó la comparación incompleta para no interrumpir en la funcionalidad de la nueva lógica.

**Decisiones de diseño que tomé:**
* Se implementó la lógica de solapamiento con la siguiente formula: `check_in < Booking.check_out and check_out > Booking.check_in`, esta fórmula detecta cualquier tipo de solapamiento entre dos rangos de fechas.


### B5 — Race condition con `with_for_update()`
**Qué TODOs había:**
* Detectar bloque que permitia la condición de carrera.
* Implementar bloque de código con `with_for_update()` para prevenir la condición de carrera.
* Probar que la condición de carrera ya no se presenta.

**Cómo los implementé:**
* Se identificaron las secciones donde la session de la bases de datos se usaba en la sección de encontrar habitaciones disponibles, y se implementó lo siguiente: `.with_for_update(nowait=False)`, metodo de SQLAlchemy que bloquea las filas seleccionadas hasta estar disponibles.

**Decisiones de diseño que tomé:**
* Se uso `nowait=False` para que en caso de que una transacción intente acceder a una fila bloqueada espere a que esta se desbloquee, y mantenga esperando su turno para ser procesada.


### B7 — Idempotencia
**Qué encontré:**
El servicio de pagon no tenia maneras d e saber si un mimso evento de reserva confirmada ya lo habia reservado, si rabbitmq entregaba el mensjae 2 veces entonces el sistema cobraba 2 veces sin que este ko supiera, en la db no habia ningun registro que nos permitiera detectar que esa reservacion ya habia sido atendio

**Cómo lo arreglé:**
Se creo una nueva tabla en postgres llamada processed_events donde se guardo el booking_id cada ves que se procesa el pago, antes del cobro se pregunta si ese booking_id ya existe en la tabla. Si ya esta significa que el evento ya se proceso y entoences se salta y le digo a rabbitmq que todo esta bien, si no existe se incerte el booking_id, se hace el cobro y se guarda el pago

**Por qué esto era un problema:**
Rabbitmq puede reenviar el mensaje cuando un consumido falla antes de cornfirmar la recepcion, sin indepondencia ese doble envio significa doble cobro, con la tabla se evita ese riesgo y el sistema se vuelve tolerante a fallos

---

## Bonus que implementé (si aplica)

---

## Cosas que decidí NO hacer

(Ej: "no agregué tests porque preferí enfocarme en el flujo end-to-end", "no implementé saga porque no me dio tiempo", etc.)

---

## Si tuviera más tiempo, lo siguiente que mejoraría sería:
