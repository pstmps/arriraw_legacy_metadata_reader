"""
Defines the ArriRawLegacyMetadataReader class,
which is used to read metadata from ARRIRAW files.
"""

import json
from typing import Union
import pandas as pd

from arriraw_legacy_metadata_reader.IDI import Idi
from arriraw_legacy_metadata_reader.ICI import Ici
from arriraw_legacy_metadata_reader.CDI import Cdi
from arriraw_legacy_metadata_reader.LDI import Ldi
from arriraw_legacy_metadata_reader.VFX import Vfx
from arriraw_legacy_metadata_reader.CID import Cid
from arriraw_legacy_metadata_reader.SID import Sid
from arriraw_legacy_metadata_reader.FLI import Fli
from arriraw_legacy_metadata_reader.NRI import Nri


class ArriRawLegacyMetadataReader:
    """
    Class to read the metadata from an ARRIRAW file.
    """

    def __init__(self, file_path: str, fields_to_extract: Union[list, None] = None):
        try:
            with open(file_path, "rb") as f:
                self.rawdata = f.read(4096)
        except (FileNotFoundError, IOError) as e:
            raise e
        self.fields_to_extract = fields_to_extract

        self.objects = [
            Idi(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Ici(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Cdi(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Ldi(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Vfx(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Cid(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Sid(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Fli(file=self.rawdata, fields_to_extract=self.fields_to_extract),
            Nri(file=self.rawdata, fields_to_extract=self.fields_to_extract),
        ]

    def _collect_metadata(self) -> dict:
        metadata = {}
        for obj in self.objects:
            metadata.update(obj.get_data())
        return metadata

    def get_dictionary(self) -> dict:
        """
        Method to return the metadata as a dictionary
        Returns:
            dict: The metadata as a dictionary
        """
        return self._collect_metadata()

    def get_dataframe(self) -> pd.DataFrame:
        """
        Method to return the metadata as a pandas DataFrame
        Returns:
            pandas.DataFrame: The metadata as a pandas DataFrame
        """
        metadata = self._collect_metadata()
        return pd.DataFrame.from_dict(metadata, orient="index").transpose()

    def get_json(self) -> str:
        """
        Method to return the metadata as a JSON string
        Returns:
            str: The metadata as a JSON string
        """
        return json.dumps(self.get_dictionary(), indent=4)

    def list_fields(self) -> list:
        """
        Method to return a list of all fields in the metadata
        Returns:
            list: A list of all fields in the metadata
        """
        fields = []
        for obj in self.objects:
            fields.extend(obj.list_fields())
        return fields


def read_metadata(file_path: str, fields_to_extract: Union[list, None] = None) -> dict:
    """
    Function to read the metadata from an ARRIRAW file.
    Creates a new ArriRawLegacyMetadataReader object and returns the metadata as a dictionary.
    Args:
        file_path (str): The path to the ARRIRAW file
        fields_to_extract (Union[list, None]): A list of fields to extract.
            If None, all fields will be extracted.
    Returns:
        dict: The metadata as a dictionary
    """
    return ArriRawLegacyMetadataReader(
        file_path=file_path, fields_to_extract=fields_to_extract
    ).get_dictionary()
