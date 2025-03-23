import abc
from abc import ABC


class ConnectorABC(ABC):

    @abc.abstractmethod
    def search_proteins_by_keyword(self, keyword):
        pass

    @abc.abstractmethod
    def download_proteins_by_pdb_id(self, pdb_id):
        pass