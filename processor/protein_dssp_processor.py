import os
import subprocess
import tempfile


def _parse_dssp_file(dssp_path: str) -> dict[str, list[int]]:
    """Return {'helix': [...], 'strand': [...], 'turn': [...]} from a .dssp file."""
    sec = {"helix": [], "strand": [], "turn": []}
    with open(dssp_path) as fh:
        start = False
        for ln in fh:
            if ln.startswith("  #  RESIDUE AA STRUCTURE"):
                start = True
                continue
            if not start or len(ln) < 17:
                continue
            try:
                res_no = int(ln[5:10])
            except ValueError:
                continue
            code = ln[16]
            if code == "H":
                sec["helix"].append(res_no)
            elif code == "E":
                sec["strand"].append(res_no)
            elif code == "T":
                sec["turn"].append(res_no)
    return sec


def _dssp_for_pdb_text(pdb_text: str) -> dict[str, list[int]]:
    """给一段 PDB 文本跑 mkdssp，返回 helix/strand/turn 列表"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as tmp_pdb:
        tmp_pdb.write(pdb_text.encode())
        pdb_path = tmp_pdb.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dssp") as tmp_dssp:
        dssp_path = tmp_dssp.name

    try:
        # for win
        # subprocess.run(['mkdssp', '-i', pdb_path, '-o', dssp_path])

        # for macbook
        subprocess.run(["mkdssp", pdb_path, dssp_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return _parse_dssp_file(dssp_path)
    finally:
        os.unlink(pdb_path)
        os.unlink(dssp_path)
