# Cálculos del resumen de NetSciX 2027

Esta carpeta es `camino` 0.20.0, la versión del 7 de octubre. Es la que da los números del resumen: las razones de costo, el nulo de 500 rutas, la red nacional y las dos redes de la Fig. 1.

**No la mezcles con tu carpeta `leimebamba`.** Tu versión actual (0.22) está configurada para otro estudio. Analiza un solo tramo (Chillo – Chachapoyas), acepta unidades desde 100 m y usa una pendiente máxima de 35°. Por eso, ahí `nulos` da otros números.

La carpeta `datos/` ya trae todo lo que hace falta: los dos DEM, el KMZ del registro, el agua de OSM y el recorte del camino. No hay que bajar nada ni usar la llave de OpenTopography.

## Antes de empezar

1. Descomprime el zip en `C:\Users\jvera\Documents`. Te queda la carpeta `C:\Users\jvera\Documents\netscix_calculos`.
2. Abre Anaconda Prompt y escribe:

```
conda activate camino
cd C:\Users\jvera\Documents\netscix_calculos
```

## 1. Las derivadas y las razones de costo (unos 3 minutos)

```
python -m camino preparar
python -m camino superficies
python -m camino grafo
python -m camino revisar
```

`revisar` imprime la razón de costo de cada tramo: de 1.03 a 1.22 en cinco tramos, y 1.39 en Pauja – Santa Cruz. El resultado queda en `resultados/revision_grafo.json`.

## 2. El nulo: 500 rutas de control por tramo (de 30 a 60 minutos)

```
python nulo_en_dos_partes.py
```

Corre dos procesos en paralelo con las mismas semillas que usé, así que el resultado sale idéntico:

- p = 0.002 en cinco tramos
- p = 0.73 en Pauja – Santa Cruz

Para probar primero que todo funciona, corre `python nulo_en_dos_partes.py --m 5`, que tarda un par de minutos.

También sirve `python -m camino nulos`. Corre en un solo proceso, con otros sorteos, y tarda el doble. La conclusión es la misma.

El resultado queda en `derivados/nulos.npz` y `resultados/nulo_de_costo.csv`.

## 3. La red nacional (unos 5 minutos)

```
python -m camino red
```

Si te dice que falta networkx, instálalo con:

```
conda install -c conda-forge networkx
```

## 4. Las dos redes de la Fig. 1 (unos 3 minutos)

Necesitas el repositorio `canete-corridor-model`. Si no lo tienes, clónalo o bájalo como zip desde GitHub:

```
git clone https://github.com/javier-vz/canete-corridor-model C:\Users\jvera\Documents\canete-corridor-model
```

Después corre:

```
python canete_paths.py C:\Users\jvera\Documents\canete-corridor-model
python red_regional.py
```

- `canete_paths.py` rehace la corrida canónica de corredores (eps 0.15, kappa 0.03, semilla 42) y guarda las 344 rutas en `canete_paths.pkl`.
- `red_regional.py` mide la red de Chachapoyas y la de Cañete con las mismas funciones del paso `red`. Deja el resultado en `resultados/red_regional.json`.

## Para comparar

En `resultados_de_referencia/` está lo que salió cuando lo corrí:

| Archivo | Paso |
| --- | --- |
| `revision_grafo.json` | 1 |
| `nulo_de_costo.csv` | 2 |
| `red_nacional.txt` | 3 |
| `red_regional.json` | 4 |

## Lo que todavía no se puede correr

La optimización inversa (`barrido` y `validar`) necesita el catálogo de espacios ceremoniales filtrado por Dina. Va en `datos/`, con un nombre que empiece por `sitios`.

Hasta que esté el catálogo, no corras `python -m camino todo` en esta carpeta: intentaría también esos dos pasos.
