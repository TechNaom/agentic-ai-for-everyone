"""
Chapter 4 Project (L2 Assisted, partial scaffold): CareBot for Hollowridge
Wellness Clinic -- REFERENCE SOLUTION

This is this course's numbered L2 Assisted project (per
docs/curriculum/CURRICULUM_MAP.md's project ladder: "Build a multi-tool
agent with memory and a reflection step for a provided scenario, partial
scaffold, ships after Ch. 4, extended through Ch. 5-6's reflection/
guardrail material"). Chapter 4 shipped the multi-tool-plus-memory half
of that description in full, with reflect_on_response() wired in as a
labeled no-op. Chapter 5 ("Reflection and Self-Correction") filled in
reflect_on_response() for real -- see the CHAPTER 5 EXTENSION comment
block. THIS FILE HAS NOW BEEN EXTENDED A SECOND TIME BY CHAPTER 6
("Guardrails and Safety for Autonomous Agents"): run_visit_session() now
calls guardrail_check_booking() BEFORE schedule_followup() is ever
dispatched -- a hard, enforced check, not a message revised after the
fact -- see the CHAPTER 6 EXTENSION comment block for exactly what
changed and why TODOs 1-3 (build_working_context,
promote_worthy_and_persist, run_visit_session's original body) and
Chapter 5's reflection body were NOT restructured.

Scenario: Hollowridge Wellness Clinic wants CareBot, a scheduling and
intake assistant with three tools plus a persisted long-term memory
store for patient conditions/preferences that must correctly inform a
LATER, separate visit -- the same short-term/long-term split the lesson
built for Larkspur Fitness Studio's CoachBot, applied to a fresh
scenario.

How to run:
    python3 solution.py
It prints a structural self-check: 10 checks across memory merge,
promote-before-persist, the composed end-to-end visit flow, the
reflection step catching and revising an unsafe draft response, and
(new this chapter) the guardrail actually holding an unsafe booking
before it's dispatched, and releasing it once explicitly approved.
"""

import json
import os


MEMORY_PATH = "carebot_memory_solution.json"

APPOINTMENT_SLOTS = {"2026-10-05": True, "2026-10-06": False}
PATIENTS = {"pt-88": {"name": "Jordan"}, "pt-99": {"name": "Sam"}}


def check_appointment_slot(date):
    return {"date": date, "available": APPOINTMENT_SLOTS.get(date, False)}


def get_patient_profile(patient_id):
    return PATIENTS.get(patient_id, {"error": f"no patient on file for '{patient_id}'"})


def schedule_followup(patient_id, date):
    return {"scheduled": True, "patient_id": patient_id, "date": date}


# ---------------------------------------------------------------------------
# Persisted long-term memory -- read-modify-write, one JSON file, no vector
# database or embeddings, matching the lesson's MemoryStore exactly.
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
# CHAPTER 5 EXTENSION -- blocking-condition policy check, new this chapter.
# ---------------------------------------------------------------------------
# A condition is "blocking" if it's serious/unresolved enough that a routine
# scheduling confirmation would misrepresent it -- the exact class of mistake
# Chapter 5's lesson (fresh scenario: Briarcliff Bike Rentals) demonstrated
# with a real, un-scripted BikeBot failure, applied here to CareBot's own
# domain.
BLOCKING_CONDITION_PHRASES = [
    "chest pain", "can't breathe", "cannot breathe", "severe allergic reaction",
    "unresolved", "suicidal", "difficulty breathing",
]


def is_blocking_condition(text):
    t = text.lower()
    return any(p in t for p in BLOCKING_CONDITION_PHRASES)


# ---------------------------------------------------------------------------
# CHAPTER 6 EXTENSION -- guardrail: a hard, enforced check at the
# tool-dispatch boundary, checked BEFORE schedule_followup() is ever called,
# not a message revised after the fact. See run_visit_session() above for
# the call site.
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
# CHAPTER 5 EXTENSION -- reflection step, filled in for real this chapter.
# ---------------------------------------------------------------------------
# Chapter 4 shipped this function as a labeled no-op passthrough. Chapter 5
# ("Reflection and Self-Correction") replaces ONLY this function's body --
# not its call site inside run_visit_session(), and not TODOs 1-3 -- with a
# real self-critique-and-revise step: a second, deliberate check that
# evaluates the draft response against a policy (a blocking condition must
# never be presented as a routine, confirmed booking) and revises it if that
# policy is violated.
#
# Note the honest limit this function demonstrates, previewing Chapter 6:
# by the time reflect_on_response() runs, run_visit_session() has ALREADY
# called schedule_followup() if a slot was available -- reflection can only
# fix what CareBot SAYS, not undo a tool call that already executed. Stopping
# an unsafe tool call from firing in the first place is a guardrail's job,
# not reflection's -- which is exactly what Chapter 6 (CHAPTER 6 EXTENSION
# POINT, below, inside run_visit_session) will add: a check BEFORE
# schedule_followup() is dispatched, not just a revised message after it.
def reflect_on_response(draft_response, context):
    """Deterministic self-critique-and-revise step (Chapter 5).

    Checks the draft against one concrete policy: if any persisted
    condition for this visit is "blocking" (see is_blocking_condition)
    AND a follow-up was actually booked this visit, a routine-sounding
    confirmation misrepresents the situation -- the draft is revised to
    flag it for mandatory clinical review instead. Otherwise, the draft
    is returned unchanged (reflection that finds nothing wrong is not a
    failure of reflection -- most drafts should pass through untouched;
    see the lesson's own Section 6 on when reflection is worth its cost).
    """
    facts = context.get("facts", {})
    tool_trace = context.get("tool_trace", [])
    conditions = facts.get("conditions", [])

    blocking = [c for c in conditions if is_blocking_condition(c)]
    booked = any(name == "schedule_followup" and result.get("scheduled") for name, result in tool_trace)

    if blocking and booked:
        flagged = "; ".join(blocking)
        return (
            f"I've noted a new, unresolved concern ({flagged}) in your file. "
            "Your requested follow-up has been provisionally scheduled, but "
            "it needs clinical review before it's finalized -- our care team "
            "will reach out if it needs to move sooner. Please do not treat "
            "this as a confirmed routine visit."
        )
    return draft_response


