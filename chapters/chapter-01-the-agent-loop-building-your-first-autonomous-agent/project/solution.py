"""
Chapter 1 Project (L1 Guided): Build and Trace a Minimal Agent Loop
REFERENCE SOLUTION. See starter.py's module docstring for the full
scenario (Wavecrest Marina's SlipBot). Running this file directly
passes all 4 structural self-checks.
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
    def __init__(self, behavior="normal"):
        self.behavior = behavior

    def step(self, iteration, slip_id, last_observation):
        if self.behavior == "runaway":
            return FakeMessage(tool_calls=[FakeToolCall("check_slip_availability", {"slip_id": slip_id})])
        if iteration == 1:
            return FakeMessage(tool_calls=[FakeToolCall("check_slip_availability", {"slip_id": slip_id})])
        if last_observation and last_observation.get("available"):
            return FakeMessage(content=f"Slip {slip_id.upper()} is available.")
        elif last_observation and "reason" in last_observation:
            return FakeMessage(content=f"Slip {slip_id.upper()} is not available: {last_observation['reason']}.")
        else:
            return FakeMessage(content=f"I couldn't find slip {slip_id.upper()} on file.")


def run_agent(slip_id, model, max_iterations=4):
    trace = []
    last_observation = None

    for i in range(1, max_iterations + 1):
        msg = model.step(i, slip_id, last_observation)

        if not msg.tool_calls:
            return msg.content, trace

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            fn = TOOL_IMPLS[call.function.name]
            result = fn(**args)
            trace.append((call.function.name, args, result))
            last_observation = result

    return None, trace


def self_check():
    results = []

    answer, trace = run_agent("a12", FakeModel("normal"))
    ok = answer is not None and "available" in answer.lower() and "not available" not in answer.lower()
    results.append(("Resolves an available slip with a real final answer", ok))

    ok = len(trace) == 1 and trace[0][0] == "check_slip_availability" and trace[0][2].get("available") is True
    results.append(("Traces exactly one real tool call with the right result", ok))

    answer2, _ = run_agent("b04", FakeModel("normal"))
    ok = answer2 is not None and "reserved" in answer2.lower()
    results.append(("Surfaces the real reason for an unavailable slip", ok))

    answer3, trace3 = run_agent("a12", FakeModel("runaway"), max_iterations=3)
    ok = answer3 is None and len(trace3) == 3
    results.append(("Guard halts a runaway model at max_iterations", ok))

    print("Chapter 1 Project -- Structural Self-Check (SOLUTION)")
    print("=" * 55)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 55)
    print(f"{passed}/{len(results)} checks passed")


if __name__ == "__main__":
    self_check()
