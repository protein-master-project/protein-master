import os
import subprocess
import tempfile

def align_with_pymol(pdb1_path, pdb2_path):
    # 1. 在临时目录中准备 PML 脚本和输出文件路径
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path   = os.path.join(tmpdir, "align.pml")
        out1_path     = os.path.join(tmpdir, "aligned1.pdb")
        out2_path     = os.path.join(tmpdir, "aligned2.pdb")

        # 2. 构造 PML 脚本内容
        pml = f"""
load {pdb1_path}, mol1
load {pdb2_path}, mol2
align mol2, mol1
save {out1_path}, mol1
save {out2_path}, mol2
quit
"""
        # 3. 写入脚本文件
        with open(script_path, 'w') as f:
            f.write(pml)

        # 4. 调用 PyMOL（-q: quiet, -c: no GUI, script_path: 自动执行脚本）
        subprocess.run(
            ['pymol', '-qc', script_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )

        # 5. 读取对齐后的 PDB 文本
        with open(out1_path, 'r') as f:
            aligned1 = f.read()
        with open(out2_path, 'r') as f:
            aligned2 = f.read()

    return aligned1, aligned2
