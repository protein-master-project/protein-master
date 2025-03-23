from app import app
from flask import Flask, request, jsonify, Response
import requests
from rcsbapi.search import TextQuery


@app.route('/test', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask backend!"}
    return jsonify(data)


@app.route('/search', methods=['GET'])
def search_proteins():
    """
    1. Endpoint: Search for protein structure IDs by a given keyword
       - GET /search?keyword=hemoglobin&db=rcsb
       - Returns a JSON object of the form: {"results": ["4HHB", "1A3N", ...]}
    """
    keyword = request.args.get('keyword', '').strip()
    db = request.args.get('db', '').strip().lower()

    if not keyword or not db:
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    try:
        # Use TextQuery to perform a full-text search on RCSB
        query = TextQuery(value=keyword)
        results = list(query())  # Convert generator to a list
    except Exception as e:
        return jsonify({"error": f"Search error: {str(e)}"}), 500

    return jsonify({"results": results})


@app.route('/download', methods=['GET'])
def download_pdb():
    """
    2. Endpoint: Download a PDB file by a given PDB ID and return it to the frontend
       - GET /download?pdb_id=3SL9&db=rcsb
       - Returns a PDB file as an attachment
    """
    pdb_id = request.args.get('pdb_id', '').strip()
    db = request.args.get('db', '').strip().lower()

    if not pdb_id or not db:
        return jsonify({"error": "Missing 'pdb_id' parameter"}), 400

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if not response.ok:
        return jsonify({"error": f"Failed to download the PDB file for {pdb_id}"}), 404

    # Return the downloaded PDB file content as a Response
    return Response(
        response.text,
        mimetype='chemical/x-pdb',
        headers={
            "Content-Disposition": f"attachment; filename={pdb_id}.pdb"
        }
    )
