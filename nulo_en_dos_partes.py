"""El nulo de costo (paso 7 de camino) repartido en dos procesos en paralelo.

Es el mismo `pipeline.correr_nulos`, sin tocarlo. Solo cambian dos cosas:
cada proceso corre tres de los seis tramos, y cada uno usa su propia semilla,
derivada de la del config con SeedSequence([semilla, ord(parte)]). Asi se
corrio el 22 de octubre de 2026, y con los mismos datos sale lo mismo.

`python -m camino nulos` hace lo mismo en un solo proceso, con otros sorteos:
tarda el doble y llega a la misma conclusion.

Uso, desde esta carpeta y con el entorno activado:

    python nulo_en_dos_partes.py           # las 500 rutas de control por tramo
    python nulo_en_dos_partes.py --m 5     # prueba rapida, unos minutos

Deja derivados/nulos.npz (lo mismo que deja el paso 7), la tabla en pantalla
y en resultados/nulo_de_costo.csv, y un registro por proceso en
log_nulo_A.txt y log_nulo_B.txt.
"""
import argparse
import csv
import dataclasses
import os
import pathlib
import subprocess
import sys
import time

import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parent
PARTES = {
    "A": ["Chachapoyas - Jumbilla", "Pauja - Santa Cruz", "Chillo - Chachapoyas"],
    "B": ["Leymebamba - Chilchos - Mendoza", "La Jalca - Mendoza", "Chachapoyas - Cochamal"],
}


def una_parte(parte: str, m: int | None) -> None:
    """Lo que corre cada proceso hijo."""
    sys.path.insert(0, str(RAIZ))
    from camino import config, pipeline

    cfg = config.Config.cargar(RAIZ / "config.yaml")
    hija = np.random.SeedSequence([cfg.semilla, ord(parte)]).generate_state(1)[0]
    cambios = {"semilla": int(hija)}
    if m:
        cambios["m_nulos"] = m
    cfg = dataclasses.replace(cfg, **cambios)
    print(f"parte {parte}: semilla {cfg.semilla}, {cfg.m_nulos} rutas por tramo", flush=True)

    nombres = set(PARTES[parte])
    original = pipeline._carga_unidades

    def solo_estas(c):
        g, t, uds = original(c)
        uds = [(n, geom) for n, geom in uds if n in nombres]
        print(f"  parte {parte}: {[n for n, _ in uds]}", flush=True)
        return g, t, uds

    pipeline._carga_unidades = solo_estas

    # la salida de cada parte va a su propio archivo, no a nulos.npz
    guarda = np.savez_compressed

    def guarda_aparte(ruta, *a, **kw):
        ruta = pathlib.Path(ruta)
        if ruta.name == "nulos.npz":
            ruta = ruta.with_name(f"nulos_parte_{parte}.npz")
        return guarda(ruta, *a, **kw)

    np.savez_compressed = guarda_aparte
    pipeline.correr_nulos(cfg)
    print(f"LISTO {parte}", flush=True)


def juntar() -> None:
    """Une las dos partes en derivados/nulos.npz e imprime la tabla."""
    sys.path.insert(0, str(RAIZ))
    from camino import pipeline

    der = RAIZ / "derivados"
    todo = {}
    for parte in PARTES:
        z = np.load(der / f"nulos_parte_{parte}.npz")
        for k in z.files:
            todo[k] = z[k]
    np.savez_compressed(der / "nulos.npz", **todo)

    nombres = [k[len("razon__"):] for k in todo if k.startswith("razon__")]
    obs = {n: float(todo["razonobs__" + n][0]) for n in nombres}
    nul = {n: todo["razon__" + n] for n in nombres}
    tabla = pipeline._tabla_nulo_de_costo(obs, nul)

    with open(RAIZ / "resultados" / "nulo_de_costo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tramo", "razon_observada", "nulo_p25", "nulo_mediana", "nulo_p75", "p",
                    "rutas_validas"])
        for n, d in tabla.items():
            w.writerow([n, round(d["r_observada"], 3), round(d["nulo_p25"], 2),
                        round(d["nulo_mediana"], 2), round(d["nulo_p75"], 2), round(d["p"], 4),
                        d["m_validos"]])
    print(f"\n  guardado: derivados/nulos.npz y resultados/nulo_de_costo.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--m", type=int, default=None,
                    help="rutas de control por tramo (por omision, las del config: 500)")
    ap.add_argument("--parte", choices=list(PARTES), help=argparse.SUPPRESS)
    args = ap.parse_args()

    if args.parte:                       # proceso hijo
        una_parte(args.parte, args.m)
        sys.exit(0)

    if not (RAIZ / "derivados" / "grafo.npz").exists():
        sys.exit("Falta derivados/grafo.npz. Corre antes: preparar, superficies, grafo y revisar "
                 "(ver LEEME.md).")

    t0 = time.time()
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8")
    procesos = []
    for parte in PARTES:
        log = open(RAIZ / f"log_nulo_{parte}.txt", "w", encoding="utf-8")
        extra = ["--m", str(args.m)] if args.m else []
        procesos.append((parte, log, subprocess.Popen(
            [sys.executable, str(pathlib.Path(__file__).resolve()), "--parte", parte, *extra],
            cwd=RAIZ, stdout=log, stderr=subprocess.STDOUT, env=entorno)))
        print(f"  parte {parte} lanzada: {', '.join(PARTES[parte])}  (registro en log_nulo_{parte}.txt)")

    fallo = False
    for parte, log, p in procesos:
        p.wait()
        log.close()
        if p.returncode != 0:
            fallo = True
            print(f"  la parte {parte} fallo: mira log_nulo_{parte}.txt")
    if fallo:
        sys.exit(1)

    print(f"  las dos partes terminaron en {(time.time() - t0) / 60:.0f} min")
    juntar()
