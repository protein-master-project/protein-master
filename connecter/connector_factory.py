from connecter.connector_abc import ConnectorABC
from connecter.rcsb import RCSBConnector


class ConnectorFactory:

    @staticmethod
    def get_connector(db_name: str) -> ConnectorABC:
        """
        Given a database name (e.g. 'rcsb'), return the appropriate connector.
        Return None if no matching connector is found.
        """
        if db_name.lower() == "rcsb":
            return RCSBConnector()
        # Add more connectors here if needed:
        # elif db_name.lower() == "some_other_db":
        #     return SomeOtherDBConnector()

        # No matching connector found
        return None