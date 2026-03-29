# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Show a prioritized daily schedule

## Features

The core logic of PawPal+ is driven by a custom `Scheduler` architecture. Key implemented features include:

- **Chronological Sorting**: A lightweight algorithm that parses `"HH:MM"` string formats to accurately reorganize all daily care tasks into a chronological timeline for the user.
- **Priority-Driven Task Scheduling**: Given an owner's maximum availability threshold (in minutes), the system generates a tailored plan by prioritizing the most crucial tasks (Priority 1) before secondary tasks. It fits as many in as possible (a greedy algorithm approach) while cleanly compiling a list of omitted tasks that run over the time limit.
- **Automated Recurring Tasks**: A smart task generation engine. When an owner checks off a task tagged as "Daily" or "Weekly", the system calculates `datetime` delta offsets and automatically spawns the next occurrence directly onto the correct pet's ongoing task log.
- **Conflict & Overlap Warnings**: A proactive verification layer that prevents "double-booking" by continuously parsing the pending tasks list and rendering warnings if multiple tasks on an owner's plate share an identical start time.
- **Robust Object Orientated Design**: Clean implementation of Python `dataclasses` managing structured relationships linking limited `Owner` availability capacity, to specific `Pet` profiles, directly to individual `Task` objects utilizing UUIDs for tracking capability.
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling
    
* **Chronological Sorting**: Tasks now include a time attribute (HH:MM format). The Scheduler can sort the owner's itinerary chronologically for better readability.
* **Task Filtering**: Tasks can be filtered dynamically by specific pets or by completion status using an optimized single-pass algorithm.
* **Automated Recurring Tasks**: Tasks now track a due_date. When a Daily or Weekly task is marked as complete, the scheduler automatically calculates the next occurrence using Python's datetime module and spawns a new instance.
* **Lightweight Conflict Detection**: The system actively scans the uncompleted tasks and generates friendly warnings if multiple tasks are scheduled for the exact same time slot, alerting the owner without crashing the application.

## Testing PawPal+
    Confidence Level - 5
    python -m unittest tests/test_pawpal.py
    The test suite currently includes 5 test cases that cover the core functionality of the PawPal system:

    Task Completion (test_task_completion): Verifies that calling mark_complete() properly updates a task's status to is_completed = True.
    Task Addition (test_task_addition): Ensures that when a task is added to a pet using add_task(), the pet's task count increases and the task's pet_name attribute is automatically updated to match the pet.
    Sorting Correctness (test_sorting_correctness): Checks that the Scheduler successfully organizes a list of tasks in strictly chronological sequence based on their "HH:MM" times.
    Recurrence Logic (test_recurrence_logic): Validates the automated scheduling engine; when a "Daily" recurring task is completed, it verifies that the original is marked complete and precisely one new task is instantiated for the following day.
    Conflict Detection (test_conflict_detection): Confirms that if multiple incomplete tasks are scheduled closely at the exact same chronological time, the Scheduler properly detects the overlap and generates a conflict warning.
 
## Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src="/course_images/ai110/website_desc.png"></a>
<a href="/course_images/ai110/profile.png" target="_blank"><img src="/course_images/ai110/profile.png"></a>
<a href="/course_images/ai110/tasks.png" target="_blank"><img src="/course_images/ai110/tasks.png"></a>
<a href="/course_images/ai110/schedule.png" target="_blank"><img src="/course_images/ai110/schedule.png"></a>
