from arriraw_legacy_metadata_reader.IDI import IDI
from arriraw_legacy_metadata_reader.ICI import ICI
from arriraw_legacy_metadata_reader.CDI import CDI
from arriraw_legacy_metadata_reader.LDI import LDI
from arriraw_legacy_metadata_reader.VFX import VFX
from arriraw_legacy_metadata_reader.CID import CID
from arriraw_legacy_metadata_reader.SID import SID
from arriraw_legacy_metadata_reader.FLI import FLI
from arriraw_legacy_metadata_reader.NRI import NRI

import pandas as pd
import json

class ArriRawLegacyMetadataReader:
    def __init__(self, file_path, fields_to_extract=None):
        try:
            with open(file_path, 'rb') as f:
                self.rawdata = f.read(4096)
        except FileNotFoundError as e:
            raise e
        self.fields_to_extract = fields_to_extract

        self.objects = []

        self.objects.append(IDI(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(ICI(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(CDI(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(LDI(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(VFX(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(CID(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(SID(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(FLI(self.rawdata, fields_to_extract=self.fields_to_extract))
        self.objects.append(NRI(self.rawdata, fields_to_extract=self.fields_to_extract))

    def get_dictionary(self) -> dict:
        metadata = {}

        for obj in self.objects:
            metadata.update(obj.get_data())

        return metadata
    
    def get_dataframe(self) -> pd.DataFrame:
        metadata = {}

        for obj in self.objects:
            metadata.update(obj.get_data())

        return pd.DataFrame.from_dict(metadata, orient='index').transpose()
    
    def get_json(self) -> str:
        return json.dumps(self.get_dictionary(), indent=4)
    
    def list_fields(self) -> list:
        fields = []

        for obj in self.objects:
            fields.extend(obj.list_fields())

        return fields

def read_metadata(file_path, fields_to_extract=None) -> dict:
    return ArriRawLegacyMetadataReader(file_path, fields_to_extract=fields_to_extract).get_dictionary()