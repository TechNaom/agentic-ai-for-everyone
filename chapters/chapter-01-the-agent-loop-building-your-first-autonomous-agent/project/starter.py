"""
Chapter 1 Project (L1 Guided): Build and Trace a Minimal Agent Loop
Scenario: Wavecrest Marina wants "SlipBot," an agent that answers
questions about boat-slip availability using one tool,
check_slip_availability(slip_id).

This project is gradable offline with a deterministic FAKE model
(FakeModel below) so it runs the same way everywhere, including CI with
no Ollama installed. See README.md for how to swap in the real
`openai`-against-Ollama client from the lesson once this passes, for
the full live experience.

How to run:
    python3 starter.py
It prints a structural self-check: does your loop correctly perceive,
reason, act, observe, and guard against a model that never stops.
"""

import json


SLIP_DATA = {
    "a12": {"available": True, "length_ft": 30},
    "b04": {"available": False, "reason": "reserved through Sunday"},
    "c19": {"available": True, "length_ft": 45},
}


def check_slip_availability(slip_id):
    key = slip_id.strip().lower()
    if key not in SLIP_DATA:
        return {"error": f"no slip on file named '{slip_id}'"}
    return SLIP_DATA[key]


TOOL_IMPLS = {"check_slip_availability": check_slip_availability}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_slip_availability",
            "description": "Look up whether a named boat slip is currently available.",
            "parameters": {
                "type": "object",
                "properties": {"slip_id": {"type": "string"}},
                "required": ["slip_id"],
            },
        },
    }
]


class FakeToolCall:
    def __init__(self, name, args):
        self.id = f"call_{name}"
        self.function = type("F", (), {"name": name, "arguments": json.dumps(args)})


class FakeMessage:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class FakeModel:
    """
    A deterministic stand-in for a real model, so this project is
    gradable the same way every time, everywhere. It plays two
    different scripted behaviors depending on `behavior`:
      - "normal": on iteration 1, requests check_slip_availability for
        whatever slip_id is in the user message; on iteration 2,
        returns a final answer using the observation from iteration 1.
      - "runaway": ALWAYS requests another tool call and never returns
        a final answer -- this is what your guard has to survive.
    """

    def __init__(self, behavior="normal"):
        self.behavior = behavior

    def step(self, iteration, slip_id, last_observation):
        if self.behavior == "runaway":
            return FakeMessage(tool_calls=[FakeToolCall("check_slip_availability", {"slip_id": slip_id})])
        if iteration == 1:
            return FakeMessage(tool_calls=[FakeToolCall("check_slip_availability", {"slip_id": slip_id})])
        # iteration 2+: answer using whatever was observed
        if last_observation and last_observation.get("available"):
            return FakeMessage(content=f"Slip {slip_id.upper()} is available.")
        elif last_observation and "reason" in last_observation:
            return FakeMessage(content=f"Slip {slip_id.upper()} is not available: {last_observation['reason']}.")
        else:
            return FakeMessage(content=f"I couldn't find slip {slip_id.upper()} on file.")


def run_agent(slip_id, model, max_iterations=4):
    """
    Complete this function so it runs the perception -> reasoning ->
    action -> observation loop against `model` (a FakeModel instance),
    using TOOL_IMPLS to execute any requested tool call, and returns
    the model's final answer text -- or None if max_iterations is
    reached without one.

    Track a `trace` list of (tool_name, args, result) tuples for every
    action taken, and return (final_answer, trace) as a 2-tuple.
    """
    trace = []
    last_observation = None

    for i in range(1, max_iterations + 1):
        msg = model.step(i, slip_id, last_observation)

        # TODO 1: if msg.tool_calls is empty, this is the final answer.
        # Return (msg.content, trace) right here.

        # TODO 2: otherwise, for each call in msg.tool_calls:
        #   - parse call.function.arguments with json.loads
        #   - look up and run the matching function from TOOL_IMPLS
        #   - append (call.function.name, args, result) to trace
        #   - set last_observation = result (used by the FakeModel's
        #     next .step() call to decide its answer)
        pass

    # TODO 3: the guard. If the loop above finishes all max_iterations
    # without ever returning, return (None, trace) here.
    return None, trace


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    results = []

    # Check 1: normal behavior resolves a real, available slip.
    answer, trace = run_agent("a12", FakeModel("normal"))
    ok = answer is not None and "available" in answer.lower() and "not available" not in answer.lower()
    results.append(("Resolves an available slip with a real final answer", ok))

    # Check 2: the tool was actually called and traced.
    ok = len(trace) == 1 and trace[0][0] == "check_slip_availability" and trace[0][2].get("available") is True
    results.append(("Traces exactly one real tool call with the right result", ok))

    # Check 3: normal behavior on an unavailable slip mentions the reason.
    answer2, _ = run_agent("b04", FakeModel("normal"))
    ok = answer2 is not None and "reserved" in answer2.lower()
    results.append(("Surfaces the real reason for an unavailable slip", ok))

    # Check 4: the guard actually halts a runaway model.
    answer3, trace3 = run_agent("a12", FakeModel("runaway"), max_iterations=3)
    ok = answer3 is None and len(trace3) == 3
    results.append(("Guard halts a runaway model at max_iterations", ok))

    print("Chapter 1 Project -- Structural Self-Check")
    print("=" * 55)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 55)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
