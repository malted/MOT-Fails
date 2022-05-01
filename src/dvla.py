import requests
import os

def is_taxed(dvla_info):
    return dvla_info["taxStatus"] == "Taxed"


def has_MOT(dvla_info):
    return dvla_info["motStatus"] != "Not valid"


def vehicle_info(reg):
    return requests.post(
        """https://driver-vehicle-licensing.api.gov.uk/\
vehicle-enquiry/v1/vehicles""",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "x-api-key": os.environ["DVLA_API_KEY"],
        },
        json={"registrationNumber": reg},
    )
