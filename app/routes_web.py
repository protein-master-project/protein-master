from app import app
from flask import Flask, jsonify, render_template, request, send_file
import subprocess
# from Bio.PDB import PDBParser
# from Bio.PDB.DSSP import DSSP
import json
import os

@app.route('/molstar')
def index():
    return render_template('molstar.html')


@app.route('/matrix')
def matrix():
    return render_template('matrix.html')

@app.route('/chatapp')
def chatapp():
    return render_template('chat.html')

# def align_and_view():
#     pdb1 = '1avr'
#     pdb2 = '4pti'
#
#     pdb1_path = f'static/pdb/{pdb1}.pdb'
#     pdb2_path = f'static/pdb/{pdb2}.pdb'
#     output_path1 = f'static/aligned1.pdb'
#     output_path2 = f'static/aligned2.pdb'
#
#     #os.makedirs('static', exist_ok=True)
#
#
#     subprocess.run(['python3', 'app/align_local_pdb.py', pdb1_path, pdb2_path, output_path1, output_path2])
#
#     # 渲染 HTML 页面并传入对齐结果的路径
#     #aligned_url = f'/static/aligned/{pdb1}_{pdb2}_aligned.pdb'
#     # return render_template('align.html')
#
@app.route('/contrast')
def contrast():
    return render_template('contrast.html')
#
# @app.route('/process_pdb')
# def process_pdb():
#     pdb_path = 'static/pdb/1avr.pdb'
#     parser = PDBParser()
#     structure = parser.get_structure("X", pdb_path)
#     model = structure[0]
#     dssp = DSSP(model, pdb_path)
#
#     result = []
#     for key in dssp.keys():
#         chain_id, res_id = key
#         residue_info = {
#             'chain': chain_id,
#             'residue_id': res_id[1],
#             'structure': dssp[key][2]  # 'H', 'E', 'T', etc.
#         }
#         result.append(residue_info)
#
#     return jsonify(result)
#
#
# def parse_dssp(dssp_file):
#     """解析 DSSP 文件，提取二级结构"""
#     secondary_structures = {"helix": [], "strand": [], "turn": []}
#     with open(dssp_file, 'r') as f:
#         lines = f.readlines()
#         start_parsing = False
#         for line in lines:
#             if line.startswith("  #  RESIDUE AA STRUCTURE"):
#                 start_parsing = True
#                 continue
#             if not start_parsing:
#                 continue
#             if len(line) < 16:
#                 continue
#             # 提取氨基酸编号和二级结构
#             res_num = line[5:10].strip()  # 残基编号
#             ss = line[16]  # 二级结构
#             if not res_num:
#                 continue
#             res_num = int(res_num)
#             # 映射二级结构
#             if ss == 'H':
#                 secondary_structures["helix"].append(res_num)
#             elif ss == 'E':
#                 secondary_structures["strand"].append(res_num)
#             elif ss == 'T':
#                 secondary_structures["turn"].append(res_num)
#     return secondary_structures
#
# def generate_structure_json(pdb_name):
#     """生成 PDB 文件的二级结构 JSON 文件"""
#     pdb_path = f'static/{pdb_name}.pdb'
#     dssp_path = f'static/{pdb_name}.dssp'
#     json_dir = 'static/json'
#     json_path = f'{json_dir}/{pdb_name}_structure.json'
#
#     # 确保 json 文件夹存在
#     if not os.path.exists(json_dir):
#         os.makedirs(json_dir)
#
#     # 如果 JSON 文件已存在，直接返回
#     if os.path.exists(json_path):
#         return
#
#     # 运行 DSSP
#     subprocess.run(['mkdssp', '-i', pdb_path, '-o', dssp_path])
#
#     # 解析 DSSP 文件
#     structures = parse_dssp(dssp_path)
#
#     # 保存为 JSON 文件
#     with open(json_path, 'w') as f:
#         json.dump(structures, f)
#
# @app.route('/barcontrast')
# def show_pdb():
#
#     generate_structure_json('aligned1')
#     generate_structure_json('aligned2')
#     return render_template('barcontrast.html')
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)