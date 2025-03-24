# ProteinMaster Backend

## Setup
```shell
pip install -r requirements.txt
python run.py
```

## APIs
```
Search proteins by keyword
http://127.0.0.1:8080/search?keyword=hemoglobin&db=rcsb

Get .pdb file content
http://127.0.0.1:8080/raw?pdb_id=1WMU&db=rcsb

Download .pdb file by pdb_id
http://127.0.0.1:8080/download?pdb_id=1WMU&db=rcsb
```

## Pages
```
# mol* demo
http://127.0.0.1:8080/molstar

# protein contact map demo
http://127.0.0.1:8080/matrix
```