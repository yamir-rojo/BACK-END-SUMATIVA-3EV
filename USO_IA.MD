El requerimiento 1, está correcto? 

r:parcialmente correcta

y ahora?

r: falta agregarla a installed_apps

y ahora está lista?

r: sí

"en producto, el sistema registra al menos 8 datos, entre, su línea, fotografía del producto, el precio en pesos, la cantidad de porciones, si es apto para celiacos, el stock y si está disponible para la venta."

para el requerimiento 3 se utilizó chatgpt para configurar las fotografías de los productos, con ImageField y pillow, y la configuración de media en settings y urls.

r: se instalaron las dependencias, se aplicó la migración y se probó subir una imagen desde el admin y verla.

intenté recuperar el chat de copilot que realicé en el laboratorio en la universidad, pero no lo tengo y no pude recuperarlo.

parte terminada de yamir.


Pablo Rojas

en que parte: requerimiento 4. Panel De Administracion

herramienta de IA: copilot

para que: se utilizo IA para ayudarme a integrar los filtros de producto especificamente en el de filtrar por línea y por si es apto para celíacos, y buscar por nombre. y tambien en el filtro de encargos especificamente en el filtro por producto y por fecha de retiro, y buscar por nombre o correo.

Pablo Rojas

en que parte: requerimiento 5. Catálogo público

herramienta de IA: copilot

para que: se utilizo IA para ayudarme a programar la lógica en la vista que permite usar la búsqueda por nombre y el filtro por línea al mismo tiempo, y para entender cómo configurar correctamente la respuesta de error 404 cuando un producto no existe o no está disponible.

Pablo Rojas

en que parte: requerimiento 6. Encargo público, control de stock y comprobante

herramienta de IA: copilot

para que: se utilizo IA para guiarme en cómo hacer la validación personalizada en el formulario para que la fecha de retiro no sea anterior al día de hoy, y para consultar la lógica de cómo descontar el stock del producto automáticamente justo al momento de guardar el encargo en la base de datos.

Pablo Rojas

en que parte: requerimiento 6. Encargo público, control de stock y comprobante

herramienta de IA: copilot

para que: se utilizo IA para darme ideas de cómo evitar que se duplique el encargo y se descuente el stock de nuevo si el usuario recarga la página del comprobante por accidente.

Pablo Rojas

en que parte: requerimiento 7. Usuarios y datos de prueba

herramienta de IA: copilot

para que: se utilizo IA para recordar los comandos de terminal necesarios para cambiar la contraseña del superusuario, y para aclarar cómo asignar permisos de solo lectura al grupo Cocina sin darles acceso total de administrador.