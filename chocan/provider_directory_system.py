from chocan import storage_system, ui_util
from typing import Optional
import json
import os

class ProviderService:
    def __init__(self, data : dict):
        self.code = data['code']
        self.fee  = data['fee']
        self.name = data['name']

    def for_report(self) -> str:
        s = (
            f"Code: {self.code}\n"
            f"Name: {self.name}\n"
            f"Fee: {ui_util.fee_format(self.fee)}\n"
        )
        return s

_provider_directory_report_file = "provider_directory.txt"

def _get_provider_directory() -> list[dict]:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, './prov_dir.json')
    return json.load(open(filename, 'r'))

def generate_provider_directory() -> None:
    directory = _get_provider_directory()
    services = map(lambda p: ProviderService(p).for_report(), directory)
    report = "\n".join(services)
    storage_system.create_report(_provider_directory_report_file, report)

def get_provider_service(code : int) -> Optional['ProviderService']:
    provider_services = _get_provider_directory()
    provider_service = next((ProviderService(p) for p in provider_services if p['code'] == code), None)
    return provider_service