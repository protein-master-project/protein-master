import requests
from rcsbapi.data import DataQuery
# from rcsbapi.search import TextQuery
from rcsbapi.search import TextQuery, search_attributes as attrs
from connecter.connector_abc import ConnectorABC

class RCSBConnector(ConnectorABC):

    def _search_ids(self, keyword: str, max_hits: int = 100):
        q = TextQuery(keyword) & (attrs.rcsb_entry_info.polymer_entity_count_protein >= 1)
        ids = list(
            q(
                return_type="entry",
                # request_options={"paginate": {"start": 0, "rows": max_hits}}
            )
        )
        return ids[:max_hits]

    def fetch_entry_details(self, entry_ids, fields=None):
        default_fields = [
            "struct.title",
            "exptl.method",
            "rcsb_entry_info.resolution_combined"
        ]
        fields = fields or default_fields

        dq = DataQuery(
            input_type="entries",
            input_ids=entry_ids,
            return_data_list=fields
        )
        return dq.exec()["data"]["entries"]

    def search_proteins_by_keyword(self, keyword, max_hits=50, extra_fields=None):
        print(f"Searching proteins by keyword, {keyword}")

        try:
            ids = self._search_ids(keyword, max_hits)
            if not ids:
                return []
            return self.fetch_entry_details(ids, extra_fields)
        except Exception as e:
            print(f"Search error: {str(e)}")
            raise RuntimeError(f"RCSB query failed: {e}")

    # def search_proteins_by_keyword(self, keyword):
    #     """
    #     Use rcsbapi's TextQuery to perform a full-text search on RCSB
    #     and return a list of matching PDB IDs.
    #     """
    #     try:
    #         q_text = TextQuery(keyword)
    #         q_protein_type = attrs.entity_poly.rcsb_entity_polymer_type == "protein"
    #
    #         results = list((q_text & q_protein_type)(return_type="entry"))
    #
    #         print(results)
    #
    #         # query = TextQuery(value=keyword)
    #         # results = list(query())  # Convert the generator to a list
    #         return results
    #
    #     except Exception as e:
    #         # you could log the error or handle it as needed
    #         raise RuntimeError(f"Error searching proteins by keyword {keyword}: {e}")

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

