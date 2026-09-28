"""
Chapter 2 Project (Chapter Mini-Project): Dual-Mode Planning for RouteBot
REFERENCE SOLUTION. See starter.py's module docstring for the full
scenario (Cobblestone Courier Co.'s RouteBot). Running this file
directly passes all 7 structural self-checks.
"""

import json


ORDERS = {
    "ord-101": {"address": "12 Maple St", "package_type": "standard"},
    "ord-102": {"address": "9 Ridge Rd", "package_type": "fragile"},
}
ROUTES = {
    "ord-101": {"eta_minutes": 25, "distance_mi": 6.2},
    "ord-102": {"eta_minutes": 40, "distance_mi": 11.8},
}
DELAY_LOG = {
    "ord-201": {"status": "delayed", "notes": "driver reports heavy traffic on Route 9"},
    "ord-202": {"status": "delayed", "notes": "driver reports severe weather, roads icy"},
    "ord-203": {"status": "delayed", "notes": "driver hasn't checked in since pickup"},
}
TRAFFIC_REPORTS = {"ord-201": {"congestion": "heavy", "route": "Route 9"}}
WEATHER_CONDITIONS = {"ord-202": {"condition": "icy roads", "advisory": True}}
DRIVER_CHECKINS = {"ord-203": {"last_checkin_minutes_ago": 95, "status": "no response"}}


def verify_delivery_address(order_id):
    key = order_id.strip().lower()
    if key not in ORDERS:
        return {"error": f"no order on file for '{order_id}'"}
    return {"address": ORDERS[key]["address"], "verified": True}


def calculate_route(order_id):
    key = order_id.strip().lower()
    if key not in ROUTES:
        return {"error": f"no route data for '{order_id}'"}
    return ROUTES[key]


def dispatch_driver(order_id):
    key = order_id.strip().lower()
    if key not in ORDERS:
        return {"error": f"no order on file for '{order_id}'"}
    return {"dispatched": True, "order_id": order_id}


def get_delay_status(order_id):
    key = order_id.strip().lower()
    if key not in DELAY_LOG:
        return {"error": f"no delay log for '{order_id}'"}
    return DELAY_LOG[key]


def check_traffic_report(order_id):
    key = order_id.strip().lower()
    if key not in TRAFFIC_REPORTS:
        return {"error": f"no traffic report for '{order_id}'"}
    return TRAFFIC_REPORTS[key]


def check_weather_conditions(order_id):
    key = order_id.strip().lower()
    if key not in WEATHER_CONDITIONS:
        return {"error": f"no weather data for '{order_id}'"}
    return WEATHER_CONDITIONS[key]


def check_driver_checkin(order_id):
    key = order_id.strip().lower()
    if key not in DRIVER_CHECKINS:
        return {"error": f"no check-in record for '{order_id}'"}
    return DRIVER_CHECKINS[key]


TOOL_IMPLS = {
    "verify_delivery_address": verify_delivery_address,
    "calculate_route": calculate_route,
    "dispatch_driver": dispatch_driver,
    "get_delay_status": get_delay_status,
    "check_traffic_report": check_traffic_report,
    "check_weather_conditions": check_weather_conditions,
    "check_driver_checkin": check_driver_checkin,
}

FIXED_DISPATCH_ORDER = ["verify_delivery_address", "calculate_route", "dispatch_driver"]


def run_fixed_dispatch(order_id, max_replans=2, correction=None):
    current_id = order_id
    for attempt in range(max_replans + 1):
        sections = {}
        failed = False
        for tool_name in FIXED_DISPATCH_ORDER:
            result = TOOL_IMPLS[tool_name](current_id)
            if "error" in result:
                failed = True
                break
            sections[tool_name] = result
        if not failed:
            return sections, attempt
        if correction is None or attempt >= max_replans:
            return None, attempt
        current_id = correction
    return None, max_replans


def decide_next_delay_check(history):
    if not history:
        return "get_delay_status"
    last_tool, last_result = history[-1]
    if last_tool == "get_delay_status":
        notes = last_result.get("notes", "").lower()
        if "traffic" in notes:
            return "check_traffic_report"
        if "weather" in notes or "icy" in notes:
            return "check_weather_conditions"
        if "checked in" in notes or "check-in" in notes:
            return "check_driver_checkin"
        return None
    return None


def run_emergent_diagnosis(order_id, max_iterations=3):
    history = []
    for _ in range(max_iterations):
        next_tool = decide_next_delay_check(history)
        if next_tool is None:
            break
        result = TOOL_IMPLS[next_tool](order_id)
        history.append((next_tool, result))
    return history


def classify_task_planning_mode(later_steps_depend_on_earlier_results, steps_known_in_advance):
    if later_steps_depend_on_earlier_results:
        return "emergent"
    if steps_known_in_advance:
        return "fixed"
    return "emergent"


def self_check():
    results = []

    sections, attempts = run_fixed_dispatch("ord-101")
    ok = (
        sections is not None
        and attempts == 0
        and sections.get("dispatch_driver", {}).get("dispatched") is True
    )
    results.append(("Fixed dispatch succeeds on a valid order, 0 re-plans", ok))

    sections2, attempts2 = run_fixed_dispatch("ord-999", correction="ord-101")
    ok = sections2 is not None and attempts2 == 1
    results.append(("Fixed dispatch recovers after 1 re-plan with a correction", ok))

    sections3, attempts3 = run_fixed_dispatch("ord-888", correction=None, max_replans=2)
    ok = sections3 is None and attempts3 <= 2
    results.append(("Fixed dispatch gives up cleanly with no correction available", ok))

    hist1 = run_emergent_diagnosis("ord-201")
    ok = len(hist1) == 2 and hist1[1][0] == "check_traffic_report"
    results.append(("Emergent diagnosis follows the traffic branch", ok))

    hist2 = run_emergent_diagnosis("ord-202")
    ok = len(hist2) == 2 and hist2[1][0] == "check_weather_conditions"
    results.append(("Emergent diagnosis follows the weather branch", ok))

    hist3 = run_emergent_diagnosis("ord-203")
    ok = len(hist3) == 2 and hist3[1][0] == "check_driver_checkin"
    results.append(("Emergent diagnosis follows the driver check-in branch", ok))

    ok = (
        classify_task_planning_mode(False, True) == "fixed"
        and classify_task_planning_mode(True, False) == "emergent"
        and classify_task_planning_mode(True, True) == "emergent"
    )
    results.append(("Planning-mode heuristic classifies all three cases correctly", ok))

    print("Chapter 2 Project -- Structural Self-Check (SOLUTION)")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
