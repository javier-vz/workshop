#!/usr/bin/env python3
"""Execute all released notebooks in demo mode; verify reproducibility and no sensitive CSV leakage.
Usage: python scripts/smoke_test.py [--real-private-dir PATH]
For --real-private-dir, only use approved local storage; files never uploaded.
"""
from pathlib import Path
import os, json, argparse, sys, tempfile, shutil
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nbformat

REPO=Path(__file__).resolve().parents[1]
NB=REPO/'notebooks'

def execute(name, mode='demo', priv=None):
    oldmode=os.environ.get('NETSCIX_DATA_MODE')
    olddir=os.environ.get('NETSCIX_PRIVATE_DIR')
    oldfile=os.environ.get('NETSCIX_PRIVATE_DATA')
    os.environ['NETSCIX_DATA_MODE']=mode
    if priv:
        os.environ['NETSCIX_PRIVATE_DIR']=str(priv)
        os.environ['NETSCIX_PRIVATE_DATA']=str(priv/'canete_250m_PRIVATE.csv')
    ns={'__name__':'__main__'}
    plt.show=lambda *a,**kw: plt.close('all')
    try:
        nb=nbformat.read(NB/name,as_version=4)
        assert len(nb.cells)>8
        for i,cell in enumerate(nb.cells):
            if cell.cell_type=='code':
                try: exec(compile(cell.source,f'{name} cell {i}','exec'),ns)
                except Exception as exc:
                    raise RuntimeError(f'{name} code cell {i} failed: {exc}') from exc
        return ns
    finally:
        for key,old in [('NETSCIX_DATA_MODE',oldmode),('NETSCIX_PRIVATE_DIR',olddir),('NETSCIX_PRIVATE_DATA',oldfile)]:
            if old is None: os.environ.pop(key,None)
            else: os.environ[key]=old

def check_public_tree():
    forbidden=[]
    for f in REPO.rglob('*'):
        if not f.is_file(): continue
        if f.name.endswith('_PRIVATE.csv') or '02_PRIVADO_NO_SUBIR' in str(f) or f.name.lower().startswith('canete_250m'):
            forbidden.append(str(f.relative_to(REPO)))
    assert not forbidden, 'Sensitive files in public repo: '+', '.join(forbidden)
    for f in NB.glob('*.ipynb'):
        n=nbformat.read(f,as_version=4)
        assert all(not c.get('outputs') for c in n.cells if c.cell_type=='code'), f'{f.name} has saved outputs'
        assert '"demo"' in n.cells[2].source and 'NETSCIX_DATA_MODE' in n.cells[2].source

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--real-private-dir',type=Path)
    args=parser.parse_args()
    check_public_tree()
    mode='real' if args.real_private_dir else 'demo'
    priv=args.real_private_dir
    if priv and not priv.is_dir(): raise FileNotFoundError(priv)
    s1=execute('01_spatial_prediction.ipynb',mode,priv)
    s2=execute('02_network_construction.ipynb',mode,priv)
    s3=execute('03_network_analysis.ipynb',mode,priv)
    assert len(s1['df'])==len(s2['df'])
    assert s1['df'].cell_id.tolist()==s2['df'].cell_id.tolist()
    assert np.allclose(s1['out_of_fold'],s2['df']['oof_rank_score'],atol=1e-10), 'NB1 vs NB2 OOF scores differ'
    assert s2['route_df'].shape[0]==2*len(s2['pairs'])
    assert s2['nodes'].shape[0]>=4
    assert len(s3['nodes'])==len(s2['nodes'])
    from pandas.testing import assert_frame_equal
    assert_frame_equal(s3['edges'].sort_values(['scenario','source','target']).reset_index(drop=True)[['scenario','source','target','physical_length_m','accumulated_model_cost']], s2['route_df'].sort_values(['scenario','source','target']).reset_index(drop=True)[['scenario','source','target','physical_length_m','accumulated_model_cost']],check_exact=False,atol=1e-5,rtol=1e-7)
    assert s3['summary_df'].n_nodes.nunique()==1 and s3['summary_df'].n_edges.nunique()==1
    if mode=='demo':
        sam=REPO/'data'/'sample'
        for name,table in [('nb2_nodes_SYNTHETIC.csv',s2['nodes']),('nb2_edges_SYNTHETIC.csv',s2['route_df']),('nb2_route_cells_SYNTHETIC.csv',s2['route_cells'])]:
            expected=pd.read_csv(sam/name)
            assert_frame_equal(expected,table,check_exact=False,atol=1e-5,rtol=1e-6)
    print(f'PASS: {mode} | cells={len(s1["df"])} | candidate nodes={len(s2["nodes"])} | candidate pairs={len(s2["pairs"])} | three notebooks OK')

if __name__=='__main__': main()
