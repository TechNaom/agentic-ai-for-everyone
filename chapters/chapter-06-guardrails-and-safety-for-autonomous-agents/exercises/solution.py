"""
Chapter 6 Exercises: Guardrails and Safety for Autonomous Agents
Scenario: Amberlock Self-Storage, a fictional self-storage facility. Its
operations agent, DispatchBot, can check unit status, issue refunds, remotely
unlock a unit (a physical security override), and run a facility
"reconciliation script." Every one of those except the status check is a
real, consequential action a guardrail has to bound.

This is a fresh scenario, deliberately different from the lesson's Millbrook
Credit Union/LedgerBot hook. The point is applying this chapter's guardrail
concepts (allowlist, approval checkpoint, sandboxing, fail-safe default deny)
to a system you haven't seen before -- REFERENCE SOLUTION.

How to run:
    python3 solution.py
It prints a score report. Scores 18/18.
"""

REFUND_APPROVAL_THRESHOLD = 200.00
ALLOWED_TOOLS = {"check_unit_status", "issue_refund", "unlock_unit", "run_facility_script"}
SANDBOX_ALLOWED_PREFIXES = ["generate_occupancy_report", "list_units"]
SANDBOX_DENYLIST_SUBSTRINGS = [";", "&&", "|", "`", "$(", "rm ", "curl ", "wget ", "sudo ", ">", "<"]


# ---------------------------------------------------------------------------
# Task 1: Map five DispatchBot facts to the guardrail concept each is about.
# ---------------------------------------------------------------------------
TASK_1_ANSWERS = {
    "fact_a": "tool allowlist",
    "fact_b": "human-approval checkpoint",
    "fact_c": "sandboxed tool execution",
    "fact_d": "action budget",
    "fact_e": "fail-safe default deny",
}


def score_exercise_1():
    correct = {
        "fact_a": "tool allowlist",
        "fact_b": "human-approval checkpoint",
        "fact_c": "sandboxed tool execution",
        "fact_d": "action budget",
        "fact_e": "fail-safe default deny",
    }
    matched = sum(1 for k, v in correct.items() if TASK_1_ANSWERS.get(k) == v)
    return matched, len(correct)


# ---------------------------------------------------------------------------
# Task 2: Dependency reasoning.
# ---------------------------------------------------------------------------
TASK_2_ANSWER = "MORE likely"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): tool allowlist check.
# ---------------------------------------------------------------------------
def is_tool_allowed(tool_name):
    return tool_name in ALLOWED_TOOLS


def score_exercise_3():
    points = 0
    if is_tool_allowed("unlock_unit") is True:
        points += 1
    if is_tool_allowed("disable_facility_alarm") is False:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 4 (production-gear): approval-threshold check.
# ---------------------------------------------------------------------------
def needs_approval(tool_name, args):
    if tool_name == "issue_refund" and args.get("amount", 0) >= REFUND_APPROVAL_THRESHOLD:
        return True
    if tool_name == "unlock_unit":
        return True
    return False


def score_exercise_4():
    points = 0
    if needs_approval("issue_refund", {"amount": 50}) is False:
        points += 1
    if needs_approval("issue_refund", {"amount": 250}) is True:
        points += 1
    if needs_approval("unlock_unit", {"unit_id": "U-12"}) is True:
        points += 1
    return points, 3


# ---------------------------------------------------------------------------
# Task 5 (production-gear): dispatch_action -- compose allowlist, sandbox,
# and approval into one function, failing safe throughout.
# ---------------------------------------------------------------------------
def is_command_sandboxed_ok(command):
    if any(bad in command for bad in SANDBOX_DENYLIST_SUBSTRINGS):
        return False
    if not any(command.startswith(p) for p in SANDBOX_ALLOWED_PREFIXES):
        return False
    return True


