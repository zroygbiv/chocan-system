from chocan import provider_system

def test_get_all_providers(record_cleaner):
    providers = provider_system.get_all_providers()
    assert len(providers) == 2
    assert providers[0].name   == "Provider 1"
    assert providers[0].street == "Office Street"
    assert providers[0].city   == "Portland"
    assert providers[0].state  == "OR"
    assert providers[0].zip    == "97214"
    assert providers[0].number == 1

    assert providers[1].name   == "Provider 2"
    assert providers[1].street == "Provider Ave"
    assert providers[1].city   == "Portland"
    assert providers[1].state  == "OR"
    assert providers[1].zip    == "97222"
    assert providers[1].number == 2

def test_create_provider(record_cleaner):
    provider = provider_system.create_provider(
        name   = "Provider 3",
        street = "3rd Ave",
        city   = "Portland",
        state  = "OR",
        zip    = "34567"
    )
    assert provider.name   == "Provider 3"
    assert provider.street == "3rd Ave"
    assert provider.city   == "Portland"
    assert provider.state  == "OR"
    assert provider.zip    == "34567"
    assert provider.number == 3
    assert provider.deleted == False

    # Check that the provider was actually created in the storage system.
    all_providers = provider_system.get_all_providers()
    assert len(all_providers)      == 3
    assert all_providers[2].name   == "Provider 3"
    assert all_providers[2].number == 3

def test_get_provider(record_cleaner):
    # fetches an existing provider record
    provider = provider_system.get_provider(1)
    assert provider.number == 1

    # fetches a non-existing provider record
    provider = provider_system.get_provider(999999999)
    assert provider == None

def test_update_provider(record_cleaner):
    provider = provider_system.update_provider(
        name   = "Updated Provider 1",
        street = "Updated Street",
        city   = "Portland",
        state  = "OR",
        zip    = "97214",
        number = 1,
        deleted = False
    )
    assert provider.name   == "Updated Provider 1"
    assert provider.street == "Updated Street"
    assert provider.city   == "Portland"
    assert provider.state  == "OR"
    assert provider.zip    == "97214"
    assert provider.number == 1
    assert provider.deleted == False

    # Check that the provider was updated in the storage system.
    updated_provider = provider_system.get_provider(1)
    assert updated_provider.name   == "Updated Provider 1"
    assert updated_provider.street == "Updated Street"

def test_delete_provider(record_cleaner):
    provider_system.delete_provider(2)

    # Check that provider 2 was deleted from the storage system.
    del_provider = provider_system.get_provider(2)
    assert del_provider.deleted == True

def test_verify_provider(record_cleaner):
    test_1 = provider_system.verify_provider(1)
    test_2 = provider_system.verify_provider(0)
    assert test_1 == True
    assert test_2 == False

def test_get_active_provider(record_cleaner):
    provider = provider_system.get_active_provider(1)
    assert provider.deleted == False

    # Delete one provider and test that their no longer active
    provider_system.delete_provider(1)
    provider = provider_system.get_active_provider(1)
    assert provider == None

def test_get_all_active_providers(record_cleaner):
    active_providers = provider_system.get_all_active_providers()
    assert len(active_providers) == 2
    assert active_providers[0].name    == "Provider 1"
    assert active_providers[0].street  == "Office Street"
    assert active_providers[0].city    == "Portland"
    assert active_providers[0].state   == "OR"
    assert active_providers[0].zip     == "97214"
    assert active_providers[0].number  == 1
    assert active_providers[0].deleted == False

    assert active_providers[1].name    == "Provider 2"
    assert active_providers[1].street  == "Provider Ave"
    assert active_providers[1].city    == "Portland"
    assert active_providers[1].state   == "OR"
    assert active_providers[1].zip     == "97222"
    assert active_providers[1].number  == 2
    assert active_providers[0].deleted == False

    # Delete one provider and test that their no longer active
    provider_system.delete_provider(1)
    active_providers = provider_system.get_all_active_providers()
    assert len(active_providers) == 1
    assert active_providers[0].name    == "Provider 2"
    assert active_providers[0].street  == "Provider Ave"
    assert active_providers[0].city    == "Portland"
    assert active_providers[0].state   == "OR"
    assert active_providers[0].zip     == "97222"
    assert active_providers[0].number  == 2
    assert active_providers[0].deleted == False
