# LFP_PR2_201901657
LFP. Proyecto 2. Primer Semestre 2022

# TABLA DE TOKENS

| Nombre | Descripción del patrón | Expresión regular | Ejemplos |
| -------------------------- | ----------------------------------------------------- | ----------------- | ----------------------- |
| Cadena | Una cadena de caracteres encerrada en comillas dobles  | \\"[^.\\"]\*\\" | "Real Madrid" "Barcelona" |
| Menor que | Signo menor que | '<' | < |
Año | Cuatro numero consecutivos | \d\d\d\d | 2022 1999
Guion | Signo guion | '-' | -
| Mayor que | Signo mayor que | '>' | >
| RESULTADO | reservada RESULTADO  | RESULTADO | RESULTADO
| VS | reservada VS | VS | VS
| TEMPORADA | reservada TEMPORADA | TEMPORADA | TEMPORADA
| JORNADA | reservada JORNADA | JORNADA | JORNADA
| GOLES | reservada GOLES | GOLES | GOLES 
| LOCAL | reservada LOCAL | LOCAL | LOCAL
| VISITANTE | reservada VISITANTE | VISITANTE | VISITANTE
| TOTAL | reservada TOTAL | TOTAL | TOTAL
| TABLA | reservada TABLA | TABLA | TABLA
| PARTIDOS | reservada PARTIDOS | PARTIDOS | PARTIDOS
| TOP | reservada TOP | TOP | TOP
| SUPERIOR | reservada SUPERIOR | SUPERIOR | SUPERIOR
| INFERIOR | reservada INFERIOR | INFERIOR | INFERIOR 
| ADIOS | reservada ADIOS | ADIOS | ADIOS

# GRAMÁTICA

| |  | |
| -------------------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| S | ::= | INICIO
| INICIO | ::= | RESULTADO
| | ::= | JORNADA
| | ::= | GOLES
| | ::= | TABLA
| | ::= | PARTIDOS
| | ::= | TOP
| | ::= | ADIOS
| RESULTADO | ::= | pr_resultado cadena pr_vs cadena pr_temporada menorque año guion año mayor que
| JORNADA | ::= | 
| GOLES | ::= | pr_goles CONDICION cadena pr_temporada menorque año guion año mayor que
| CONDICION | ::= | pr_local 
| | ::= | \| pr_visitante
| | ::= | \| pr_total
| TABLA | ::= |
| PARTIDOS | ::= |
| TOP | ::= |
| ADIOS | ::= | pr_adios

