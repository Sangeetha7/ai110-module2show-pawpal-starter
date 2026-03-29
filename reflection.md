# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    Three core actions that the user should be able to perform are enter owner and pet information, manage care tasks, generate and view a daily plan. 
- What classes did you include, and what responsibilities did you assign to each?
   
- What classes did you include, and what responsibilities did you assign to each?
    I included four classes: Owner, Pet, CareTask and SchedulePlanner. 
    * **Owner**: Responsible for holding the user's information and their availability
    * **Pet**: Responsible for storing basic details about the pet
    * **Task**: Responsible for tracking the specific details of a task, like the duration and priority level.
    * **Scheduler**: Responsible for taking a list of CareTask objects and the Owner's time constraint, and applying logic to generate a prioritized daily schedule that fits within the available time.
       
**b. Design changes**

- Did your design change during implementation?
    Yes, my design changed  when I asked AI to review the skeleton 
- If yes, describe at least one change and why you made it.
    Missing Relationships:
        In the initial design, tasks are not linked to specific pets. I changed this because if an owner has two pets, the scheduler will not know which pet the task is for
        The scheduler is disconnected form the owner. It should either take an Owner object when it's initialized, or pass the Owner object to generate_plan(owner) so the scheduler has access to the owner's time constraints and pet list directly.
    
    Logic Bottlenecks:
        Missing Unique IDs - Managing UI state across reloads can be tricky. If the user edits or removes a task, how to find exactly that task in a list? (e.g., if there are two tasks named "Walk")
        Task State Tracking: The current Task has a duration and priority, but no way to know if it has been completed.
        When sorting tasks, the logic needs to know if 1 means High or if bigger numbers mean higher priority
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    Time Limit (available_time): The absolute maximum number of minutes the owner can spend on pet care today.
    Task Priority (priority): Tasks are ranked (1 = High, 2 = Medium, 3 = Low).
    Task Duration (duration): How long each task takes.
    Time of Day (time): The scheduled "HH:MM" slot for the task
- How did you decide which constraints mattered most?
    Priority was made the most important sorting factor because basic needs must take precedence over optional activities. Total time is the bounding contraint because a owner cannot exceed their available time. If priorities are tied, Duration is used as a tie-breaker.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    The scheduler uses a simple greedy approach. It just sorts by priority and duration, adding tasks down the list until it runs out of time. It trades off mathematical time optimization for speed and simplicity
- Why is that tradeoff reasonable for this scenario?
    It's reasonable because pet owners care more about making sure the most urgent tasks are completed rather than utilizing every single free minute with low-priority tasks
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI for design, reviewing initial skeleton structure, identifying missing relationships and test drafting.
- What kinds of prompts or questions were most helpful?
    Asking specific questions work best.  For eg. What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    When building the initial UML class diagram, the AI suggested generating the entire Python codebase fully fleshed out immediately based on that design. I explicitly rejected this and forced it to only generate the stubs without log, so I could implement the scheduling algorithm step-by-step.
- How did you evaluate or verify what the AI suggested?
    I verified the AI's suggestions conceptually against the assignment requirements first. When it wrote the incrementally requested chunks of main.py, I traced the code block before committing it to ensure it was prioritizing by Priority first and duration second, rather than the other way around
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested five main things - basic task completion, adding tasks to a pet, sorting tasks chronologically by time, the daily recurrence logic, and conflict detection for tasks sharing the exact same time slot.
- Why were these tests important?
    They ensure the core logic of the app actually works. If sorting is broken, the user's schedule is useless. If recurrence fails, the user has to manually re-enter tasks every day. Conflict detection is important so owners don't doublebook themselves.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    I'm pretty confident in the core features since the unit tests run and pass cleanly. The basic priority sorting and greedy algorithm seem solid for everyday use.
- What edge cases would you test next if you had more time?
    I'd want to test what happens if a user enters a weird time format (like "9AM" instead of "09:00"), how the recurrence handles end-of-month or leap-year date math, and whether the system completely breaks down if a pet has zero tasks assigned but the scheduler tries to evaluate them anyway.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisfied with how the Scheduler operates as a stateless brain to ingest Owner and Pet structures and output a prioritized daily plan. Adding the detect_conflicts logic was also a satisfying feature that adds real user value.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I would improve the time handling. Currently, the system relies heavily on `"HH:MM"` strings which can cause bugs with formatting. I would upgrade all time fields to use Python's built-in `datetime.time` objects for more robust validation and sorting.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    I learned that AI is incredibly useful as a sounding board during the design phase. By having AI review the initial UML structure, it identified missing relationships (like tying Tasks to Pets and linking the Scheduler to the Owner's time constraint) early on, which prevented major refactoring headaches later during implementation.
