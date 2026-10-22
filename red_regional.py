"""Las dos redes de la Fig. 1 como grafos espaciales, medidas igual.

Chachapoyas: el registro del Qhapaq Nan (solo lo observado) dentro de la caja
del estudio, la de config.yaml. Canete: la red de corredores del modelo, o sea
las rutas de la Fig. 1A (las arma canete_paths.py).

Las dos redes se arman con `camino.red.construir` (nodos = cruces y cabos,
aristas = tramos entre ellos) y se miden con las mismas funciones que usa el
paso `python -m camino red`.

Uso, desde esta carpeta y con el entorno activado:

    python red_regional.py [canete_paths.pkl]

Deja la tabla en pantalla y en resultados/red_regional.json. Tarda un minuto.
"""
import json
import pathlib
import pickle
import sys
import warnings

import networkx as nx
import numpy as np
import yaml
from pyproj import Transformer
from shapely.geometry import LineString, box

warnings.filterwarnings("ignore")
RAIZ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
from camino import config, red, registro, ruta  # noqa: E402

PKL = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "canete_paths.pkl"


def puentes(G):
    """Fraccion de km en puentes: tramos cuya perdida parte su componente.

    En un MultiGraph una arista doble nunca es puente, asi que se cuenta sobre
    el grafo simple y solo valen las aristas de multiplicidad 1.
    """
    S = nx.Graph()
    for u, v, d in G.edges(data=True):
        if S.has_edge(u, v):
            S[u][v]["mult"] += 1
            S[u][v]["largo"] += d["largo"]
        else:
            S.add_edge(u, v, mult=1, largo=d["largo"])
    km_total = sum(d["largo"] for *_, d in G.edges(data=True)) / 1000
    km_p = sum(S[u][v]["largo"] for u, v in nx.bridges(S) if S[u][v]["mult"] == 1) / 1000
    return round(km_p / km_total, 3) if km_total else 0.0


def describe(G, nombre):
    m = red.medidas(G)
    mayor = G.subgraph(max(nx.connected_components(G), key=len))
    return {
        "red": nombre,
        "km": m["km_totales"],
        "nodos": m["nodos"],
        "aristas": m["aristas"],
        "componentes": m["componentes"],
        "km_en_la_mayor": m["km_en_la_mayor"],
        "grado_medio": m["grado_medio"],
        "fraccion_cabos": m["fraccion_grado_1"],
        "ciclos": m["ciclos"],
        "alfa": round(red.alfa(G), 3),
        "alfa_de_la_mayor": round(red.alfa(mayor), 3),
        "fraccion_km_en_puentes": puentes(G),
    }


cfg = config.Config.cargar(RAIZ / "config.yaml")
bb = yaml.safe_load(open(RAIZ / "config.yaml", encoding="utf-8"))["extension"]["bbox"]
salida = {}

# ---------------------------------------------------------------- Chachapoyas
fuente = ruta.busca_archivo(cfg)
print(f"registro: {fuente.name}")
qn = registro.lee(fuente, cfg.crs, solo_observadas=False)
qn, _ = registro.aplica_exclusiones(cfg, qn)

t = Transformer.from_crs("EPSG:4326", cfg.crs, always_xy=True)
x0, y0 = t.transform(bb["oeste"], bb["sur"])
x1, y1 = t.transform(bb["este"], bb["norte"])
caja = box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
obs = qn[(qn["categoria"] == "observado") & qn.intersects(caja)]
geoms = [g.intersection(caja) for g in obs.geometry]
geoms = [g for g in geoms if not g.is_empty]
print(f"Chachapoyas: {len(geoms)} rasgos observados en la caja del estudio, "
      f"{sum(g.length for g in geoms) / 1000:.0f} km")

filas = []
for tol in red.TOLERANCIAS:
    G, _ = red.construir(geoms, tol)
    f = describe(G, f"Chachapoyas, registro, huecos cerrados hasta {tol:.0f} m")
    f["tolerancia_m"] = tol
    filas.append(f)
salida["chachapoyas"] = filas

# ------------------------------------------------------------------- Canete
if not PKL.exists():
    print(f"\nNo esta {PKL.name}: corre antes canete_paths.py (ver LEEME.md). "
          "Sigo solo con Chachapoyas.")
else:
    d = pickle.load(open(PKL, "rb"))
    xs, ys = np.array(d["xs"]), np.array(d["ys"])

    def linea(p):
        return LineString([(xs[j], ys[i]) for i, j in p])

    todas = [linea(p) for p, w in d["paths"] if len(p) > 1]
    por_par = {}                      # la mejor ruta de cada par: la de mas peso
    for p, w in d["paths"]:
        clave = (tuple(p[0]), tuple(p[-1]))
        if clave not in por_par or w > por_par[clave][1]:
            por_par[clave] = (p, w)
    mejores = [linea(p) for p, w in por_par.values() if len(p) > 1]

    G, _ = red.construir(todas, 0.0)
    G1, _ = red.construir(mejores, 0.0)
    salida["canete"] = [describe(G, "Canete, corredores del modelo (4 rutas por par)"),
                        describe(G1, "Canete, corredores del modelo (la mejor ruta de cada par)")]
    print(f"Canete: {len(todas)} rutas entre {len(mejores)} pares de atractores")

(RAIZ / "resultados").mkdir(exist_ok=True)
json.dump(salida, open(RAIZ / "resultados" / "red_regional.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

print(f"\n{'red':58s} {'km':>6s} {'comp':>5s} {'ciclos':>6s} {'alfa':>6s} {'%puente':>8s}")
for f in salida["chachapoyas"] + salida.get("canete", []):
    print(f"{f['red']:58s} {f['km']:6.0f} {f['componentes']:5d} {f['ciclos']:6d} "
          f"{f['alfa']:6.3f} {100 * f['fraccion_km_en_puentes']:7.0f}%")
print("\n  comp     componentes desconectadas")
print("  ciclos   rutas alternativas independientes; 0 = entre dos puntos hay una sola ruta")
print("  alfa     indice alfa de Garrison y Marble (meshedness): 0 = arbol, 1 = malla")
print("  %puente  km en tramos cuya perdida parte la red: 100% = ninguna alternativa")
print("\n  guardado: resultados/red_regional.json")
