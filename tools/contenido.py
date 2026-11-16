"""Contenido de las páginas de tratamientos.

Cada tratamiento genera una página en /<slug>/ (por ejemplo /implantes/).
Los textos admiten HTML sencillo (<p>, <ul>, <a>, <strong>).
Después de editar este archivo, ejecuta:  python tools/generar.py
"""

TRATAMIENTOS = [
    {
        "slug": "implantes",
        "nombre": "Implantes dentales",
        "h1": "Implantes dentales en Leganés",
        "titulo": "Implantes dentales en Leganés | Dra. Eva Martín Molina",
        "descripcion": "Implantes dentales en Leganés para reponer uno o varios dientes. Estudio y tratamiento por la Dra. Eva Martín Molina. Pide cita en el 91 680 67 24.",
        "resumen": "La solución más estable cuando falta un diente.",
        "intro": "Un implante sustituye la raíz de un diente perdido y sirve de base para una corona fija. Es la forma más estable de recuperar un diente: se ve, se siente y se usa como uno natural.",
        "secciones": [
            ("¿Cuándo se recomienda un implante?", """
<p>Cuando falta uno o varios dientes, ya sea por una extracción, un golpe o un problema de encías. Con implantes podemos:</p>
<ul>
  <li><strong>Reponer un solo diente</strong> sin tallar los dientes vecinos, como ocurre con un puente tradicional.</li>
  <li><strong>Reponer varios dientes</strong> con un puente fijo apoyado sobre implantes.</li>
  <li><strong>Fijar una dentadura completa</strong> para que no se mueva al hablar ni al comer.</li>
</ul>
<p>Cada caso es distinto. Antes de decidir hay que valorar la cantidad de hueso, el estado de las encías y tu salud general.</p>
"""),
            ("Ventajas de los implantes", """
<ul>
  <li>Son fijos: no hay que quitarlos para dormir ni para limpiarlos.</li>
  <li>No obligan a tallar dientes sanos.</li>
  <li>Ayudan a conservar el hueso, que tiende a perderse cuando falta un diente.</li>
  <li>Permiten masticar con seguridad y hablar con naturalidad.</li>
</ul>
"""),
            ("Cuidados después del tratamiento", """
<p>Un implante no tiene caries, pero la encía que lo rodea sí puede inflamarse. Para que dure muchos años:</p>
<ul>
  <li>Cepíllate después de cada comida, también alrededor del implante.</li>
  <li>Usa seda dental o cepillos interproximales a diario.</li>
  <li>Acude a tus revisiones y limpiezas profesionales.</li>
  <li>Si fumas, intenta dejarlo: el tabaco es uno de los principales riesgos para los implantes.</li>
</ul>
"""),
        ],
        "pasos": [
            ("Estudio y diagnóstico", "Exploramos la boca y hacemos las radiografías necesarias para medir el hueso y planificar la posición del implante."),
            ("Colocación del implante", "Se realiza en la clínica con anestesia local. Te explicamos antes cómo será y qué cuidados tener los días siguientes."),
            ("Integración en el hueso", "Durante unos meses el implante se une al hueso. Según el caso, puedes llevar una prótesis provisional mientras tanto."),
            ("Corona o prótesis definitiva", "Tomamos medidas y colocamos la corona o la prótesis fija sobre el implante."),
            ("Revisiones", "Revisamos el implante y la encía periódicamente para asegurarnos de que todo sigue bien."),
        ],
        "faqs": [
            ("¿Duele ponerse un implante?", "Se coloca con anestesia local, así que durante la intervención no se siente dolor. Después es normal notar molestias o inflamación unos días, que se controlan con la medicación que te indiquemos."),
            ("¿Cuánto dura un implante?", "Con buena higiene y revisiones periódicas, un implante puede durar muchos años. Su duración depende sobre todo del cuidado de las encías y de hábitos como el tabaco."),
            ("¿Puede ponerse implantes cualquier persona?", "La mayoría de los adultos sí, pero hay que valorar el hueso disponible, las encías y la salud general. En algunos casos hace falta un tratamiento previo."),
            ("¿Cuánto cuesta un implante?", "Depende del número de implantes y del tipo de prótesis. Después del estudio te explicamos el presupuesto detallado antes de empezar."),
        ],
        "relacionados": ["estetica-dental", "odontologia-general"],
    },
    {
        "slug": "ortodoncia",
        "nombre": "Ortodoncia",
        "h1": "Ortodoncia en Leganés para niños y adultos",
        "titulo": "Ortodoncia en Leganés para niños y adultos | Dra. Eva Martín",
        "descripcion": "Ortodoncia en Leganés para niños, adolescentes y adultos. Corregimos apiñamiento, separaciones y problemas de mordida. Pide cita en el 91 680 67 24.",
        "resumen": "Corrige la posición de los dientes y la mordida.",
        "intro": "La ortodoncia corrige la posición de los dientes y la forma en que encajan al morder. Una boca bien alineada es más fácil de limpiar y reparte mejor las fuerzas al masticar.",
        "secciones": [
            ("¿Qué problemas trata la ortodoncia?", """
<ul>
  <li>Dientes apiñados o torcidos.</li>
  <li>Separaciones entre los dientes.</li>
  <li>Mordida cruzada, abierta o demasiado profunda.</li>
  <li>Dientes muy adelantados o retrasados.</li>
</ul>
"""),
            ("Ortodoncia en niños", """
<p>Es buena idea hacer una primera revisión de ortodoncia hacia los 6 o 7 años. Algunos problemas de mordida se corrigen mejor mientras los huesos están creciendo, y detectarlos a tiempo puede simplificar el tratamiento más adelante.</p>
"""),
            ("Ortodoncia en adultos", """
<p>Nunca es tarde para alinear los dientes si las encías y el hueso están sanos. Muchos adultos prefieren la <a href="/ortodoncia-invisible/">ortodoncia invisible</a>, con alineadores transparentes que apenas se notan.</p>
"""),
        ],
        "pasos": [
            ("Primera visita y estudio", "Hacemos fotografías, radiografías y registros de tu mordida para conocer bien el caso."),
            ("Plan de tratamiento", "Te explicamos las opciones, la duración aproximada y el presupuesto antes de empezar."),
            ("Colocación de los aparatos", "Colocamos los brackets o el aparato elegido y te enseñamos a cuidarlo."),
            ("Revisiones periódicas", "Ajustamos el tratamiento en cada visita para guiar el movimiento de los dientes."),
            ("Retención", "Al terminar, un retenedor mantiene los dientes en su nueva posición."),
        ],
        "faqs": [
            ("¿Cuánto dura un tratamiento de ortodoncia?", "Depende de cada caso y de la edad. Después del estudio te damos una estimación personalizada."),
            ("¿Duele llevar brackets?", "Los primeros días y después de cada ajuste es normal notar presión o molestias leves, que desaparecen en poco tiempo."),
            ("¿Puedo comer de todo con brackets?", "Conviene evitar alimentos muy duros o pegajosos que puedan despegar los brackets. Te damos una lista de recomendaciones al empezar."),
            ("¿Qué es la retención?", "Es la fase final: un retenedor fijo o removible que evita que los dientes vuelvan a moverse una vez terminado el tratamiento."),
        ],
        "relacionados": ["ortodoncia-invisible", "odontologia-general"],
    },
    {
        "slug": "ortodoncia-invisible",
        "nombre": "Ortodoncia invisible",
        "h1": "Ortodoncia invisible en Leganés",
        "titulo": "Ortodoncia invisible en Leganés | Alineadores transparentes",
        "descripcion": "Ortodoncia invisible en Leganés con alineadores transparentes a medida. Corrige tu sonrisa sin brackets visibles. Clínica Dental Dra. Eva Martín Molina.",
        "resumen": "Alineadores transparentes que casi no se notan.",
        "intro": "Los alineadores son férulas transparentes hechas a medida que mueven los dientes poco a poco. Apenas se notan y se quitan para comer y para cepillarse.",
        "secciones": [
            ("Ventajas de la ortodoncia invisible", """
<ul>
  <li><strong>Casi no se ven</strong>, así que puedes llevarlos en el trabajo o en cualquier situación.</li>
  <li><strong>Se quitan para comer</strong>: no hay que renunciar a ningún alimento.</li>
  <li><strong>La higiene es más fácil</strong>, porque te cepillas los dientes como siempre.</li>
  <li><strong>Son cómodos</strong>: no tienen piezas metálicas que rocen.</li>
</ul>
"""),
            ("¿Para quién es?", """
<p>Es una opción muy adecuada para adultos y adolescentes con apiñamiento, separaciones o dientes que se han movido después de una ortodoncia anterior. Algunos casos complejos se resuelven mejor con <a href="/ortodoncia/">ortodoncia con brackets</a>; lo valoramos contigo en el estudio.</p>
"""),
            ("Tu parte del tratamiento", """
<p>Para que los alineadores funcionen hay que llevarlos puestos la mayor parte del día, unas 20 a 22 horas, y quitarlos solo para comer y para la higiene.</p>
"""),
        ],
        "pasos": [
            ("Estudio", "Revisamos tus dientes y encías y tomamos los registros necesarios."),
            ("Planificación", "Diseñamos el movimiento de los dientes y te enseñamos cómo será el resultado previsto."),
            ("Entrega de los alineadores", "Te entregamos los alineadores y te explicamos cada cuánto cambiarlos."),
            ("Revisiones", "Comprobamos en la clínica que los dientes se mueven según lo previsto."),
            ("Retención", "Al terminar, un retenedor mantiene el resultado."),
        ],
        "faqs": [
            ("¿Se notan los alineadores?", "Son transparentes y se adaptan a tus dientes, por lo que a una distancia normal casi nadie se da cuenta de que los llevas."),
            ("¿Duelen?", "Al cambiar de alineador es normal notar presión uno o dos días. Es la señal de que los dientes se están moviendo."),
            ("¿Puedo quitármelos?", "Sí, para comer, beber algo que no sea agua y cepillarte. El resto del tiempo deben estar puestos."),
            ("¿Cuánto dura el tratamiento?", "Depende del caso. Después del estudio te damos una estimación personalizada."),
        ],
        "relacionados": ["ortodoncia", "blanqueamiento-dental"],
    },
    {
        "slug": "estetica-dental",
        "nombre": "Estética dental",
        "h1": "Estética dental en Leganés",
        "titulo": "Estética dental en Leganés | Carillas y fundas",
        "descripcion": "Carillas, fundas y reconstrucciones estéticas en Leganés para mejorar el color, la forma y el tamaño de tus dientes con un resultado natural.",
        "resumen": "Carillas, fundas y retoques para la sonrisa que buscas.",
        "intro": "Mejoramos el color, la forma y el tamaño de los dientes buscando siempre un resultado natural, que encaje con tu cara y tu forma de sonreír.",
        "secciones": [
            ("Tratamientos de estética dental", """
<ul>
  <li><strong>Carillas</strong>: láminas finas que se adhieren a la cara visible del diente para corregir su color, forma o pequeñas separaciones.</li>
  <li><strong>Fundas o coronas</strong>: cubren el diente entero. Se usan cuando está muy dañado, tiene grandes empastes o ha recibido una endodoncia.</li>
  <li><strong>Reconstrucciones estéticas</strong>: reparan pequeñas fracturas o bordes desgastados con material del color del diente.</li>
  <li><strong><a href="/blanqueamiento-dental/">Blanqueamiento dental</a></strong>: aclara el tono de los dientes naturales.</li>
</ul>
"""),
            ("Un resultado natural", """
<p>Antes de proponerte nada estudiamos tus dientes, tus encías y tu sonrisa. Así elegimos el tratamiento más sencillo que consigue lo que buscas, sin hacer más de lo necesario.</p>
"""),
        ],
        "pasos": [
            ("Valoración", "Revisamos la salud de tus dientes y encías y hablamos de lo que te gustaría cambiar."),
            ("Propuesta", "Te explicamos las opciones posibles, con sus ventajas y su presupuesto."),
            ("Tratamiento", "Preparamos los dientes si es necesario y colocamos las carillas, fundas o reconstrucciones."),
            ("Revisiones", "Comprobamos que todo está bien ajustado y te damos pautas de cuidado."),
        ],
        "faqs": [
            ("¿Carillas o fundas?", "Las carillas cubren solo la parte visible y conservan más diente. Las fundas cubren el diente entero y se reservan para dientes más dañados. En la valoración te decimos qué opción es mejor en tu caso."),
            ("¿Se nota que no son dientes naturales?", "Elegimos el color y la forma para que se integren con el resto de tus dientes y el resultado sea natural."),
            ("¿Cuánto duran?", "Con buena higiene y revisiones, las carillas y las fundas pueden durar muchos años. Conviene evitar morder objetos duros."),
        ],
        "relacionados": ["blanqueamiento-dental", "implantes"],
    },
    {
        "slug": "blanqueamiento-dental",
        "nombre": "Blanqueamiento dental",
        "h1": "Blanqueamiento dental en Leganés",
        "titulo": "Blanqueamiento dental en Leganés | Dra. Eva Martín Molina",
        "descripcion": "Blanqueamiento dental en Leganés supervisado por la doctora. Revisamos dientes y encías antes de empezar para aclarar el tono de forma segura.",
        "resumen": "Dientes más blancos con un tratamiento supervisado.",
        "intro": "El blanqueamiento aclara el tono de los dientes naturales. Hecho y controlado por un profesional, es un tratamiento seguro para el esmalte.",
        "secciones": [
            ("¿Por qué se oscurecen los dientes?", """
<p>Con los años los dientes van perdiendo blancura. También influyen el café, el té, el vino, el tabaco y algunos medicamentos.</p>
"""),
            ("Antes de blanquear", """
<p>Revisamos tus dientes y encías y, si hace falta, hacemos una limpieza o tratamos caries antes de empezar. Ten en cuenta que el blanqueamiento solo aclara los dientes naturales: no cambia el color de empastes, fundas ni carillas.</p>
"""),
            ("Cómo mantener el resultado", """
<ul>
  <li>Modera el café, el té, el vino y evita el tabaco.</li>
  <li>Mantén una buena higiene y tus limpiezas periódicas.</li>
  <li>Si con el tiempo el tono baja, puede hacerse un repaso.</li>
</ul>
"""),
        ],
        "pasos": [
            ("Revisión", "Comprobamos que dientes y encías están sanos y registramos el color inicial."),
            ("Tratamiento", "Aplicamos el producto blanqueador en la concentración adecuada para tu caso, siempre bajo supervisión."),
            ("Control", "Revisamos el resultado y la posible sensibilidad, y te damos pautas para mantenerlo."),
        ],
        "faqs": [
            ("¿El blanqueamiento daña el esmalte?", "Hecho y controlado por un profesional, con los productos y concentraciones adecuados, el blanqueamiento no daña el esmalte."),
            ("¿Es normal notar sensibilidad?", "Algunas personas notan sensibilidad durante el tratamiento. Es pasajera y desaparece al terminar."),
            ("¿Cuánto dura el resultado?", "Depende de tus hábitos. Evitando el tabaco y moderando el café, el té y el vino, el resultado se mantiene mucho tiempo."),
            ("¿Blanquea los empastes y las fundas?", "No. Solo aclara los dientes naturales; si tienes empastes visibles, puede que haya que cambiarlos después para igualar el color."),
        ],
        "relacionados": ["estetica-dental", "odontologia-general"],
    },
    {
        "slug": "ferulas-bruxismo",
        "nombre": "Férulas para el bruxismo",
        "h1": "Férulas de descarga para el bruxismo en Leganés",
        "titulo": "Férulas de descarga para el bruxismo en Leganés",
        "descripcion": "Férulas de descarga a medida en Leganés para el bruxismo. Protegen tus dientes si aprietas o rechinas y alivian la tensión de la mandíbula.",
        "resumen": "Protegen tus dientes si aprietas o rechinas.",
        "intro": "El bruxismo es el hábito de apretar o rechinar los dientes, muchas veces de noche y sin darse cuenta. Una férula de descarga hecha a medida protege tus dientes y alivia la tensión.",
        "secciones": [
            ("Señales de bruxismo", """
<ul>
  <li>Dientes desgastados, con bordes planos o pequeñas fracturas.</li>
  <li>Sensibilidad dental.</li>
  <li>Dolor o cansancio en la mandíbula al despertar.</li>
  <li>Dolor de cabeza, sobre todo por la mañana.</li>
  <li>Chasquidos al abrir o cerrar la boca.</li>
</ul>
"""),
            ("Por qué conviene tratarlo pronto", """
<p>El desgaste del esmalte no se recupera. Proteger los dientes cuanto antes evita fracturas y tratamientos más complejos en el futuro, y ayuda a aliviar las molestias de la mandíbula.</p>
"""),
            ("Cuidado de la férula", """
<p>Límpiala cada mañana con un cepillo y agua fría, guárdala seca en su estuche y tráela a tus revisiones para comprobar su ajuste y su desgaste.</p>
"""),
        ],
        "pasos": [
            ("Diagnóstico", "Revisamos el desgaste de tus dientes, la mordida y la articulación de la mandíbula."),
            ("Registros", "Tomamos las medidas de tu boca para fabricar la férula a medida."),
            ("Entrega y ajuste", "Probamos la férula y ajustamos la mordida para que sea cómoda."),
            ("Revisiones", "Comprobamos periódicamente el ajuste y el estado de la férula."),
        ],
        "faqs": [
            ("¿Sirven las férulas genéricas?", "Una férula hecha a medida se adapta exactamente a tu boca y a tu mordida, por lo que resulta más cómoda y protege mejor que una genérica."),
            ("¿La férula cura el bruxismo?", "La férula no elimina el hábito, pero protege los dientes del desgaste y reduce la tensión en la mandíbula. Si el estrés influye, también ayuda trabajar sobre él."),
            ("¿Cuánto dura una férula?", "Depende de la intensidad del bruxismo. En las revisiones comprobamos su desgaste y te decimos cuándo conviene renovarla."),
        ],
        "relacionados": ["odontologia-general", "estetica-dental"],
    },
    {
        "slug": "odontologia-general",
        "nombre": "Odontología general",
        "h1": "Odontología general en Leganés",
        "titulo": "Dentista en Leganés: revisiones, limpiezas y empastes",
        "descripcion": "Odontología general en Leganés para toda la familia: revisiones, limpiezas, empastes y endodoncias. Pide cita en el 91 680 67 24.",
        "resumen": "Revisiones, limpiezas, empastes y endodoncias.",
        "intro": "La base de una boca sana: revisiones periódicas, limpiezas profesionales y tratar los problemas a tiempo, antes de que vayan a más. Atendemos a toda la familia.",
        "secciones": [
            ("Qué incluye", """
<ul>
  <li><strong>Revisiones</strong>: exploramos dientes y encías para detectar cualquier problema a tiempo.</li>
  <li><strong>Limpieza profesional</strong>: eliminamos el sarro y las manchas que el cepillado no puede quitar.</li>
  <li><strong>Empastes</strong>: tratamos las caries con materiales del color del diente.</li>
  <li><strong>Endodoncias</strong>: cuando la caries o un golpe afectan al nervio, la endodoncia permite conservar el diente.</li>
</ul>
"""),
            ("Prevenir es lo más sencillo", """
<p>Muchos problemas dentales no duelen al principio. Una revisión periódica permite tratarlos cuando todavía son pequeños, con tratamientos más sencillos.</p>
"""),
        ],
        "pasos": [],
        "faqs": [
            ("¿Cada cuánto debo hacerme una revisión?", "Como norma general, al menos una vez al año. Según tu caso podemos recomendarte revisiones más frecuentes."),
            ("¿La limpieza dental daña el esmalte?", "No. La limpieza profesional elimina el sarro y la placa sin dañar el esmalte, y ayuda a mantener las encías sanas."),
            ("¿Duele una endodoncia?", "Se hace con anestesia local, así que durante el tratamiento no se siente dolor. Después puede haber alguna molestia leve durante unos días."),
        ],
        "relacionados": ["ferulas-bruxismo", "blanqueamiento-dental"],
    },
]
