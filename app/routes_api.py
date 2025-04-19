import os
import subprocess
import tempfile

from app import app
from flask import Flask, request, jsonify, Response
from connecter import ConnectorFactory
from processor.protein_align_processor import align_with_pymol


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


