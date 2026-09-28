"""
Chapter 3 Project (Chapter Mini-Project): Robust Tool Use for RepairBot
REFERENCE SOLUTION. See starter.py's module docstring for the full
scenario (Kestrel Appliance Service's RepairBot). Running this file
directly passes all 7 structural self-checks.
"""

import concurrent.futures


WARRANTY = {
    "appl-301": {"status": "expired"},
    "appl-402": {"status": "active"},
}
DIAGNOSTICS = {
    "appl-402": {"issue_code": "E4", "severity": "moderate"},
}
REPAIR_TICKETS = {
    "tk-701": {"status": "completed"},
    "tk-702": {"status": "scheduled"},
}


def check_warranty_status(appliance_id):
    key = appliance_id.strip().lower()
    if key not in WARRANTY:
        return {"error": f"no warranty record for '{appliance_id}'"}
    return WARRANTY[key]


def run_diagnostic(appliance_id, _simulate_hang=False):
    import time
    key = appliance_id.strip().lower()
    if _simulate_hang:
        time.sleep(3)
    if key not in DIAGNOSTICS:
        return {"error": f"no diagnostic data for '{appliance_id}'"}
    return DIAGNOSTICS[key]


def schedule_repair_visit(ticket_id):
    return {"scheduled": True, "ticket_id": ticket_id}


def get_repair_ticket_status(ticket_id):
    key = ticket_id.strip().lower()
    if key not in REPAIR_TICKETS:
        return {"error": f"no ticket on file for '{ticket_id}'"}
    return REPAIR_TICKETS[key]


def call_with_timeout(fn, kwargs, budget_seconds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(fn, **kwargs)
        try:
            return {"ok": True, "result": future.result(timeout=budget_seconds)}
        except concurrent.futures.TimeoutError:
            return {"ok": False, "failure_type": "timeout"}


def diagnose_appliance_issue(appliance_id):
    warranty = check_warranty_status(appliance_id)
    if warranty.get("status") == "expired":
        return "check_warranty_status", warranty
    return "run_diagnostic", run_diagnostic(appliance_id)


def run_diagnostic_with_retry(appliance_id, simulate_hang=False, max_retries=2, budget_seconds=1):
    for attempt in range(max_retries + 1):
        outcome = call_with_timeout(
            run_diagnostic,
            {"appliance_id": appliance_id, "_simulate_hang": simulate_hang and attempt == 0},
            budget_seconds,
        )
        if outcome["ok"]:
            return outcome["result"], attempt
    return None, max_retries


def verify_repair_outcome(ticket_id):
    schedule_result = schedule_repair_visit(ticket_id)
    status = get_repair_ticket_status(ticket_id)
    resolved = status.get("status") == "completed"
    return {"schedule_result": schedule_result, "resolved": resolved}


def full_service_flow(appliance_id, ticket_id, simulate_hang=False):
    tool, diag_result = diagnose_appliance_issue(appliance_id)
    if tool == "run_diagnostic":
        diag_result, _attempts = run_diagnostic_with_retry(appliance_id, simulate_hang=simulate_hang)
    outcome = verify_repair_outcome(ticket_id)
    return {"root_cause_tool": tool, "diagnosis": diag_result, "resolved": outcome["resolved"]}


def self_check():
    results = []

    tool1, result1 = diagnose_appliance_issue("appl-301")
    ok = tool1 == "check_warranty_status" and result1.get("status") == "expired"
    results.append(("diagnose_appliance_issue picks warranty when expired", ok))

    tool2, result2 = diagnose_appliance_issue("appl-402")
    ok = tool2 == "run_diagnostic" and "issue_code" in result2
    results.append(("diagnose_appliance_issue falls through to diagnostic when warranty active", ok))

    result3, attempts3 = run_diagnostic_with_retry("appl-402", simulate_hang=True)
    ok = result3 is not None and attempts3 == 1
    results.append(("run_diagnostic_with_retry recovers from a hang after 1 retry", ok))

    result4, attempts4 = run_diagnostic_with_retry("appl-402", simulate_hang=False)
    ok = result4 is not None and attempts4 == 0
    results.append(("run_diagnostic_with_retry succeeds immediately with no hang", ok))

    outcome5 = verify_repair_outcome("tk-701")
    ok = outcome5["resolved"] is True
    results.append(("verify_repair_outcome correctly reports a completed ticket as resolved", ok))

    outcome6 = verify_repair_outcome("tk-702")
    ok = outcome6["resolved"] is False
    results.append(("verify_repair_outcome correctly reports a scheduled-but-not-done ticket as unresolved", ok))

    flow = full_service_flow("appl-402", "tk-701", simulate_hang=True)
    ok = flow["root_cause_tool"] == "run_diagnostic" and flow["resolved"] is True
    results.append(("full_service_flow composes selection, retry, and outcome-check correctly end to end", ok))

    print("Chapter 3 Project -- Structural Self-Check (SOLUTION)")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
