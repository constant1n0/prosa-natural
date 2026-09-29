He tomado esa carpeta como raíz del proyecto: `claims-aprobados.md` fija las tres alegaciones ya autorizadas, así que las he dejado literales, carácter a carácter, y he editado solo el resto de la prosa de `ficha.md`.

**Qué se ha cambiado:**

- **Título** (P20, Title Case): «Descubre El Sérum Vital C De NaturPiel» → «Descubre el Sérum Vital C de NaturPiel». Solo se baja la mayúscula de las palabras funcionales; «Sérum Vital C» y «NaturPiel» conservan su mayúscula por ser nombre de producto y marca.
- **Frase de apertura**: se corta «Profundicemos en lo que hace especial a…» (P04, preámbulo escenificado, está en la propia lista de fórmulas del patrón) y el contraste «no se trata de un sérum más, se trata de…» (P01): la mitad negativa no corregía ninguna creencia real del lector, así que se deja solo la afirmación. «que se erige como» se funde en «es» (P18: «se erige como» es señal fuerte por sí sola). El código de referencia y el precio se mantienen intactos, solo cambian de sitio dentro de la misma frase.
- **Párrafo de beneficios**: sin tocar. Las tres frases son justo las alegaciones aprobadas (ilumina en 7 días, 15 % de vitamina C estabilizada, dermatológicamente testado) y quedan literales; la coma final sobre la textura («ligera, fresca y de rápida absorción») describe tres propiedades reales del producto, no una tríada retórica, así que también se deja igual.
- **Cierre**: se corta «El Sérum Vital C llega para quedarse en la rutina de quienes buscan un extra de luminosidad sin renunciar a la sencillez». No añadía ningún dato nuevo (repetía la luminosidad ya alegada) y es un cierre publicitario que valdría igual para cualquier otra marca (P43/P26). Se conserva la instrucción de uso, que sí es información real.

**Qué se ha señalado sin tocar:** las tres alegaciones aprobadas, tal cual están en `claims-aprobados.md`.

He verificado con `scan_tells.py --original` que ningún dato (código, precio, porcentaje, duración, claim) falta o cambia entre el original y esta versión; la única diferencia que marca el escáner es la preposición «De» del título, que deja de tener mayúscula al corregir el Title Case — no es un nombre propio perdido, es justo el efecto esperado de ese arreglo.

Versión final:

---

## Descubre el Sérum Vital C de NaturPiel

El Sérum Vital C (REF-3305, 32,00 €) es un ritual diario y el aliado perfecto de tu piel.

Ilumina la piel visiblemente en 7 días. Contiene un 15 % de vitamina C estabilizada y es dermatológicamente testado, con una textura ligera, fresca y de rápida absorción.

Aplica dos gotas por la mañana antes de tu crema habitual.
