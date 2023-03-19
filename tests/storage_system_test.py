from chocan import storage_system
import pytest

def test_get_all_records_many(storage_records):
    records = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    assert (len(records) == 3)
    records = storage_system.get_all_records(storage_system.RecordType.PROVIDER)
    assert (len(records) == 2)
    records = storage_system.get_all_records(storage_system.RecordType.SERVICE)
    assert (len(records) == 1)

def test_create_record_member(record_cleaner):
    records = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    # Test that there is no record with member number 4242.
    assert not next((x for x in records if x['number'] == 4242), None)
    record = {
        "name": "Test Member",
        "street": "Street Ave",
        "city": "Portland",
        "state": "OR",
        "zip": "97214",
        "number": 4242,
        "deleted":False
    }
    storage_system.create_record(storage_system.RecordType.MEMBER, record)
    records = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    # Test that the record with member number 4242 exists.
    assert next((x for x in records if x['number'] == 4242), None)

def test_get_record(storage_records):
    record1 = storage_system.get_record(storage_system.RecordType.MEMBER, 3)
    assert record1['name'] == "Taylor Todds"
    record2 = storage_system.get_record(storage_system.RecordType.PROVIDER, 2)
    assert record2['name'] == "Provider 2"
    with pytest.raises(storage_system.InvalidRecordType):
        storage_system.get_record(storage_system.RecordType.SERVICE, 2)
        # this should not be reached because the above line raises an error
        assert False

def test_update_record(record_cleaner):
    record1 = storage_system.get_record(storage_system.RecordType.MEMBER, 3)
    assert record1['name'] == "Taylor Todds"
    record1['name'] = "Taylor Franks"
    storage_system.update_record(storage_system.RecordType.MEMBER, 3, record1)
    record1 = storage_system.get_record(storage_system.RecordType.MEMBER, 3)
    assert record1['name'] == "Taylor Franks"

    record2 = storage_system.get_record(storage_system.RecordType.PROVIDER, 2)
    assert record2['name'] == "Provider 2"
    record2['name'] = "Provider Update"
    storage_system.update_record(storage_system.RecordType.PROVIDER, 2, record2)
    record2 = storage_system.get_record(storage_system.RecordType.PROVIDER, 2)
    assert record2['name'] == "Provider Update"

    with pytest.raises(storage_system.InvalidRecordType):
        storage_system.update_record(storage_system.RecordType.SERVICE, 2, {})
        # this should not be reached because the above line raises an error
        assert False

def test_update_record_invalid(record_cleaner):
    with pytest.raises(storage_system.InvalidRecordNumber):
        storage_system.update_record(storage_system.RecordType.MEMBER, 987, {})
        # this should not be reached because the above line raises an error
        assert False

def test_delete_record(record_cleaner):
    record1 = storage_system.get_record(storage_system.RecordType.MEMBER, 3)
    assert record1['name'] == "Taylor Todds"
    storage_system.delete_record(storage_system.RecordType.MEMBER, 3)
    record1 = storage_system.get_record(storage_system.RecordType.MEMBER, 3)
    assert record1['deleted'] == True

    record2 = storage_system.get_record(storage_system.RecordType.PROVIDER, 2)
    assert record2['name'] == "Provider 2"
    storage_system.delete_record(storage_system.RecordType.PROVIDER, 2)
    record2 = storage_system.get_record(storage_system.RecordType.PROVIDER, 2)
    assert record2['deleted'] == True

    with pytest.raises(storage_system.InvalidRecordType):
        storage_system.delete_record(storage_system.RecordType.SERVICE, 2)
        # this should not be reached because the above line raises an error
        assert False

def test_delete_record_invalid(record_cleaner):
    with pytest.raises(storage_system.InvalidRecordNumber):
        storage_system.delete_record(storage_system.RecordType.MEMBER, 87)
        # this should not be reached because the above line raises an error
        assert False

# TODO:
# def test_create_report(report_cleaner):
#     pass