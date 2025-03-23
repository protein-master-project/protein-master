import requests
from rcsbapi.search import TextQuery

from connecter.connector_abc import ConnectorABC


class RCSBConnector(ConnectorABC):

    def search_proteins_by_keyword(self, keyword):
        """
        Use rcsbapi's TextQuery to perform a full-text search on RCSB
        and return a list of matching PDB IDs.
        """
        try:
            query = TextQuery(value=keyword)
            results = list(query())  # Convert the generator to a list
            return results
        except Exception as e:
            # you could log the error or handle it as needed
            raise RuntimeError(f"Error searching proteins by keyword {keyword}: {e}")

    def download_proteins_by_pdb_id(self, pdb_id):
        """
        Download the PDB file content for a given PDB ID.
        Returns the PDB file content as a string.
        """
        url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        response = requests.get(url)
        if response.ok:
            return response.text
        else:
            raise RuntimeError(f"Failed to retrieve the PDB file for {pdb_id}")

