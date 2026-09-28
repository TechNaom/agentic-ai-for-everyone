"""
Chapter 4 Project (L2 Assisted, partial scaffold): CareBot for Hollowridge
Wellness Clinic

This is this course's numbered L2 Assisted project (per
docs/curriculum/CURRICULUM_MAP.md's project ladder: "Build a multi-tool
agent with memory and a reflection step for a provided scenario, partial
scaffold, ships after Ch. 4, extended through Ch. 5-6's reflection/
guardrail material"). Chapter 4 shipped the multi-tool-plus-memory half
of that description in full. Chapter 5 ("Reflection and Self-
Correction") taught the general reflection mechanism, applied here in
TODO 4. NOW that Chapter 6 ("Guardrails and Safety for Autonomous
Agents") has taught guardrails, TODO 5 asks you to wire
guardrail_check_booking() (given below) into run_visit_session() BEFORE
schedule_followup() is dispatched -- a hard, enforced check, not a
message revised after the fact.

Scenario: Hollowridge Wellness Clinic wants CareBot, a scheduling and
intake assistant with three tools plus a persisted long-term memory
store for patient conditions/preferences that must correctly inform a
LATER, separate visit.

How to run:
    python3 starter.py
It prints a structural self-check: 10 checks. Fill in the 5 # TODOs and
watch checks pass.
"""

import json
import os


MEMORY_PATH = "carebot_memory_starter.json"

APPOINTMENT_SLOTS = {"2026-10-05": True, "2026-10-06": False}
PATIENTS = {"pt-88": {"name": "Jordan"}, "pt-99": {"name": "Sam"}}


def check_appointment_slot(date):
    return {"date": date, "available": APPOINTMENT_SLOTS.get(date, False)}


def get_patient_profile(patient_id):
    return PATIENTS.get(patient_id, {"error": f"no patient on file for '{patient_id}'"})


def schedule_followup(patient_id, date):
    return {"scheduled": True, "patient_id": patient_id, "date": date}


