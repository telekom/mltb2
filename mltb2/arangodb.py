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
from dotenv import dotenv_values

from mltb2.db import BatchDataManager


@dataclass
class ArangoBatchDataManager(BatchDataManager):
    """TODO: add docstring."""

    hosts: Union[str, Sequence[str]]
    db_name: str
    username: str
    password: str
    collection_name: str
    attribute_name: str
    batch_size: int = 20
    aql_overwrite: Optional[str] = None

    @classmethod
    def from_config_file(cls, config_file_name, aql_overwrite=None):
        """Construct ``ArangoDataManager`` from config file."""
        arango_config = dotenv_values(config_file_name)
        return cls(
            hosts=arango_config["hosts"],
            db_name=arango_config["db_name"],
            username=arango_config["username"],
            password=arango_config["password"],
            collection_name=arango_config["collection_name"],
            attribute_name=arango_config["attribute_name"],
            batch_size=int(arango_config["batch_size"]),
            aql_overwrite=aql_overwrite,
        )

    def _get_arango_client(self):
        arango_client = ArangoClient(hosts=self.hosts)
        return arango_client

    def _get_connection(self, arango_client):
        connection = arango_client.db(self.db_name, username=self.username, password=self.password)
        return connection

    def load_batch(self) -> Sequence:
        """TODO: add docstring."""
        with closing(self._get_arango_client()) as arango_client:
            connection = self._get_connection(arango_client)
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
                bind_vars=bind_vars,
                batch_size=self.batch_size,
            )
            with closing(cursor) as closing_cursor:
                batch = closing_cursor.batch()
        return batch

    def save_batch(self, batch: Sequence):
        """TODO: add docstring."""
        with closing(self._get_arango_client()) as arango_client:
            connection = self._get_connection(arango_client)
            collection = connection.collection(self.collection_name)
            collection.import_bulk(batch, on_duplicate="update")
