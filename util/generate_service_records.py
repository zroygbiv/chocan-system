# This code will overwrite anything in your `./reports` directory. Use this program
# to generate thousands of service records in order to test the 999 weekly provider
# service limit and to test report generation speed.
import json
import random
import sys
from datetime import datetime, timedelta

_providers = [
    {
        "name": "Chocolate helpers",
        "street": "431 ne",
        "city": "Portland",
        "state": "OR",
        "zip": "97214",
        "number": 1,
        "deleted": False,
    },
    {
        "name": "Healthy pros",
        "street": "98",
        "city": "Vancouver",
        "state": "WA",
        "zip": "98686",
        "number": 2,
        "deleted": False,
    },
    {
        "name": "Empty Provider",
        "street": "123",
        "city": "Portland",
        "state": "OR",
        "zip": "97214",
        "number": 3,
        "deleted": False,
    },
    {
        "name": "Deleted Provider",
        "street": "98 St",
        "city": "Portland",
        "state": "OR",
        "zip": "97213",
        "number": 4,
        "deleted": True,
    },
]

_members = [
    {
        "name": "Robert peterson",
        "street": "123",
        "city": "Portland",
        "state": "OR",
        "zip": "97214",
        "number": 1,
        "active": True,
        "deleted": False,
    },
    {
        "name": "Steve Stevies",
        "street": "Apple St",
        "city": "Portland",
        "state": "OR",
        "zip": "97215",
        "number": 2,
        "active": True,
        "deleted": False,
    },
    {
        "name": "Empty Member",
        "street": "Frank St",
        "city": "Portland",
        "state": "OR",
        "zip": "97215",
        "number": 3,
        "active": True,
        "deleted": False,
    },
    {
        "name": "Deleted Member",
        "street": "Jane St",
        "city": "Seattle",
        "state": "WA",
        "zip": "98734",
        "number": 4,
        "active": True,
        "deleted": True,
    },
]

MAX_SERVICE_CODE = 10
MAX_FEE_CENTS = 99999

_report_directory = "./records/"
_member_file = "members.json"
_provider_file = "providers.json"
_service_file = "services.json"

_services = []

# create given amount of service records for given provider and member
def create_service_records(provider, member, amount = 1000):
    for _ in range(0, amount):
        sys.stdout.write(".")
        date = (datetime.now() - timedelta(days = random.randrange(0,2))).isoformat()
        service = {
            "provider_number": provider["number"],
            "member_number": member["number"],
            "member_name": member["name"],
            "service_code": random.randrange(1, MAX_SERVICE_CODE),
            "fee": random.randrange(1000, MAX_FEE_CENTS),
            "date_of_service": date,
            "date_received": date,
            "comments": "N/A"
        }
        _services.append(service)

print("Writing members")
json.dump(_members, open(_report_directory + _member_file, "w+"))
print("Writing providers")
json.dump(_providers, open(_report_directory + _provider_file, "w+"))

print("Writing services")
create_service_records(_providers[0], _members[0], 35)
create_service_records(_providers[1], _members[0], 35)
create_service_records(_providers[3], _members[0], 35)
create_service_records(_providers[0], _members[1], 35)
create_service_records(_providers[1], _members[1], 35)
create_service_records(_providers[3], _members[1], 35)
create_service_records(_providers[0], _members[3], 35)
create_service_records(_providers[1], _members[3], 35)
create_service_records(_providers[3], _members[3], 35)
json.dump(_services, open(_report_directory + _service_file, "w+"))
print("done")