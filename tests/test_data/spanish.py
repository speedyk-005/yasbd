ISO_CODE = "es"
TEST_DATA = [
    # Basic punctuation
    "Hola mundo.| ¿Cómo estás?| Bien, gracias.",
    "¿Cuál es tu nombre?| Me llamo Carlos.",
    "¿Viste la película anoche?.| Sí, fue increíble.| ¡Me encantó!| La actuación fue excelente.",

    # Abbreviations
    "El Sr. García llegó ayer.| La Sra. López también.",
    "La Profe. María dio una conferencia.",
    "El Lcdo. Pérez y el Mag. Torres son amigos.",
    "D. José y Dña. María son los dueños.",
    "El Cmdte. Rodríguez saludó al Cnel. Díaz.",
    "Véase la pág. 55 del libro.",
    "Vea el cap. 3 en el t. II de la obra.",
    "El art. 4 y el nro. 8 son clave.",
    "Llama al dir. general al tel. 555-1234.",
    "Llama al tel. 555-0199.| Envía el fax. 02-555 mañana.",
    "Compré pan, leche, etc. para la cena.",
    "Lea p. ej. el capítulo 5.",
    "Ayer le dije que no.| 5 personas llegaron después.",
    "Lo dejo entre nos.| 3 personas lo saben.",
    "El tren para.| 5 pasajeros bajan.",
    "La reunión es el lun. 15 de enero.",
    "Nació el 5 de abr. de 1990.",
    "El presidente de los EE.UU. visitó Europa.",
    "Las FF.AA. emitieron un comunicado oficial.",
    "El departamento de RR.HH. aprobó las vacaciones.",
    "La reunión es el lun. 15 de enero.",

    # structural headings
    "Capítulo 1. El Comienzo.| Estaba oscuro afuera. | Nada se movía.",
    "Parte II. Introducción.| El sistema comienza aquí. | La inicialización sigue.",
    "El informe fue completado.| Capítulo 3. Análisis de resultados.",

    # Addresses & Locations
    "Yo vi un ave.| ¿Lo has visto también?",
    "Vive en la Av. Siempre Viva.",
    "Viven en la C. Mayor, 12.",
    "El accidente fue en la Cra. 50 con Cll. 100.",
    "Dobla en la Transv. 3 y sigue por la Diag. 5.",
    "La casa está en la Urb. Las Rosas, Mz. A, Lt. 15 del Asent. Humano.",

    # Common Starters after abbreviations
    "Llegó el Sr. Por suerte trajo el paquete.",
    "Fui a la Cra. Para ver el desfile.",
    "Llegó el Sr. García.| Como no estaba, se fue.",

    # Parentheses and quotes
    "El problema —¿y quién lo iba a decir?— fue resuelto rápido.",
    "La decisión —¡increíblemente difícil!— cambió todo.",
    "Él dijo (No estoy listo.) durante la reunión.",
    "Él preguntó: ¿Estás listo?| Respondí que sí.",
    'Ella dijo: "No estoy segura."| Luego se fue.',

    # Pronoun heuristic (Ud./Vd.)
    "Me dirijo a Ud. Marco, para saludarlo.",
    "Me dirijo a Ud.| Mañana le enviaré el paquete.",
    "Se lo di a Uds.| Ellos lo confirmaron.",
    "Pregunté por Vds.| Lamentablemente no estaban.",
    "Me dirijo a Ud.| ¿Cuándo me enviará el paquete?",
    "Espero que Ud. comprenda el problema.",

    # Ellipsis
    "El proyecto estaba casi terminado... pero encontramos un problema.",
]
