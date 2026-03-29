from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    print("--- Setting up PawPal+ Demo ---")
    
    # 1. Create an Owner with limited time
    # Let's say Alice only has 45 minutes today for pet care
    owner = Owner("Alice", available_time=45)
    print(f"Created Owner: {owner.name} with {owner.available_time} mins available.")

    # 2. Create at least two Pets
    dog = Pet(name="Buddy", species_or_breed="Golden Retriever", age=3)
    cat = Pet(name="Whiskers", species_or_breed="Siamese", age=2)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    print(f"Added pets: {dog.name} the {dog.species_or_breed} and {cat.name} the {cat.species_or_breed}.")

    # 3. Add at least three Tasks with different times/priorities
    # Priority 1 (High), 2 (Medium), 3 (Low)
    task1 = Task(name="Morning Walk", duration=30, priority=1, description="Walk around the park.")
    task2 = Task(name="Feed Buddy", duration=10, priority=1, description="Give morning kibble.")
    task3 = Task(name="Play with laser pointer", duration=20, priority=2, description="Cat playtime.")
    task4 = Task(name="Brush fur", duration=15, priority=3, description="Grooming.")

    # Add tasks directly to their respective pets
    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task4)
    cat.add_task(task3)

    # 4. Generate the Schedule
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)

    # 5. Print a "Today's Schedule" to the terminal
    print("\n" + "="*40)
    print(f"          TODAY'S SCHEDULE FOR {owner.name.upper()}")
    print("="*40)
    
    print("\n✅ SCHEDULED TASKS:")
    for t in plan["scheduled_tasks"]:
        print(f"  - {t.name} ({t.duration} mins) [Priority: {t.priority}, Pet: {t.pet_name}]")
        
    print("\n❌ OMITTED TASKS (Not enough time):")
    for t in plan["omitted_tasks"]:
        print(f"  - {t.name} ({t.duration} mins) [Priority: {t.priority}, Pet: {t.pet_name}]")
        
    print("\n" + "-"*40)
    print(f"Total Time Scheduled: {plan['total_duration']} mins")
    print(f"Time Remaining: {owner.available_time - plan['total_duration']} mins")
    print(f"Reasoning:\n{plan['reasoning']}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()