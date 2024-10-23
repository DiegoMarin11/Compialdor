# COMPILADOR DE LENGUAJE NATURAL A SQL

## Resumen

- El objetivo principal de este proyecto es desarrollar un compilador sencillo que convierta frases en lenguaje natural en consultas SQL utilizando lso metodos básicos de SQL. Este proyecto busca automatizar y simplificar la generación de consultas SQL a partir de instrucciones simples, mejorando la accesibilidad a la programación de bases de datos.

## Motivación y Problema a Resolver

- **Descripción del problema:**
  El uso de SQL para acceder a bases de datos es una habilidad que no todos dominan, lo que limita su acceso a usuarios no técnicos. Este compilador pretende facilitar este acceso y podrai servir como una herramienta de aprendizaje.

- **Importancia:**
  Hacer mas accesible la creación de consultas SQL puede hacer que la gestión de bases de datos sea más facil para aquellos con poca o ninguna experiencia en programación.
- **Casos de uso:**
  Usuarios que necesitan generar consultas SQL de manera sencilla y rápida, como gerentes que necesitan reportes, analistas no técnicos, etc. Tambien una herramienta de aprendizaje

## Objetivos del Proyecto

- **Objetivo 1:**
  Desarrollar un compilador que transforme frases simples en consultas SQL.
- **Objetivo 2:**
  Implementar el autómata no determinista y el autómata determinista utilizando JFLAP. Convertir autómatas no deterministas a deterministas mediante una tabla de transición.
- **Objetivo 3:**
  Implementar el compilador en Python, con soporte para comandos básicos de SQL.
- **Objetivo 4**
  Mejorar el entendimiento de consultas SQL para personas no tecnicas.

## Revisión del Estado del Arte

- **Compiladores similares:**
  Con la inteligencia artificial han surgido varios proyectos o paginas que utilizan el mismo modelo para traducir de lengiaje natral a sql, como NL2SQL
- **Limitaciones de soluciones actuales:**
  Muy comunmente dependen de patrones predefinidos
- **Justificación del nuevo compilador:**
  Este proyecto ofrece una solución minimalista y específica, enfocada en las necesidades básicas de usuarios no técnicos.

## Arquitectura y Diseño del Compilador

- **Diagrama de bloques:**
  <center><img width="250px" src="./ResourcesMD/bloques.jpg"></center>
- **Explicación del flujo de datos:**
  La entrada en lenguaje natural se analiza para identificar palabras clave, operadores e identificar que palabras se estan refiriendo al nomnre de una columna. Luego son transformados en una consulta SQL.
- **Decisiones de diseño:**
  Se implementaran los autómatas en JFLAP y se realizara la conversión a código Python para la compilación final.

## Análisis Léxico

- **Análisis léxico:**
  - La entrada en lenguaje natural se tokeniza para identificar palabras clave como “seleccionar”, “de” y operadores condicionales como “dónde”.
  - Se identificaran las palabras que se refieren a columnas
  - El abecedario va consistir en letras de a-z, numeros de 0-9, el simbolo de igual "=" y los espacios entre palabras se representaran con un guion bajo "\_"
- **Ejemplos:**

  - "dame_nombres_de_empleados_de_Mexicali"
  - "borrar_luis_de_empleados"
  - "dame_todos_los_usuarios_de_Cetys"

- Tokens: SELECT, nombre, FROM, empleados, WHERE, Mexicali, DELETE, luis, FROM, empleados, SELECT, \*, FROM, usuarios, cetys

## Diagramas:

**Automata finito no deterministico**
<img src="./ResourcesMD/automatanodefinido.jpg">

**Automata finito deterministico**
<img src="./ResourcesMD/automatadeterministico.png">



**Palabras clave**

- **"Dame"**: "SELECT",
- **"Todos"**: "\*",
- **"De"**: "FROM",
- **"Donde"**: "WHERE",
- **"Insertar"**: "INSERT",
- **"Actualizar"**: "UPDATE",
- **"Borrar"**:"DELETE"
- **"En"** : "IN",
- **"Valores":**"VALUES",
- **"A":**"INTO",
- **"El":**"SET",
- **"Los":**"SET".

## Análisis Sintáctico

- **Análisis sintáctico:**

Primera versión de la gramática:

InsertQuery -> INSERT INTO Table VALUES ValuesGroup \
ValuesGroup -> "(" Values ")" | "(" Values ")" "," ValuesGroup \
Values -> Value | Value "," Values \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER

DeleteQuery -> DELETE FROM Table WhereClause \
WhereClause -> WHERE Condition | Epsilon \
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \ 
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER 

SelectQuery -> SELECT Columns FROM Table WhereClause \
Columns -> * | ColumnList \
ColumnList -> Column | Column "," ColumnList \
WhereClause -> WHERE Condition | Epsilon \ 
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER 

UpdateQuery -> UPDATE Table SET Assignments WhereClause \
Assignments -> Assignment | Assignment "," Assignments \
Assignment -> Column "=" Value \
WhereClause -> WHERE Condition | Epsilon \
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER


**Posibles recursiones izquierdas posibles (Nueva propuesta):**

De acuerdo a la tabla de first and follow podemos separar ValuesGroup Y Values

INSERT: \
InsertQuery -> INSERT INTO Table Values ValesGroup \
ValuesGroup -> “(“ Values ”)”  ValuesGroupPrime \
ValuesGroupPrime -> “,” ValuesGroup | Epsilon \
Values -> Value ValuePrime \
ValuePrime -> “,” Value | Epsilon \
Table -> IDENTIFIER \
VALUE -> IDENTIFIER | NUMBER

DELETE no necesita cambios.

DeleteQuery -> DELETE FROM Table WhereClause \
WhereClause -> WHERE Condition | Epsilon \
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER

SELECT:
 
SelectQuery -> SELECT Columns FROM Table WhereClause \
Columns -> * | ColumnList \
ColumnList -> Column ColumnListPrime \ 
ColumnListPrime - > "," ColumnList | Epsilon \
WhereClause -> WHERE Condition | Epsilon \
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER

UPDATE: 

UpdateQuery -> UPDATE Table SET Assignments WhereClause \
Assignments -> Assignment AssignmentPrime \
AssignmentsPrime -> "," Assignments | Epsilon \
Assignment -> Column "=" Value \
WhereClause -> WHERE Condition | Epsilon \
Condition -> Column Operator Value \
Operator -> "=" | ">" | "<" \
Column -> IDENTIFIER \
Table -> IDENTIFIER \
Value -> IDENTIFIER | NUMBER


- **Ejemplos:**

## Análisis Semántico

- **Análisis sintáctico:**

- **Ejemplos:**

## Pruebas y Validación

- **Metodología de pruebas:**
- **Resultados obtenidos:**
- **Casos de prueba específicos:**

## Herramientas y Entorno de Desarrollo

- **Lenguajes de programación utilizados:**
- **Herramientas de desarrollo:**
- **Entorno de pruebas y simulación:**

## Demostración

- **Ejemplo de código fuente:**
- **Proceso de compilación:**
- **Ejecución del código compilado:**

## Desafíos y Soluciones

- **Problemas técnicos o de diseño:**
- **Estrategias adoptadas para superar desafíos:**
- **Lecciones aprendidas:**

## Conclusiones y Trabajo Futuro

- **Resumen de objetivos cumplidos:**
- **Evaluación del desempeño:**
- **Propuestas para mejoras futuras:**

## Preguntas y Discusión

- Espacio para responder preguntas y discusión sobre el proyecto.

## Referencias

- **Fuentes citadas:** Lista de libros, artículos, papers, y otras fuentes relevantes.
