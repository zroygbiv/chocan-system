from chocan import storage_system
from constants import MAX_USER_NUM

class InvalidMemberNumber(Exception):
    pass

class MemberRecord:
    def __init__(self, data: dict):
        self.name    = data["name"]
        self.street  = data["street"]
        self.city    = data["city"]
        self.state   = data["state"]
        self.zip     = data["zip"]
        self.active  = data["active"]
        self.number  = data["number"]
        self.deleted = data["deleted"]

def generate_member_number() -> int:
    members = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    number = max(map(lambda r : r["number"], members)) + 1 if members else 1
    if number > MAX_USER_NUM:
        raise InvalidMemberNumber("Member number too large: " + str(number))
    return number

def create_member(
    name   : str,
    street : str,
    city   : str,
    state  : str,
    zip    : str
) -> 'MemberRecord':
    number = generate_member_number()
    # Create a dictionary for "data" using dictionary comprehension
    data = {
        "name"    : name,
        "street"  : street,
        "city"    : city,
        "state"   : state,
        "zip"     : zip,
        "number"  : number,
        "active"  : True,
        "deleted" : False
    }
    member_record = MemberRecord(data)
    storage_system.create_record(storage_system.RecordType.MEMBER, data)
    return member_record

def update_member(
    name    : str,
    street  : str,
    city    : str,
    state   : str,
    zip     : str,
    active  : bool,
    number  : int,
    deleted : bool
) -> 'MemberRecord':
    data = {
        "name"    : name,
        "street"  : street,
        "city"    : city,
        "state"   : state,
        "zip"     : zip,
        "number"  : number,
        "deleted" : deleted,
        "active"  : active
    }
    member_record = MemberRecord(data)
    storage_system.update_record(storage_system.RecordType.MEMBER, number, data)
    return member_record

def get_all_members() -> list['MemberRecord']:
    records = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    records = list(map(lambda r : MemberRecord(r), records))
    return records

def get_member(number: int) -> 'MemberRecord':
    record = storage_system.get_record(storage_system.RecordType.MEMBER, number)
    return MemberRecord(record) if record else None

def delete_member(number: int) -> None:
    storage_system.delete_record(storage_system.RecordType.MEMBER, number)
    return None

def get_active_member(number: int) -> 'MemberRecord':
    record = storage_system.get_record(storage_system.RecordType.MEMBER, number)
    return MemberRecord(record) if record and not record['deleted'] else None

def get_all_active_members() -> list['MemberRecord']:
    records = storage_system.get_all_records(storage_system.RecordType.MEMBER)
    active_records = filter(lambda r: r['deleted'] == False, records)
    active_members = list(map(lambda r: MemberRecord(r), active_records))
    return active_members