# align_local_pdb.py
import sys
import pymol
from pymol import cmd

pdb1_path = sys.argv[1]
pdb2_path = sys.argv[2]
output_path1 = sys.argv[3]
output_path2 = sys.argv[4]

pymol.finish_launching(['pymol', '-cq'])

# 加载两个结构
cmd.load(pdb1_path, 'mol1')
cmd.load(pdb2_path, 'mol2')

# 对齐 mol2 到 mol1
cmd.align('mol2', 'mol1')

cmd.save(output_path1, 'mol1')
cmd.save(output_path2, 'mol2')

cmd.quit()
