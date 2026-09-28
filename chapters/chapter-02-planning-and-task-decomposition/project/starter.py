"""
Chapter 2 Project (Chapter Mini-Project): Dual-Mode Planning for RouteBot
Scenario: Cobblestone Courier Co., a fictional local delivery service,
wants RouteBot to handle two kinds of task with two different planning
strategies -- exactly the chapter's own dual-mode PlanBot (Section 14),
applied to a fresh scenario you build yourself.

Task A -- Processing a new delivery order (fixed, up-front plan):
verify the delivery address, calculate the route, dispatch a driver.
Every order needs all three steps, in that exact order, and nothing
about the address changes whether the route is worth calculating --
this is a fixed-shape task, per Section 12's heuristic.

Task B -- Diagnosing a delayed delivery (emergent, one-step-at-a-time
plan): check the delay status first, and only THEN decide whether the
right follow-up is a traffic check, a weather check, or a driver
check-in -- because that choice depends entirely on what the delay
status notes actually say. This cannot be a fixed plan, the same
reason the lesson's stock-drop investigation needed emergent planning.

This project is gradable offline with deterministic fixtures (no live
model call needed), so it runs the same way everywhere, including CI
with no Ollama installed -- the same grading policy as this chapter's
exercises/practice and Chapter 1's own project. See README.md for how
to swap in the real `openai`-against-Ollama client from the lesson
once this passes, for the full live experience.

How to run:
    python3 starter.py
It prints a structural self-check: 7 checks across the fixed-plan
executor (with re-planning), the emergent decision function, and the
fixed-vs-emergent classification heuristic.
"""

import json


# ---------------------------------------------------------------------------
# Fixtures and tools -- given, no need to edit below this line.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# TODO 1: the fixed-plan executor, WITH a re-planning guard built in --
# mirrors the lesson's Section 13 run_fixed_plan_with_replan_guard, but as
# one combined function this time instead of two.
# ---------------------------------------------------------------------------
def run_fixed_dispatch(order_id, max_replans=2, correction=None):
    """
    Run FIXED_DISPATCH_ORDER's three tools in order against order_id.
    If any step returns an "error", and a `correction` order_id is
    available and max_replans hasn't been exhausted, rebuild the WHOLE
    plan with the corrected order_id and try again.

    Return (sections, attempts_used) where sections is a dict mapping
    each tool name to its real result, or (None, attempts_used) if
    every attempt failed (either no correction was given, or
    max_replans was exhausted).
    """
    # TODO 1: implement the fixed-plan-with-replan-guard loop.
    # For attempt in range(max_replans + 1):
    #   - run each tool in FIXED_DISPATCH_ORDER against the current
    #     order_id, collecting results into a `sections` dict
    #   - if any step returns a dict containing "error", stop this
    #     attempt early
    #   - if all three steps succeeded, return (sections, attempt)
    #   - otherwise, if correction is None or this was the last
    #     allowed attempt, return (None, attempt)
    #   - otherwise, set order_id = correction and try again
    return None, 0


# ---------------------------------------------------------------------------
# TODO 2: the emergent decision function for diagnosing a delay.
# ---------------------------------------------------------------------------
def decide_next_delay_check(history):
    """
    history is a list of (tool_name, result) tuples for what's been
    checked so far. Decide the SINGLE next tool to call:
      - with no history yet, return "get_delay_status"
      - after get_delay_status, look at the notes (lowercased):
          * if "traffic" is mentioned, return "check_traffic_report"
          * if "weather" or "icy" is mentioned, return "check_weather_conditions"
          * if "checked in" or "check-in" is mentioned, return "check_driver_checkin"
          * otherwise, return None (nothing more to check)
      - after any other step, return None (stop)
    """
    if not history:
        return "get_delay_status"
    # TODO 2: implement the branching described above.
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


# ---------------------------------------------------------------------------
# TODO 3: the fixed-vs-emergent decision heuristic itself (Section 12).
# ---------------------------------------------------------------------------
def classify_task_planning_mode(later_steps_depend_on_earlier_results, steps_known_in_advance):
    """
    Implement the same heuristic the lesson's classify_planning_mode
    used in Section 12:
      - if later_steps_depend_on_earlier_results is True, return "emergent"
      - elif steps_known_in_advance is True, return "fixed"
      - else return "emergent" (default when steps aren't knowable
        up front either)
    """
    # TODO 3: implement the three-branch heuristic described above.
    return None


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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

    print("Chapter 2 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
