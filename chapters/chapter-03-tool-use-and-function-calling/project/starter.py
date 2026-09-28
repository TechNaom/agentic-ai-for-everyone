"""
Chapter 3 Project (Chapter Mini-Project): Robust Tool Use for RepairBot
Scenario: Kestrel Appliance Service, a fictional home-appliance repair
dispatcher, wants RepairBot to combine this chapter's three pillars in
one build: tool selection among overlapping candidates, timeout-vs-
malformed-output-aware failure handling, and outcome verification for
a tool that always "succeeds."

RepairBot has four tools:
  - check_warranty_status(appliance_id): cheap, decisive -- if the
    warranty is expired, that alone explains why a repair visit is
    needed (no diagnostic required).
  - run_diagnostic(appliance_id): a real (simulated) diagnostic call
    that can hang past a configured budget, the same TIMEOUT failure
    type as the lesson's run_line_diagnostic.
  - schedule_repair_visit(ticket_id): "succeeds" unconditionally --
    like the lesson's restart_modem, a clean success dict that doesn't
    guarantee the underlying problem is actually fixed.
  - get_repair_ticket_status(ticket_id): independent evidence of
    whether a ticket is actually completed, used to verify the real
    outcome of scheduling a repair.

This project is gradable offline with deterministic fixtures (no live
model call needed), so it runs the same way everywhere, including CI
with no Ollama installed -- the same grading policy as this chapter's
exercises/practice and Chapter 2's own project.

How to run:
    python3 starter.py
It prints a structural self-check: 7 checks across tool selection,
timeout-retry handling, and outcome verification.
"""

import concurrent.futures


# ---------------------------------------------------------------------------
# Fixtures and tools -- given, no need to edit below this line.
# ---------------------------------------------------------------------------

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
    """Given -- the same bounded-wait wrapper the lesson built."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(fn, **kwargs)
        try:
            return {"ok": True, "result": future.result(timeout=budget_seconds)}
        except concurrent.futures.TimeoutError:
            return {"ok": False, "failure_type": "timeout"}


# ---------------------------------------------------------------------------
# TODO 1: the tool-selection function -- check the cheapest, most decisive
# signal (warranty status) BEFORE the more expensive diagnostic call.
# ---------------------------------------------------------------------------
def diagnose_appliance_issue(appliance_id):
    """
    Check check_warranty_status(appliance_id) first. If its "status" is
    "expired", that alone explains the need for a repair visit --
    return ("check_warranty_status", that result) WITHOUT calling
    run_diagnostic at all. Otherwise, return ("run_diagnostic",
    run_diagnostic(appliance_id)).
    """
    # TODO 1: implement the selection logic described above.
    return "run_diagnostic", run_diagnostic(appliance_id)


# ---------------------------------------------------------------------------
# TODO 2: the timeout-retry policy for run_diagnostic.
# ---------------------------------------------------------------------------
def run_diagnostic_with_retry(appliance_id, simulate_hang=False, max_retries=2, budget_seconds=1):
    """
    For attempt in range(max_retries + 1): call call_with_timeout()
    against run_diagnostic with kwargs {"appliance_id": appliance_id,
    "_simulate_hang": simulate_hang and attempt == 0} and budget_seconds.
    If the outcome is ok, return (outcome["result"], attempt). If every
    attempt times out, return (None, max_retries).
    """
    # TODO 2: implement the retry loop described above.
    return None, max_retries


# ---------------------------------------------------------------------------
# TODO 3: the outcome-verification function for schedule_repair_visit,
# which always "succeeds" without meaning the appliance is actually fixed.
# ---------------------------------------------------------------------------
def verify_repair_outcome(ticket_id):
    """
    Call schedule_repair_visit(ticket_id), then check independent
    evidence with get_repair_ticket_status(ticket_id). Set resolved =
    True only if that status's "status" field equals "completed".
    Return {"schedule_result": schedule_result, "resolved": resolved}.
    """
    schedule_result = schedule_repair_visit(ticket_id)
    # TODO 3: look up the real ticket status and set `resolved`
    # correctly, then return the dict described above.
    return {"schedule_result": schedule_result, "resolved": False}


# ---------------------------------------------------------------------------
# Given -- composes the three functions above; no need to edit.
# ---------------------------------------------------------------------------
def full_service_flow(appliance_id, ticket_id, simulate_hang=False):
    tool, diag_result = diagnose_appliance_issue(appliance_id)
    if tool == "run_diagnostic":
        diag_result, _attempts = run_diagnostic_with_retry(appliance_id, simulate_hang=simulate_hang)
    outcome = verify_repair_outcome(ticket_id)
    return {"root_cause_tool": tool, "diagnosis": diag_result, "resolved": outcome["resolved"]}


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

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

    print("Chapter 3 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