# ---------------------------------------------------------------------------
# Given -- persisted long-term memory, no need to edit.
# ---------------------------------------------------------------------------
class MemoryStore:
    def __init__(self, path=MEMORY_PATH):
        self.path = path

    def _load_all(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r") as f:
            return json.load(f)

    def get(self, patient_id):
        return self._load_all().get(patient_id, {"conditions": [], "preferences": []})

    def _save_all(self, all_memory):
        with open(self.path, "w") as f:
            json.dump(all_memory, f, indent=2)

    def add_condition(self, patient_id, note):
        all_memory = self._load_all()
        facts = all_memory.get(patient_id, {"conditions": [], "preferences": []})
        facts["conditions"].append(note)
        all_memory[patient_id] = facts
        self._save_all(all_memory)

    def add_preference(self, patient_id, note):
        all_memory = self._load_all()
        facts = all_memory.get(patient_id, {"conditions": [], "preferences": []})
        facts["preferences"].append(note)
        all_memory[patient_id] = facts
        self._save_all(all_memory)


def is_promote_worthy(message_text):
    text = message_text.lower()
    condition_words = ["allerg", "condition", "diagnos", "latex", "asthma"]
    preference_words = ["prefer", "female provider", "male provider", "morning", "afternoon"]
    if any(w in text for w in condition_words):
        return "condition"
    if any(w in text for w in preference_words):
        return "preference"
    return None


# ---------------------------------------------------------------------------
# Given -- a blocking-condition policy check. Not a TODO: this is the same
# helper Chapter 5's own lesson built for a fresh scenario (Briarcliff Bike
# Rentals/BikeBot); reuse it rather than re-deriving keyword matching here.
# ---------------------------------------------------------------------------
BLOCKING_CONDITION_PHRASES = [
    "chest pain", "can't breathe", "cannot breathe", "severe allergic reaction",
    "unresolved", "suicidal", "difficulty breathing",
]


def is_blocking_condition(text):
    t = text.lower()
    return any(p in t for p in BLOCKING_CONDITION_PHRASES)


# ---------------------------------------------------------------------------
# Given -- a guardrail check. Not a TODO body itself (see TODO 5 in
# run_visit_session below for where you wire this in), but read it: this
# is a HARD, enforced check at the tool-dispatch boundary, called BEFORE
# schedule_followup() -- not a message revised after the fact the way
# Chapter 5's reflect_on_response() (TODO 4 below) works.
# ---------------------------------------------------------------------------
def guardrail_check_booking(current_facts, human_approved=True):
    """Returns {"allowed": bool, "blocking": [...]}. A blocking condition
    on file requires human_approved=True before the booking is allowed to
    proceed; with no blocking condition, booking is always allowed."""
    conditions = current_facts.get("conditions", [])
    blocking = [c for c in conditions if is_blocking_condition(c)]
    if blocking and not human_approved:
        return {"allowed": False, "blocking": blocking}
    return {"allowed": True, "blocking": blocking}


# ---------------------------------------------------------------------------
# TODO 4 (new this chapter): implement reflection for real.
# ---------------------------------------------------------------------------
def reflect_on_response(draft_response, context):
    """
    context is {"facts": <patient's current facts dict>, "tool_trace": [...]}.

    1. Get context["facts"]["conditions"] and context["tool_trace"].
    2. blocking = the subset of conditions where is_blocking_condition(c) is
       True.
    3. booked = True if tool_trace contains a ("schedule_followup", result)
       entry where result["scheduled"] is True.
    4. If blocking is non-empty AND booked is True, return a revised
       response that mentions the blocking condition(s) (joined with "; ")
       and the phrase "clinical review" instead of a routine confirmation --
       do NOT just return draft_response unchanged in this case.
    5. Otherwise, return draft_response unchanged.
    """
    # TODO 4: implement the self-critique-and-revise logic described above.
    return draft_response


# ---------------------------------------------------------------------------
# TODO 1: merge persisted facts into a fresh session's working memory.
# ---------------------------------------------------------------------------
def build_working_context(patient_id, store):
    """
    Look up store.get(patient_id). If facts["conditions"] is non-empty,
    append a {"role": "system", "content": ...} message to working_memory
    listing them (joined with "; "), prefixed "Known conditions
    (persisted): ". Do the same for facts["preferences"] with the prefix
    "Known preferences (persisted): ". Return (working_memory, facts).
    """
    working_memory = []
    # TODO 1: implement the merge logic described above.
    facts = store.get(patient_id)
    return working_memory, facts


# ---------------------------------------------------------------------------
# TODO 2: promote any promote-worthy fact stated THIS visit to the
# persisted store before the session ends.
# ---------------------------------------------------------------------------
def promote_worthy_and_persist(patient_id, user_messages, store):
    """
    For each text in user_messages, classify it with is_promote_worthy().
    If "condition", call store.add_condition(patient_id, text). If
    "preference", call store.add_preference(patient_id, text). Return
    store.get(patient_id) at the end.
    """
    # TODO 2: implement the promotion loop described above.
    return store.get(patient_id)


# ---------------------------------------------------------------------------
# TODO 3: the composed multi-tool + memory visit flow, with the Chapter 5
# reflection hook already wired in as a labeled no-op call (given below --
# do not modify the reflect_on_response call itself, only the rest of the
# flow around it).
# ---------------------------------------------------------------------------
def run_visit_session(patient_id, store, user_messages, requested_date=None, human_approved=True):
    """
    1. working_memory, facts = build_working_context(patient_id, store)
    2. Append each text in user_messages to working_memory as a
       {"role": "user", ...} message.
    3. current_facts = promote_worthy_and_persist(patient_id,
       user_messages, store)
    4. tool_trace = []. If requested_date is given, call
       check_appointment_slot(requested_date), append ("check_appointment_
       slot", result) to tool_trace. If result["available"] is True:
       a. CHAPTER 6: call gate = guardrail_check_booking(current_facts,
          human_approved=human_approved) and append
          ("guardrail_check_booking", gate) to tool_trace.
       b. If gate["allowed"] is True, call schedule_followup(patient_id,
          requested_date) and append ("schedule_followup", booking) to
          tool_trace. Otherwise, do NOT call schedule_followup() -- set a
          local booking_held = True instead.
    5. Build draft_response:
       - If booking_held is True: return a response naming the blocking
         condition(s) (gate["blocking"], joined with "; ") and saying it
         needs care-team review before it can be scheduled -- do NOT say
         it's been booked.
       - Else if current_facts["conditions"] is non-empty: "Noted your
         history (<conditions joined with '; '>) -- I'll flag this for
         your provider."
       - Else: "Thanks, I've logged today's visit notes."
    6. final_response = reflect_on_response(draft_response,
       {"facts": current_facts, "tool_trace": tool_trace})  # given, do
       not change this line
    7. Append final_response to working_memory as an assistant message.
    8. Return {"working_memory": working_memory, "tool_trace": tool_trace,
       "persisted_facts": current_facts}
    """
    # TODO 3: implement the composed flow described above.
    # TODO 5 (new, Chapter 6): the guardrail_check_booking() call and the
    # booking_held branch described in step 4/5 above.
    return {"working_memory": [], "tool_trace": [], "persisted_facts": {"conditions": [], "preferences": []}}


# ---------------------------------------------------------------------------
# Structural self-check (do not need to edit below this line)
# ---------------------------------------------------------------------------

def self_check():
    if os.path.exists(MEMORY_PATH):
        os.remove(MEMORY_PATH)
    store = MemoryStore()
    results = []

    ctx0, facts0 = build_working_context("pt-88", store)
    ok = ctx0 == [] and facts0 == {"conditions": [], "preferences": []}
    results.append(("build_working_context returns empty for a never-seen patient", ok))

    visit1 = run_visit_session("pt-88", store, [
        "I'm allergic to latex, just so you know.",
        "Also I'd prefer a female provider going forward.",
    ], requested_date="2026-10-05")
    ok = any(t[0] == "schedule_followup" for t in visit1["tool_trace"])
    results.append(("visit 1 books the requested slot when available", ok))

    ok = "latex" in " ".join(visit1["persisted_facts"]["conditions"])
    results.append(("visit 1 promotes the allergy to persisted memory", ok))

    ok = "female provider" in " ".join(visit1["persisted_facts"]["preferences"])
    results.append(("visit 1 promotes the provider preference to persisted memory", ok))

    store2 = MemoryStore()  # a fresh instance -- simulates a truly separate process
    ctx2, facts2 = build_working_context("pt-88", store2)
    ok = len(ctx2) == 2 and "latex" in ctx2[0]["content"]
    results.append(("a fresh MemoryStore instance still sees visit 1's persisted facts", ok))

    visit2 = run_visit_session("pt-88", store2, ["Can we do 2026-10-06?"], requested_date="2026-10-06")
    ok = visit2["tool_trace"] and visit2["tool_trace"][0][1]["available"] is False and not any(t[0] == "schedule_followup" for t in visit2["tool_trace"])
    results.append(("visit 2 correctly does not book an unavailable slot", ok))

    # --- Chapter 5 additions: TODO 4, reflection actually catches and revises. ---
    ok = reflect_on_response("plain text", {"facts": {"conditions": []}, "tool_trace": []}) == "plain text"
    results.append(("reflect_on_response leaves a benign draft unchanged (Ch5)", ok))

    store3 = MemoryStore()
    visit3 = run_visit_session(
        "pt-99", store3,
        ["I have a new condition: chest pain that hasn't been evaluated yet."],
        requested_date="2026-10-05",
    )
    final_reply = visit3["working_memory"][-1]["content"] if visit3["working_memory"] else ""
    ok = (
        any(t[0] == "schedule_followup" for t in visit3["tool_trace"])
        and "clinical review" in final_reply
    )
    results.append(("reflect_on_response revises the draft when a blocking condition was booked (Ch5)", ok))

    # --- Chapter 6 additions: the guardrail actually stops/holds the
    # unsafe booking BEFORE dispatch, not just revises the message after. ---
    store4 = MemoryStore()
    visit4 = run_visit_session(
        "pt-99", store4,
        ["I have a new condition: severe allergic reaction, unresolved."],
        requested_date="2026-10-05",
        human_approved=False,
    )
    ok = (
        not any(t[0] == "schedule_followup" for t in visit4["tool_trace"])
        and any(t[0] == "guardrail_check_booking" and t[1]["allowed"] is False for t in visit4["tool_trace"])
    )
    results.append(("guardrail holds the booking for a blocking condition when not approved (Ch6)", ok))

    store5 = MemoryStore()
    visit5 = run_visit_session(
        "pt-99", store5,
        ["I have a new condition: severe allergic reaction, unresolved."],
        requested_date="2026-10-05",
        human_approved=True,
    )
    ok = (
        any(t[0] == "schedule_followup" for t in visit5["tool_trace"])
        and any(t[0] == "guardrail_check_booking" and t[1]["allowed"] is True for t in visit5["tool_trace"])
    )
    results.append(("guardrail allows the booking for the same condition once human-approved (Ch6)", ok))

    print("Chapter 4 Project -- Structural Self-Check")
    print("=" * 60)
    passed = 0
    for name, ok in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        passed += 1 if ok else 0
    print("=" * 60)
    print(f"{passed}/{len(results)} checks passed")
    if os.path.exists(MEMORY_PATH):
        os.remove(MEMORY_PATH)


if __name__ == "__main__":
    self_check()
