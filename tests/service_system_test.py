from datetime import datetime, timedelta
from chocan import service_system, storage_system
import pytest

def test_get_all_services(storage_records):
    services = service_system.get_all_services()
    assert len(services) == 1
    assert services[0].provider_number == 1
    assert services[0].member_number == 1
    assert services[0].member_name == "Patty Tester"
    assert services[0].service_code == 1
    assert services[0].fee == 4550
    assert services[0].date_of_service == "2023-10-05T14:48:00.000"
    assert services[0].date_received == "2023-10-05T14:48:00.000"

def test_create_service_record(record_cleaner):
    date = datetime.now().isoformat()
    service = service_system.create_service_record(
        provider_number = 12,
        member_number   = 20,
        member_name     = "Tim Apple",
        service_code    = 3,
        fee             = 500,
        date_of_service = date,
        date_received   = date,
        comments        = "Thanks!"
    )
    assert service.provider_number  == 12
    assert service.member_number    == 20
    assert service.member_name      == "Tim Apple"
    assert service.service_code     == 3
    assert service.fee              == 500
    assert service.date_of_service  == date
    assert service.date_received    == date
    assert service.comments         == "Thanks!"

def test_get_services_this_week(record_cleaner):
    storage_system.clear_all_records(storage_system.RecordType.SERVICE)
    # these records should be "this week".
    date1 = datetime.now().isoformat()
    service_system.create_service_record(1, 1, "Robert 456", 1, 3450, date1, date1, None)
    # this date should be listed before the previous record
    date2 = (datetime.now() - timedelta(minutes = 10)).isoformat()
    service_system.create_service_record(1, 1, "Apple Juice 89", 1, 3450, date2, date2, None)

    # this record should be "last week"
    date3 = (datetime.now() - timedelta(days = 8)).isoformat()
    service_system.create_service_record(1, 1, "Steve 123", 1, 40000, date3, date3, None)

    services = service_system.get_services_this_week()
    services = list(map(lambda s: s.member_name, services))
    assert ["Apple Juice 89", "Robert 456"] == services

def test_create_service_record_max_fee(record_cleaner):
    storage_system.clear_all_records(storage_system.RecordType.SERVICE)
    date = datetime.now().isoformat()
    service_system.create_service_record(
        provider_number = 1,
        member_number   = 1,
        member_name     = "Tim Apple",
        service_code    = 3,
        fee             = 9999999,
        date_of_service = date,
        date_received   = date,
        comments        = "Thanks!"
    )
    with pytest.raises(service_system.MaxFeeError):
        service_system.create_service_record(
            provider_number = 1,
            member_number   = 1,
            member_name     = "Tim Apple",
            service_code    = 3,
            fee             = 100,
            date_of_service = date,
            date_received   = date,
            comments        = "Thanks!"
        )