--------------------------------------
Funcionamiento:
	+ Se genera un mapa (TemplateMazmorra.py) utilizando random walk. Este mapa está compuesto por habitaciones (una de ellas inicial) y túneles. La casilla de partida del algoritmo será la habitación inicial. Durante la ejecución de random walk, si un tunel terminase en una casilla vacía se crearía en esa posición una habitación. Si un tunel se encuentra en su camino con una habitación, terminará de crearse.
	+ A partir de este mapa se genera la mazmorra (Mazmorra.py), de igual o mayor dimensión que el mapa (se indica con el argumento factor). La creación de la mazmorra sigue los siguientes pasos:
		- Se traduce el contenido del mapa para ajustarse a las dimensiones de la mazmorra.
		- Hasta que se alcance un índice de densidad máximo entre 0 y 1, se crearán nuevos túneles y se expandirán las habitaciones existentes. La creación de túneles tiene el mismo comportamiento que en el template. Siempre habrá un espacio entre habitaciones.
		- Una vez se alcance el nivel de densidad, se crean los objetos aleatoriamente en habitaciones cuyas dimensiones cumplan una condición.

--------------------------------------
Cómo ejecutarlo:
	+ Basta con ejecutar el fichero Main.py.
	+ El template se crea en Main.py > inicializar_template_mazmorra().
	+ La mazmorra se crea en Main.py > inicializar_generador().
	+ Los objetos se crean en Main.py > inicializar_objetos().

--------------------------------------
Anotaciones:
	+ Se proporciona la opción de imprimir por pantalla los pasos que ejecuta el algoritmo. Se debe indicar como argumento cuando se crean las instancias de TemplateMazmorra o Mazmorra.
	+ Debido a que no se han encontrado sprites para habitaciones y túneles que fueran agradables a la vista en conjunto, no es posible distinguir habitaciones de túneles mirando a los sprites. No obstante, se puede pulsar la tecla Q para alternar la visualización entre sprites y un código de colores:
		- Negro: Casilla vacía.
		- Gris: Túnel.
		- Blanco: Habitación.
		- Rojo: Habitación inicial.
		- Verde: Tesoro (sólo pueden aparecer en habitaciones).
	+ Se puede pulsar W para generar una nueva mazmorra utilizando el mismo template. Esta opción limpia la consola.
	+ Se puede pulsar E para generar un nuevo template y mazmorra. Esta opción limpia la consola.
