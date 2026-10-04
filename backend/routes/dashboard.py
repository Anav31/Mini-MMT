import os
import json

from fastapi import APIRouter

router = APIRouter()

LOG_FILE = "healing_logs/healing_history.json"


##############################################################
# COMPLETE DASHBOARD
##############################################################

@router.get("/dashboard")
def get_dashboard_data():

    if not os.path.exists(LOG_FILE):

        return {

            "total_cycles": 0,

            "bugs_found": 0,

            "bugs_fixed": 0,

            "patches_applied": 0,

            "patches_already_present": 0,

            "success_rate": 0,

            "latest_cycle": None,

            "history": []

        }

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        history = json.load(file)

    if len(history) == 0:

        return {

            "total_cycles": 0,

            "bugs_found": 0,

            "bugs_fixed": 0,

            "patches_applied": 0,

            "patches_already_present": 0,

            "success_rate": 0,

            "latest_cycle": None,

            "history": []

        }

    total_cycles = len(history)

    bugs_found = sum(

        cycle.get(

            "bugs_found",

            0

        )

        for cycle

        in history

    )

    bugs_fixed = sum(

        cycle.get(

            "bugs_fixed",

            0

        )

        for cycle

        in history

    )

    patches_applied = sum(

        cycle.get(

            "patches_applied",

            0

        )

        for cycle

        in history

    )

    patches_already_present = sum(

        cycle.get(

            "patches_already_present",

            0

        )

        for cycle

        in history

    )

    success_rate = 0

    if bugs_found > 0:

        success_rate = round(

            (

                bugs_fixed

                /

                bugs_found

            ) * 100,

            2

        )

    latest_cycle = history[-1]

    return {

        "total_cycles":

        total_cycles,

        "bugs_found":

        bugs_found,

        "bugs_fixed":

        bugs_fixed,

        "patches_applied":

        patches_applied,

        "patches_already_present":

        patches_already_present,

        "success_rate":

        success_rate,

        "latest_cycle":

        latest_cycle,

        "history":

        history

    }


##############################################################
# LATEST HEALING CYCLE
##############################################################

@router.get("/dashboard/latest")
def latest_cycle():

    if not os.path.exists(LOG_FILE):

        return {}

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        history = json.load(file)

    if len(history) == 0:

        return {}

    return history[-1]


##############################################################
# HISTORY ONLY
##############################################################

@router.get("/dashboard/history")
def dashboard_history():

    if not os.path.exists(LOG_FILE):

        return []

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        history = json.load(file)

    return history