from chocan import report_system, member_system, provider_system

def test_format_file_name():
    s = report_system.format_file_name("foo man")
    assert s == "foo_man"
    s = report_system.format_file_name("foo       foo")
    assert s == "foo_foo"
    s = report_system.format_file_name("fu\tchu")
    assert s == "fu_chu"

def test_group_by_number(storage_records):
    members = member_system.get_all_members()
    m = report_system.group_by_number(members)
    assert m[1].name == "Patty Tester"
    assert m[3].name == "Taylor Todds"
    providers = provider_system.get_all_providers()
    p = report_system.group_by_number(providers)
    assert p[1].name == "Provider 1"
    assert p[2].name == "Provider 2"