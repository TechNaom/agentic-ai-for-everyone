"""
Chapter 4 Project (L2 Assisted, partial scaffold): CareBot for Hollowridge
Wellness Clinic

This is this course's numbered L2 Assisted project (per
docs/curriculum/CURRICULUM_MAP.md's project ladder: "Build a multi-tool
agent with memory and a reflection step for a provided scenario, partial
scaffold, ships after Ch. 4, extended through Ch. 5-6's reflection/
guardrail material"). Chapter 4 ships the multi-tool-plus-memory half of
that description in full; the reflection half is a clearly labeled,
no-op extension point (see reflect_on_response below) that Chapter 5
will fill in for real.

Scenario: Hollowridge Wellness Clinic wants CareBot, a scheduling and
intake assistant with three tools plus a persisted long-term memory
store for patient conditions/preferences that must correctly inform a
LATER, separate visit.

How to run:
    python3 starter.py
It prints a structural self-check: 7 checks. Fill in the 3 # TODOs and
watch checks pass.
"""

import json
import os


MEMORY_PATH = "carebot_memory_starter.json"

APPOINTMENT_SLOTS = {"2026-10-05": True, "2026-10-06": False}
PATIENTS = {"pt-88": {"name": "Jordan"}}


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
# Given -- CHAPTER 5 EXTENSION POINT. Do NOT implement reflection here --
# that is this course's Chapter 5 subject. Leave this exactly as it is;
# Chapter 5 will replace its body (not its call site in TODO 3) with a
# real self-critique-and-revise step.
# ---------------------------------------------------------------------------
def reflect_on_response(draft_response, context):
    """CH5 EXTENSION POINT: currently returns draft_response unchanged."""
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
def run_visit_session(patient_id, store, user_messages, requested_date=None):
    """
    1. working_memory, facts = build_working_context(patient_id, store)
    2. Append each text in user_messages to working_memory as a
       {"role": "user", ...} message.
    3. current_facts = promote_worthy_and_persist(patient_id,
       user_messages, store)
    4. tool_trace = []. If requested_date is given, call
       check_appointment_slot(requested_date), append ("check_appointment_
       slot", result) to tool_trace, and if result["available"] is True,
       call schedule_followup(patient_id, requested_date) and append
       ("schedule_followup", booking) to tool_trace too.
    5. Build draft_response: if current_facts["conditions"] is non-empty,
       "Noted your history (<conditions joined with '; '>) -- I'll flag
       this for your provider." else "Thanks, I've logged today's visit
       notes."
    6. final_response = reflect_on_response(draft_response,
       {"facts": current_facts, "tool_trace": tool_trace})  # given, do
       not change this line
    7. Append final_response to working_memory as an assistant message.
    8. Return {"working_memory": working_memory, "tool_trace": tool_trace,
       "persisted_facts": current_facts}
    """
    # TODO 3: implement the composed flow described above.
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

    ok = reflect_on_response("draft text", {"anything": True}) == "draft text"
    results.append(("reflect_on_response is a labeled no-op passthrough (Ch5 extension point)", ok))

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
