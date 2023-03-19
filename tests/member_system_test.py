from chocan import member_system

def test_create_member(record_cleaner):
    member = member_system.create_member(
        name   = "Member 4",
        street = "3rd Ave",
        city   = "Portland",
        state  = "OR",
        zip    = "34567"
    )
    assert member.name   == "Member 4"
    assert member.street == "3rd Ave"
    assert member.city   == "Portland"
    assert member.state  == "OR"
    assert member.zip    == "34567"
    assert member.number == 4

def test_get_all_members(storage_records):
    members = member_system.get_all_members()
    assert len(members) == 3
    assert members[0].name   == "Patty Tester"
    assert members[0].street == "123 Alphabet"
    assert members[0].city   == "Portlandia"
    assert members[0].state  == "OR"
    assert members[0].zip    == "97214"
    assert members[0].number == 1

    assert members[1].name   == "Steven Software"
    assert members[1].street == "10th Circle"
    assert members[1].city   == "Vancouver"
    assert members[1].state  == "WA"
    assert members[1].zip    == "98686"
    assert members[1].number == 2

    assert members[2].name   == "Taylor Todds"
    assert members[2].street == "1900 Morrison St"
    assert members[2].city   == "Portlandia"
    assert members[2].state  == "OR"
    assert members[2].zip    == "97214"
    assert members[2].number == 3

def test_get_member(storage_records):
    member = member_system.get_member(3)
    assert member.name   == "Taylor Todds"
    assert member.street == "1900 Morrison St"
    assert member.city   == "Portlandia"
    assert member.state  == "OR"
    assert member.zip    == "97214"
    assert member.number == 3

def test_delete_member(record_cleaner):
    member = member_system.get_member(3)
    assert member.name == "Taylor Todds"
    member_system.delete_member(3)
    member = member_system.get_member(3)
    assert member.deleted == True

def test_update_member(record_cleaner):
    member = member_system.get_member(2)
    assert member.name != "Updated Name"
    assert member.zip != "123123"
    updated_member = member_system.update_member(
        name = "Updated Name",
        street = member.street,
        city = member.city,
        state = member.state,
        zip = "123123",
        active = member.active,
        number = member.number,
        deleted = member.deleted
    )
    member = member_system.get_member(2)
    assert member.name == "Updated Name"
    assert member.zip == "123123"

def test_get_active_member(record_cleaner):
    active_member = member_system.get_active_member(1)
    assert active_member.deleted == False
    
    # Delete one provider and test that their no longer active
    member_system.delete_member(1)
    active_member = member_system.get_active_member(1)
    assert active_member == None

def test_get_all_active_members(record_cleaner):
    active_members = member_system.get_all_active_members()
    assert len(active_members) == 3
    assert active_members[0].name    == "Patty Tester"
    assert active_members[0].street  == "123 Alphabet"
    assert active_members[0].city    == "Portlandia"
    assert active_members[0].state   == "OR"
    assert active_members[0].zip     == "97214"
    assert active_members[0].number  == 1
    assert active_members[0].deleted == False

    assert active_members[1].name    == "Steven Software"
    assert active_members[1].street  == "10th Circle"
    assert active_members[1].city    == "Vancouver"
    assert active_members[1].state   == "WA"
    assert active_members[1].zip     == "98686"
    assert active_members[1].number  == 2
    assert active_members[1].deleted == False

    assert active_members[2].name    == "Taylor Todds"
    assert active_members[2].street  == "1900 Morrison St"
    assert active_members[2].city    == "Portlandia"
    assert active_members[2].state   == "OR"
    assert active_members[2].zip     == "97214"
    assert active_members[2].number  == 3
    assert active_members[2].deleted == False

    # Delete one provider and test that their no longer active
    member_system.delete_member(1)
    member_system.delete_member(2)
    active_members = member_system.get_all_active_members()
    assert len(active_members) == 1
    assert active_members[0].name    == "Taylor Todds"
    assert active_members[0].street  == "1900 Morrison St"
    assert active_members[0].city    == "Portlandia"
    assert active_members[0].state   == "OR"
    assert active_members[0].zip     == "97214"
    assert active_members[0].number  == 3
    assert active_members[0].deleted == False
