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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