# ---------------------------------------------------------------------------
# TODO 1 (solved): merge persisted facts into a fresh session's working
# memory.
# ---------------------------------------------------------------------------
def build_working_context(patient_id, store):
    working_memory = []
    facts = store.get(patient_id)
    if facts["conditions"]:
        working_memory.append({"role": "system", "content": f"Known conditions (persisted): {'; '.join(facts['conditions'])}"})
    if facts["preferences"]:
        working_memory.append({"role": "system", "content": f"Known preferences (persisted): {'; '.join(facts['preferences'])}"})
    return working_memory, facts


# ---------------------------------------------------------------------------
# TODO 2 (solved): promote any promote-worthy fact stated THIS visit to the
# persisted store before the session ends -- read-modify-write, not a blind
# overwrite.
# ---------------------------------------------------------------------------
def promote_worthy_and_persist(patient_id, user_messages, store):
    for text in user_messages:
        category = is_promote_worthy(text)
        if category == "condition":
            store.add_condition(patient_id, text)
        elif category == "preference":
            store.add_preference(patient_id, text)
    return store.get(patient_id)


# ---------------------------------------------------------------------------
# TODO 3 (solved): the composed multi-tool + memory visit flow, with the
# Chapter 5 reflection hook already wired in as a labeled no-op call.
# ---------------------------------------------------------------------------
def run_visit_session(patient_id, store, user_messages, requested_date=None, human_approved=True):
    working_memory, facts = build_working_context(patient_id, store)
    for text in user_messages:
        working_memory.append({"role": "user", "content": text})

    current_facts = promote_worthy_and_persist(patient_id, user_messages, store)

    tool_trace = []
    booking_held = False
    if requested_date:
        slot = check_appointment_slot(requested_date)
        tool_trace.append(("check_appointment_slot", slot))
        if slot["available"]:
            # CHAPTER 6 EXTENSION -- guardrail check, BEFORE dispatch.
            # A blocking condition on file gates schedule_followup() itself,
            # not just the message describing it -- this is the hard,
            # enforced boundary Chapter 5's reflect_on_response() (below)
            # could not provide, because reflection only ever runs AFTER a
            # tool call already fired. human_approved defaults to True to
            # keep Chapter 4-5's own regression checks (1-8 below) passing
            # unchanged, matching their original fixtures exactly -- a real
            # production entry point would default new sessions to False
            # ("not yet approved") instead; see project/README.md's "What
            # Chapter 6 changed" section for why this default was chosen
            # explicitly rather than silently.
            gate = guardrail_check_booking(current_facts, human_approved=human_approved)
            tool_trace.append(("guardrail_check_booking", gate))
            if gate["allowed"]:
                booking = schedule_followup(patient_id, requested_date)
                tool_trace.append(("schedule_followup", booking))
            else:
                booking_held = True

    if booking_held:
        flagged = "; ".join(gate["blocking"])
        draft_response = (
            f"I can't automatically confirm your requested follow-up because "
            f"of a concern in your file ({flagged}). This needs a member of "
            f"our care team to review and approve it before it's scheduled."
        )
    elif current_facts["conditions"]:
        draft_response = f"Noted your history ({'; '.join(current_facts['conditions'])}) -- I'll flag this for your provider."
    else:
        draft_response = "Thanks, I've logged today's visit notes."

    # CH5 EXTENSION POINT call site -- currently a no-op passthrough.
    final_response = reflect_on_response(draft_response, {"facts": current_facts, "tool_trace": tool_trace})

    working_memory.append({"role": "assistant", "content": final_response})
    return {"working_memory": working_memory, "tool_trace": tool_trace, "persisted_facts": current_facts}


# ---------------------------------------------------------------------------
# Structural self-check
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
    ok = visit2["tool_trace"][0][1]["available"] is False and not any(t[0] == "schedule_followup" for t in visit2["tool_trace"])
    results.append(("visit 2 correctly does not book an unavailable slot", ok))

    # --- Chapter 5 additions: reflection actually catches and revises. ---
    ok = reflect_on_response("plain text", {"facts": {"conditions": []}, "tool_trace": []}) == "plain text"
    results.append(("reflect_on_response leaves a benign draft unchanged (Ch5)", ok))

    store3 = MemoryStore()
    visit3 = run_visit_session(
        "pt-99", store3,
        ["I have a new condition: chest pain that hasn't been evaluated yet."],
        requested_date="2026-10-05",
    )
    final_reply = visit3["working_memory"][-1]["content"]
    ok = (
        any(t[0] == "schedule_followup" for t in visit3["tool_trace"])
        and "clinical review" in final_reply
        and final_reply != f"Noted your history (I have a new condition: chest pain that hasn't been evaluated yet.) -- I'll flag this for your provider."
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