def dispatch_action(tool_name, args, approve_fn):
    if not is_tool_allowed(tool_name):
        return {"dispatched": False, "reason": "not on allowlist"}
    if tool_name == "run_facility_script" and not is_command_sandboxed_ok(args.get("command", "")):
        return {"dispatched": False, "reason": "sandbox refused command"}
    if needs_approval(tool_name, args):
        try:
            approved = bool(approve_fn(tool_name, args))
        except Exception:
            approved = False  # fail safe
        if not approved:
            return {"dispatched": False, "reason": "approval declined or not granted"}
    return {"dispatched": True, "reason": "ok"}


def score_exercise_5():
    points = 0
    def deny(t, a):
        return False
    def approve(t, a):
        return True

    # Small refund, no approval needed -- dispatches.
    if dispatch_action("issue_refund", {"amount": 50}, deny)["dispatched"] is True:
        points += 1
    # Large refund, denied -- held.
    if dispatch_action("issue_refund", {"amount": 250}, deny)["dispatched"] is False:
        points += 1
    # Unlock, approved -- dispatches.
    if dispatch_action("unlock_unit", {"unit_id": "U-12"}, approve)["dispatched"] is True:
        points += 1
    # Dangerous facility script -- refused regardless of approval.
    if dispatch_action("run_facility_script", {"command": "rm -rf /data"}, approve)["dispatched"] is False:
        points += 1
    return points, 4


# ---------------------------------------------------------------------------
# Task 6 (production-gear): Diagnose a failure type from a trace.
# ---------------------------------------------------------------------------
# DispatchBot's system prompt said "never unlock a unit without asking the
# customer to confirm their identity first." An injected note inside a
# customer support ticket (read back as a tool result) told DispatchBot the
# identity check had "already been completed by phone" -- and DispatchBot
# unlocked the unit with no code anywhere actually verifying that claim.
# Name this failure using the exact concept string.
TASK_6_ANSWER = "system-prompt-only guardrail"


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "system-prompt-only guardrail" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): fail-safe default deny.
# ---------------------------------------------------------------------------
def safe_approve(tool_name, args, approve_fn):
    try:
        return bool(approve_fn(tool_name, args))
    except Exception:
        return False


def score_exercise_7():
    points = 0
    def flaky(t, a):
        raise RuntimeError("approval service down")
    if safe_approve("unlock_unit", {}, flaky) is False:
        points += 1
    if is_tool_allowed("wire_transfer_all_deposits") is False:
        points += 1
    return points, 2


# ---------------------------------------------------------------------------
# Task 8: Full-checklist completeness check.
# ---------------------------------------------------------------------------
def score_exercise_8():
    concepts_touched = set(TASK_1_ANSWERS.values())
    all_five = {
        "tool allowlist", "human-approval checkpoint", "sandboxed tool execution",
        "action budget", "fail-safe default deny",
    }
    points = 1 if concepts_touched == all_five else 0
    return points, 1


# ---------------------------------------------------------------------------
# Score report
# ---------------------------------------------------------------------------

def main():
    tasks = [
        ("Task 1: Map facts to guardrail concepts", score_exercise_1),
        ("Task 2: Dependency reasoning", score_exercise_2),
        ("Task 3 (production-gear): Tool allowlist check", score_exercise_3),
        ("Task 4 (production-gear): Approval-threshold check", score_exercise_4),
        ("Task 5 (production-gear): dispatch_action composition", score_exercise_5),
        ("Task 6 (production-gear): Failure diagnosis", score_exercise_6),
        ("Task 7 (production-gear): Fail-safe default deny", score_exercise_7),
        ("Task 8: Completeness check", score_exercise_8),
    ]
    total_earned, total_possible = 0, 0
    print("Chapter 6 Exercises -- Score Report")
    print("=" * 50)
    for name, fn in tasks:
        earned, possible = fn()
        total_earned += earned
        total_possible += possible
        print(f"{name}: {earned}/{possible}")
    print("=" * 50)
    print(f"TOTAL: {total_earned}/{total_possible}")


if __name__ == "__main__":
    main()
