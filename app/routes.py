from app import app
from flask import Flask, request, jsonify, Response

from connecter import ConnectorFactory


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
