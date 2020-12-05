import sys
import math
import logging

# Magic to import electricitymapcontrib modules at root level
sys.path.insert(0, "./electricitymapcontrib")

from flask import Flask, request, jsonify
from pytz import timezone

from utils.parsers import PARSER_KEY_TO_DICT
from parsers.lib.quality import validate_production, ValidationError

app = Flask(__name__)


# Source: https://www.sciencedirect.com/science/article/pii/S2211467X19300549?via%3Dihub#tbl1
kgco2e_per_mwh = {
    "solar": 0.00410,
    "geothermal": 0.00664,
    "wind": 0.141,
    "nuclear": 10.3,
    "hydro": 16.2,
    "biomass": 50.9,
    "gas": 583,
    "unknown": 927,
    "oil": 1033,
    "coal": 1167,
}


def error(msg, code):
    return jsonify({"error": msg}), code


@app.route("/carbon-intensity/latest")
def get_co2eq_per_kwh():

    zone = request.args.get("zone", "")

    try:
        # Production seems to be more universally available.
        # If you want a more accurate and reliable results, please use the paid API from https://api.electricitymap.org
        parser = PARSER_KEY_TO_DICT["production"][zone]
    except KeyError as e:
        return error("zone not found", 400)

    try:
        # TODO: cache and/or save to database, right now we'll end up bombarding well meaning public APIs.
        # The current assumption is that the users will only call the endpoint once every 10-20 minutes, so this is fine.
        res = parser(zone, logger=logging.getLogger(__name__))
        if isinstance(res, (list, tuple)):
            # TODO: fix this to use all available data
            # At the time of writing this, I am only trying to get a working API with "close enough data"
            res = res[0]
    except Exception as e:
        return error("error fetching carbon intensity", 500)

    try:
        validate_production(res, zone)
    except ValidationError as e:
        # Log and respond with error
        return error("validation error: {}".format(str(e)), 500)

    co2eq = 0.0
    total_mw = 0.0
    default_co2e_per_mwh = kgco2e_per_mwh["unknown"]
    for (source_type, mw) in res["production"].items():
        # Sum of (emission per megawatt by source * megawatts generated)
        co2eq += kgco2e_per_mwh.get(source_type, default_co2e_per_mwh) * mw
        total_mw += mw

    # Dividing co2eq by total_mw will give us kgco2eq/MW.
    # For the sake of simplicity, we just assume it'll remain constant for 1 hour, so with that magic, it's kgco2eq/mwh
    # Since there's 1000 grams in 1 kg and 1000 kilowatts in 1 Megawatt, the number is same for gco2eq/kwh

    response = {
        "zone": zone,
        "carbonIntensity": math.ceil(co2eq / total_mw),
    }

    if "datetime" in res:
        # While python technically follows only ISO 8601 and seems rfc3339-compatible
        # api.electricitymap.com seems to use the Z notation instead of the +00:00 and we don't want to trip anything up
        timestring = res["datetime"].astimezone(timezone("UTC")).isoformat()[:-6] + "Z"
        response["datetime"] = timestring
        response["updatedAt"] = timestring

    return jsonify(response)


if __name__ == "__main__":
    app.run()
