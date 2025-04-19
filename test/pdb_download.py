import requests

pdb_id = '7LHD'
url = f'https://files.rcsb.org/download/{pdb_id}.pdb'

response = requests.get(url)
if response.ok:
    with open(f'{pdb_id}.pdb', 'w') as file:
        file.write(response.text)
    print(f"PDB file {pdb_id}.pdb downloaded successfully.")
else:
    print(f"Failed to download PDB file {pdb_id}.")
