"""
Chapter 6 Exercises: Guardrails and Safety for Autonomous Agents
Scenario: Amberlock Self-Storage, a fictional self-storage facility. Its
operations agent, DispatchBot, can check unit status, issue refunds, remotely
unlock a unit (a physical security override), and run a facility
"reconciliation script." Every one of those except the status check is a
real, consequential action a guardrail has to bound.

This is a fresh scenario, deliberately different from the lesson's Millbrook
Credit Union/LedgerBot hook. The point is applying this chapter's guardrail
concepts to a system you haven't seen before.

How to run:
    python3 starter.py
It prints a score report. Fill in each # TODO, re-run, and watch your score
climb toward the total (19 points across 8 tasks).
"""

REFUND_APPROVAL_THRESHOLD = 200.00
ALLOWED_TOOLS = {"check_unit_status", "issue_refund", "unlock_unit", "run_facility_script"}
SANDBOX_ALLOWED_PREFIXES = ["generate_occupancy_report", "list_units"]
SANDBOX_DENYLIST_SUBSTRINGS = [";", "&&", "|", "`", "$(", "rm ", "curl ", "wget ", "sudo ", ">", "<"]


# ---------------------------------------------------------------------------
# Task 1: Map five DispatchBot facts to the single BEST-matching guardrail
# concept from this list:
#   "tool allowlist", "human-approval checkpoint", "sandboxed tool execution",
#   "action budget", "fail-safe default deny"
#
# Fact A: DispatchBot tried to call a tool name that was never actually given
#         to it, and the check refused it before anything ran.
# Fact B: A large refund cannot be issued until a human explicitly confirms
#         it, and DispatchBot's own dispatch function genuinely pauses and
#         waits for that confirmation instead of proceeding anyway.
# Fact C: run_facility_script()'s command is checked against an explicit
#         allowlist/denylist of command shapes before it's ever executed.
# Fact D: DispatchBot's session is capped at a fixed number of total
#         dispatched actions, regardless of how many reasoning steps it took.
# Fact E: When the approval service itself times out and raises an error,
#         DispatchBot treats that as "not approved," never as "approved by
#         default."
# ---------------------------------------------------------------------------

TASK_1_ANSWERS = {
    "fact_a": None,  # TODO 1
    "fact_b": None,  # TODO 2
    "fact_c": None,  # TODO 3
    "fact_d": None,  # TODO 4
    "fact_e": None,  # TODO 5
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
# If a guardrail's approval check FAILS OPEN (treats an error asking for
# approval as "approved") instead of failing safe, does an unapproved
# high-risk action actually executing become MORE likely, LESS likely, or
# have NO EFFECT?

TASK_2_ANSWER = None  # TODO 6: "MORE likely" | "LESS likely" | "NO EFFECT"


def score_exercise_2():
    return (1 if TASK_2_ANSWER == "MORE likely" else 0), 1


# ---------------------------------------------------------------------------
# Task 3 (production-gear): tool allowlist check.
# ---------------------------------------------------------------------------
def is_tool_allowed(tool_name):
    # TODO 7: return True if tool_name is in ALLOWED_TOOLS, else False.
    return False


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
    # TODO 8: return True if tool_name == "issue_refund" and
    # args.get("amount", 0) >= REFUND_APPROVAL_THRESHOLD, OR if
    # tool_name == "unlock_unit" (unlocking ALWAYS needs approval).
    # Otherwise return False.
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
    """
    1. If not is_tool_allowed(tool_name): return {"dispatched": False,
       "reason": "not on allowlist"}.
    2. If tool_name == "run_facility_script" and
       is_command_sandboxed_ok(args.get("command", "")) is False: return
       {"dispatched": False, "reason": "sandbox refused command"}.
    3. If needs_approval(tool_name, args): call approve_fn(tool_name, args)
       inside a try/except -- on ANY exception, treat as NOT approved (fail
       safe). If not approved, return {"dispatched": False, "reason":
       "approval declined or not granted"}.
    4. Otherwise return {"dispatched": True, "reason": "ok"}.
    """
    # TODO 9: implement the composed dispatch logic described above.
    return {"dispatched": True, "reason": "ok"}


def score_exercise_5():
    points = 0
    def deny(t, a):
        return False
    def approve(t, a):
        return True

    if dispatch_action("issue_refund", {"amount": 50}, deny)["dispatched"] is True:
        points += 1
    if dispatch_action("issue_refund", {"amount": 250}, deny)["dispatched"] is False:
        points += 1
    if dispatch_action("unlock_unit", {"unit_id": "U-12"}, approve)["dispatched"] is True:
        points += 1
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
# Name this failure using this chapter's exact vocabulary.

TASK_6_ANSWER = None  # TODO 10: fill in the exact concept string


def score_exercise_6():
    return (1 if TASK_6_ANSWER == "system-prompt-only guardrail" else 0), 1


# ---------------------------------------------------------------------------
# Task 7 (production-gear): fail-safe default deny.
# ---------------------------------------------------------------------------
def safe_approve(tool_name, args, approve_fn):
    """
    Call approve_fn(tool_name, args) inside a try/except. Return its
    (boolean-coerced) result on success. On ANY exception, return False --
    fail safe, never fail open.
    """
    # TODO 11: implement the fail-safe wrapper described above.
    return True


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
    concepts_touched = set(v for v in TASK_1_ANSWERS.values() if v)
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
