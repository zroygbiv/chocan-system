from chocan import provider_directory_system

def test_get_provider_service_valid():
    provider_service = provider_directory_system.get_provider_service(1)
    assert provider_service.name == "4 Hour Course: Exploring sugar alternatives"

def test_get_provider_service_invalid():
    provider_service = provider_directory_system.get_provider_service(2134)
    assert provider_service == None