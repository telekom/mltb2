# Copyright (c) 2023 Philip May
# This software is distributed under the terms of the MIT license
# which is available at https://opensource.org/licenses/MIT

"""ArangoDB utils module.

Hint:
    Use pip to install the necessary dependencies for this module:
    ``pip install mltb2[arangodb]``
"""


from contextlib import closing
from dataclasses import dataclass
from typing import Optional, Sequence, Union

from arango import ArangoClient
from arango.database import StandardDatabase
from dotenv import dotenv_values

from mltb2.db import AbstractBatchDataManager


@dataclass
class ArangoBatchDataManager(AbstractBatchDataManager):
    """ArangoDB implementation of the ``AbstractBatchDataManager``.

    Args:
        hosts: ArangoDB host or hosts.
        db_name: ArangoDB database name.
        username: ArangoDB username.
        password: ArangoDB password.
        collection_name: Documents from this collection are processed.
        attribute_name: This attribute is used to check if a document is already processed.
            If the attribute is not present in a document, the document is processed.
            If it is available the document is considered as already processed.
        batch_size: The batch size.
        aql_overwrite: AQL string to overwrite the default.
    """

    hosts: Union[str, Sequence[str]]
    db_name: str
    username: str
    password: str
    collection_name: str
    attribute_name: str
    batch_size: int = 20
    aql_overwrite: Optional[str] = None

    @classmethod
    def from_config_file(cls, config_file_name, aql_overwrite: Optional[str] = None):
        """Construct this from config file.

        The config file must contain these values:

        - ``hosts``
        - ``db_name``
        - ``username``
        - ``password``
        - ``collection_name``
        - ``attribute_name``
        - ``batch_size``

        Config file example:

        .. code-block::

            hosts="https://arangodb.com"
            db_name="my_ml_database"
            username="PhilipMay"
            password="secret"
            collection_name="my_ml_data"
            attribute_name="processing_metadata"
            batch_size=100

        Args:
            config_file_name: The config file name (path).
            aql_overwrite: AQL string to overwrite the default.
        """
        arango_config = dotenv_values(config_file_name)
        return cls(
            hosts=arango_config["hosts"],  # type: ignore
            db_name=arango_config["db_name"],  # type: ignore
            username=arango_config["username"],  # type: ignore
            password=arango_config["password"],  # type: ignore
            collection_name=arango_config["collection_name"],  # type: ignore
            attribute_name=arango_config["attribute_name"],  # type: ignore
            batch_size=int(arango_config["batch_size"]),  # type: ignore
            aql_overwrite=aql_overwrite,
        )

    def _arango_client_factory(self) -> ArangoClient:
        """Create an ArangoDB client."""
        arango_client = ArangoClient(hosts=self.hosts)
        return arango_client

    def _connection_factory(self, arango_client: ArangoClient) -> StandardDatabase:
        """Create an ArangoDB connection.

        Args:
            arango_client: ArangoDB client.
        """
        connection = arango_client.db(self.db_name, username=self.username, password=self.password)
        return connection

    def load_batch(self) -> Sequence:
        """Load a batch of data from the ArangoDB database.

        Returns:
            The loaded batch of data.
        """
        with closing(self._arango_client_factory()) as arango_client:
            connection = self._connection_factory(arango_client)
            bind_vars = {
                "@coll": self.collection_name,
                "attribute": self.attribute_name,
                "batch_size": self.batch_size,
            }
            if self.aql_overwrite is None:
                aql = "FOR doc IN @@coll FILTER !HAS(doc, @attribute) LIMIT @batch_size RETURN doc"
            else:
                aql = self.aql_overwrite
            cursor = connection.aql.execute(
                aql,
                bind_vars=bind_vars,  # type: ignore
                batch_size=self.batch_size,
            )
            with closing(cursor) as closing_cursor:  # type: ignore
                batch = closing_cursor.batch()  # type: ignore
        return batch  # type: ignore

    def save_batch(self, batch: Sequence) -> None:
        """Save a batch of data to the ArangoDB database.

        Args:
            batch: The batch of data to save.
        """
        with closing(self._arango_client_factory()) as arango_client:
            connection = self._connection_factory(arango_client)
            collection = connection.collection(self.collection_name)
            collection.import_bulk(batch, on_duplicate="update")