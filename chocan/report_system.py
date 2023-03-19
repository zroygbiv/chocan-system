from datetime import datetime
from functools import reduce
import service_system, member_system, provider_system, provider_directory_system, storage_system, ui_util

def format_file_name(name : str) -> str:
    # replace whitespace with underscore
    s = "_".join(name.split())
    return s

# turns a list of records into a dictionary accessible by the record number
def group_by_number(records : list[any]) -> dict:
    result = {}
    for r in records:
        result[r.number] = r
    return result

# turns a list of services into a dictionary grouped by the member number so you
# can access all the services of a member by using the member number as a key
def group_by_member_number(records : list['service_system.ServiceRecord']) -> dict:
    result = {}
    for r in records:
        if r.member_number in result:
            result[r.member_number].append(r)
        else:
            result[r.member_number] = [r]
    return result

# turns a list of services into a dictionary grouped by the provider number so you
# can access all the services of a provider by using the provider number as a key
def group_by_provider_number(records : list['service_system.ServiceRecord']) -> dict:
    result = {}
    for r in records:
        if r.provider_number in result:
            result[r.provider_number].append(r)
        else:
            result[r.provider_number] = [r]
    return result

def _dated_file_name(name : str) -> str:
    formatted_name = format_file_name(name)
    date = datetime.today().strftime("%d-%m-%Y")
    file_name = f"{formatted_name}-{date}.txt"
    return file_name

def _member_service_info(service, providers) -> str:
    provider_name = providers[service.provider_number].name
    service_name = provider_directory_system.get_provider_service(service.service_code).name
    info = (
        f"Date of Service: {service.date_of_service_pretty()}\n"
        f"Provider Name: {provider_name}\n"
        f"Service Name: {service_name}\n"
    )
    return info

def _build_member_service_report(member, services, providers) -> None:
    file_name = _dated_file_name(member.name)
    member_info = (
        f"Member Name: {member.name}\n"
        f"Member Number: {member.number}\n"
        f"Member Street: {member.street}\n"
        f"Member City: {member.city}\n"
        f"Member State: {member.state}\n"
        f"Member Zip: {member.zip}\n"
    )
    service_info = map(lambda s: _member_service_info(s, providers), services)
    service_info = "\n".join(service_info)
    info = (
        f"{member_info}\n"
        "Services:\n"
        f"{service_info}"
    )
    storage_system.create_report(file_name, info)

def _build_member_service_reports(members, services, providers) -> None:
    for n in list(services.keys()):
        _build_member_service_report(members[n], services[n], providers)

def _provider_service_info(service, members) -> str:
    member_name = members[service.member_number].name
    service_name = provider_directory_system.get_provider_service(service.service_code).name
    info = (
        f"Date of Service: {service.date_of_service_pretty()}\n"
        f"Date Received: {service.date_received_pretty()}\n"
        f"Member Name: {member_name}\n"
        f"Member Number: {service.member_number}\n"
        f"Service Code: {service.service_code}\n"
        f"Fee: {ui_util.fee_format(service.fee)}\n"
    )
    return info

def _build_provider_report(provider, services, members) -> None:
    file_name = _dated_file_name(provider.name)
    provider_info = (
        f"Provider Name: {provider.name}\n"
        f"Provider Number: {provider.number}\n"
        f"Provider Street: {provider.street}\n"
        f"Provider City: {provider.city}\n"
        f"Provider State: {provider.state}\n"
        f"Provider Zip: {provider.zip}\n"
    )
    service_info = map(lambda s: _provider_service_info(s, members), services)
    service_info = "\n".join(service_info)
    total_fee = reduce(lambda a, b: a + b, map(lambda s: s.fee, services))
    info = (
        f"{provider_info}\n"
        "Services:\n"
        f"{service_info}\n"
        f"Total Consultations: {len(services)}\n"
        f"Total Fee: {ui_util.fee_format(total_fee)}"
    )
    storage_system.create_report(file_name, info)

def _build_provider_reports(providers, services, members) -> None:
    for n in list(services.keys()):
        _build_provider_report(providers[n], services[n], members)

def _provider_mgmt_info(provider, services) -> str:
    total_consults = len(services)
    total_fee = reduce(lambda a, b: a + b, map(lambda s: s.fee, services))
    info = (
        f"Provider Name: {provider.name}\n"
        f"Provider Total Consultations: {total_consults}\n"
        f"Provider Total Fee: {ui_util.fee_format(total_fee)}\n"
    )
    return info

def _build_mgmt_report(services, services_by_provider, providers) -> None:
    file_name = _dated_file_name("MGMT")
    provider_info = map(lambda p: _provider_mgmt_info(providers[p], services_by_provider[p]), services_by_provider.keys())
    provider_info = "\n".join(provider_info)
    total_providers = len(services_by_provider.keys())
    total_consults = len(services)
    total_fee = reduce(lambda a, b: a + b, map(lambda s: s.fee, services))
    info = (
        "Providers:\n"
        f"{provider_info}"
        "\nTotals:\n"
        f"Total Providers: {total_providers}\n"
        f"Total Consultations: {total_consults}\n"
        f"Total Fee: {ui_util.fee_format(total_fee)}"
    )
    storage_system.create_report(file_name, info)

def _provider_eft_info(provider, services):
    total_fee = reduce(lambda a, b: a + b, map(lambda s: s.fee, services))
    info = (
        f"Provider Name: {provider.name}\n"
        f"Provider Number: {provider.number}\n"
        f"Amount to be transferred: {ui_util.fee_format(total_fee)}\n"
    )
    return info

def _build_eft_report(providers, services) -> None:
    file_name = _dated_file_name("EFT")
    provider_info = map(lambda p: _provider_eft_info(providers[p], services[p]), services.keys())
    info = "\n".join(provider_info)
    storage_system.create_report(file_name, info)

def generate_provider_report() -> None:
    members = group_by_number(member_system.get_all_members())
    providers = group_by_number(provider_system.get_all_providers())
    services = group_by_provider_number(service_system.get_services_this_week())
    _build_provider_reports(providers, services, members)

def generate_member_service_report() -> None:
    members = group_by_number(member_system.get_all_members())
    providers = group_by_number(provider_system.get_all_providers())
    services = group_by_member_number(service_system.get_services_this_week())
    _build_member_service_reports(members, services, providers)

def generate_mgmt_report() -> None:
    services = service_system.get_services_this_week()
    services_by_provider = group_by_provider_number(services)
    providers = group_by_number(provider_system.get_all_providers())
    _build_mgmt_report(services, services_by_provider, providers)

def generate_eft_report() -> None:
    providers = group_by_number(provider_system.get_all_providers())
    services = group_by_provider_number(service_system.get_services_this_week())
    _build_eft_report(providers, services)
