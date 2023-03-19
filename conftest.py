import pytest
import os
from chocan import storage_system

# Loading `storage_records` fixture changes `storage_system.record_directory` to point
# towards the "records" folder in the "test" directory.
@pytest.fixture
def storage_records():
    old_path = storage_system.record_directory
    fixture_record_folder = os.path.dirname(os.path.abspath(__file__)) + "/tests/records/"
    storage_system.record_directory = fixture_record_folder
    yield fixture_record_folder
    storage_system.record_directory = old_path

def _get_json_cache(file_path : str) -> str:
    file = open(file_path, "r")
    json = file.read()
    file.close()
    return json

def _write_json_cache(json : str, file_path : str) -> None:
    file = open(file_path, "w")
    file.write(json)
    file.close()
    return None

# Loading the `record_cleaner` fixture will store a cache of the current json records
# in the "records" folder in the "test" directory. When the fixture ends, it will restore
# the json records to the state in the cache. This allows tests to modify records without
# making persistent changes to the files after the tests are done.
@pytest.fixture
def record_cleaner(storage_records):
    member_path   = storage_system.file_path(storage_system.RecordType.MEMBER)
    provider_path = storage_system.file_path(storage_system.RecordType.PROVIDER)
    service_path  = storage_system.file_path(storage_system.RecordType.SERVICE)
    member_json   = _get_json_cache(member_path)
    provider_json = _get_json_cache(provider_path)
    service_json  = _get_json_cache(service_path)
    yield
    _write_json_cache(member_json, member_path)
    _write_json_cache(provider_json, provider_path)
    _write_json_cache(service_json, service_path)