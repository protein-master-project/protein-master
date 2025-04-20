import os
import subprocess
import tempfile

from app import app
from flask import Flask, request, jsonify, Response
from connecter import ConnectorFactory
from processor.protein_align_processor import align_with_pymol
from processor.protein_dssp_processor import _dssp_for_pdb_text


@app.route('/test', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask backend!"}
    return jsonify(data)


@app.route('/search', methods=['GET'])
def search_proteins():
    keyword = request.args.get('keyword', '').strip()
    db = request.args.get('db', '').strip().lower()

    if not keyword or not db:
        return jsonify({"error": "Missing 'keyword' or 'db' parameter"}), 400

    connector = ConnectorFactory.get_connector(db)
    if not connector:
        return jsonify({"error": f"No connector found for db: {db}"}), 400

    try:
        results = connector.search_proteins_by_keyword(keyword)
    except Exception as e:
        return jsonify({"error": f"Search error: {str(e)}"}), 500

    return jsonify({"results": results})


@app.route('/download', methods=['GET'])
def download_pdb():
    pdb_id = request.args.get('pdb_id', '').strip()
    db = request.args.get('db', '').strip().lower()

    if not pdb_id or not db:
        return jsonify({"error": "Missing 'pdb_id' or 'db' parameter"}), 400

    connector = ConnectorFactory.get_connector(db)
    if not connector:
        return jsonify({"error": f"No connector found for db: {db}"}), 400

    try:
        pdb_content = connector.download_proteins_by_pdb_id(pdb_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

    return Response(
        pdb_content,
        mimetype='chemical/x-pdb',
        headers={"Content-Disposition": f"attachment; filename={pdb_id}.pdb"}
    )

@app.route('/raw', methods=['GET'])
def raw_pdb():
    pdb_id = request.args.get('pdb_id', '').strip()
    db = request.args.get('db', '').strip().lower()

    if not pdb_id or not db:
        return jsonify({"error": "Missing 'pdb_id' or 'db' parameter"}), 400

    connector = ConnectorFactory.get_connector(db)
    if not connector:
        return jsonify({"error": f"No connector found for db: {db}"}), 400

    try:
        pdb_content = connector.download_proteins_by_pdb_id(pdb_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

    return Response(
        pdb_content,
        mimetype='text/plain',
    )

@app.route('/align', methods=['GET'])
def align_proteins():
    # 1. Parse and validate input parameters
    pdb1_id = request.args.get('pdb1_id', '').strip()
    pdb2_id = request.args.get('pdb2_id', '').strip()
    db      = request.args.get('db', '').strip().lower()
    print(pdb1_id, pdb2_id, db)

    if not pdb1_id or not pdb2_id or not db:
        return jsonify({"error": "Missing 'pdb1_id', 'pdb2_id' or 'db' parameter"}), 400

    # 2. Initialize connector
    connector = ConnectorFactory.get_connector(db)
    if not connector:
        return jsonify({"error": f"No connector found for db: {db}"}), 400

    # 3. Download raw PDBs
    try:
        pdb1_content = connector.download_proteins_by_pdb_id(pdb1_id)
        pdb2_content = connector.download_proteins_by_pdb_id(pdb2_id)
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 404

    # 4. Write to temp files, call alignment, read results
    try:
        # with tempfile.TemporaryDirectory() as tmpdir:
        #     # Paths for input and output
        #     path1    = os.path.join(tmpdir, f"{pdb1_id}.pdb")
        #     path2    = os.path.join(tmpdir, f"{pdb2_id}.pdb")
        #     aligned1 = os.path.join(tmpdir, f"aligned_{pdb1_id}.pdb")
        #     aligned2 = os.path.join(tmpdir, f"aligned_{pdb2_id}.pdb")
        #
        #     # Write downloaded content
        #     for content, outpath in [(pdb1_content, path1), (pdb2_content, path2)]:
        #         data = content.encode() if isinstance(content, str) else content
        #         with open(outpath, 'wb') as fh:
        #             fh.write(data)
        #
        #     # Locate and invoke your alignment script
        #     script = os.path.join(os.path.dirname(__file__), 'align_local_pdb.py')
        #     # script = 'app/align_local_pdb.py'
        #     subprocess.run(
        #         ['python3', script, path1, path2, aligned1, aligned2],
        #         check=True
        #     )
        #     # subprocess.run(['python3', 'app/align_local_pdb.py', path1, path2, aligned1, aligned2])
        #
        #     # Read aligned results
        #     with open(aligned1, 'r') as fh:
        #         aligned1_text = fh.read()
        #     with open(aligned2, 'r') as fh:
        #         aligned2_text = fh.read()

        # 4. Write to tmp and call in-process function
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = os.path.join(tmpdir, f"{pdb1_id}.pdb")
            path2 = os.path.join(tmpdir, f"{pdb2_id}.pdb")

            for content, outpath in [(pdb1_content, path1), (pdb2_content, path2)]:
                data = content.encode() if isinstance(content, str) else content
                with open(outpath, 'wb') as fh:
                    fh.write(data)

            aligned1_text, aligned2_text = align_with_pymol(path1, path2)
            # print(aligned1_text, aligned2_text)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Alignment error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Processing error: {e}"}), 500

    # print(aligned1_text, aligned2_text)

    # 5. Return as JSON
    return jsonify({
        "aligned1": aligned1_text,
        "aligned2": aligned2_text
    })


@app.route("/api/barcontrast", methods=["GET"])
def api_barcontrast():
    """
    GET /api/barcontrast?pdb1=1avr[&pdb2=4pti][&db=rcsb][&align=true|false]

    return JSON:
    {
      "1avr": {"helix": [...], "strand": [...], "turn": [...]},
      "4pti": {"helix": [...], "strand": [...], "turn": [...]}
    }
    """
    pdb1_id = request.args.get("pdb1", "").lower()
    pdb2_id = request.args.get("pdb2", "").lower()
    db = request.args.get("db", "rcsb").lower()
    do_align = request.args.get("align", "true").lower() != "false"

    if not pdb1_id:
        return jsonify({"error": "parameter 'pdb1' is required"}), 400

    connector = ConnectorFactory.get_connector(db)
    if connector is None:
        return jsonify({"error": f"no connector for db '{db}'"}), 400

    # 下载第一个蛋白质
    try:
        pdb1_raw = connector.download_proteins_by_pdb_id(pdb1_id)
    except Exception as e:
        return jsonify({"error": f"download error (pdb1): {e}"}), 500

    result = {}

    if not pdb2_id:
        # 单蛋白质情况：不对齐，直接处理 DSSP
        try:
            result[pdb1_id] = _dssp_for_pdb_text(pdb1_raw)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"DSSP error (pdb1): {e}"}), 500
    else:
        # 下载第二个蛋白质
        try:
            pdb2_raw = connector.download_proteins_by_pdb_id(pdb2_id)
        except Exception as e:
            return jsonify({"error": f"download error (pdb2): {e}"}), 500

        # 对齐逻辑（如启用）
        if do_align:
            print("doing align...")
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    path1 = os.path.join(tmpdir, f"{pdb1_id}.pdb")
                    path2 = os.path.join(tmpdir, f"{pdb2_id}.pdb")
                    for txt, p in [(pdb1_raw, path1), (pdb2_raw, path2)]:
                        with open(p, "w") as fh:
                            fh.write(txt)
                    pdb1_text, pdb2_text = align_with_pymol(path1, path2)
            except Exception as e:
                return jsonify({"error": f"alignment error: {e}"}), 500
        else:
            pdb1_text, pdb2_text = pdb1_raw, pdb2_raw

        # 分别进行 DSSP
        try:
            result[pdb1_id] = _dssp_for_pdb_text(pdb1_text)
            result[pdb2_id] = _dssp_for_pdb_text(pdb2_text)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"DSSP error: {e}"}), 500

    return jsonify(result)

