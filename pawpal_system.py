import uuid
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: int  # 1 = High, 2 = Medium, 3 = Low
    time: str = "12:00"  # HH:MM format
    pet_name: str = ""  # Automatically linked when added to a Pet
    description: str = ""
    frequency: str = "Daily"  # E.g., Daily, Weekly, Once
    is_completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def edit_task(self, new_duration: int, new_priority: int, new_description: str = None) -> None:
        """Updates the time, importance, or description of the task."""
        self.duration = new_duration
        self.priority = new_priority
        if new_description is not None:
            self.description = new_description

    def toggle_completion(self) -> None:
        """Flips the completion status of the task."""
        self.is_completed = not self.is_completed

    def mark_complete(self) -> None:
        """Marks the task as specifically completed."""
        self.is_completed = True

@dataclass
class Pet:
    name: str
    species_or_breed: str
    age: int
    notes: str = ""
    tasks: List[Task] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def update_info(self, details: dict) -> None:
        """Updates the pet's basic information based on a dictionary."""
        for key, value in details.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_task(self, task: Task) -> None:
        """Adds a task specifically for this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Removes a built-in task based on its ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

class Owner:
    def __init__(self, name: str, available_time: int):
        self.name: str = name
        self.available_time: int = available_time  # in minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Links a new pet to the owner."""
        self.pets.append(pet)

    def update_available_time(self, minutes: int) -> None:
        """Changes the amount of time the owner has available."""
        self.available_time = minutes

    def get_all_tasks(self) -> List[Task]:
        """Provides access to all tasks across all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_pet_by_id(self, pet_id: str) -> Optional[Pet]:
        """Helper to find a specific pet by their ID."""
        for pet in self.pets:
            if pet.id == pet_id:
                return pet
        return None

class Scheduler:
    # A stateless scheduler, essentially acting as the logic "Brain" 
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks chronologically based on their 'HH:MM' time attribute."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, tasks: List[Task], is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status or pet name."""
        filtered = tasks
        if is_completed is not None:
            filtered = [t for t in filtered if t.is_completed == is_completed]
        if pet_name:
            filtered = [t for t in filtered if t.pet_name == pet_name]
        return filtered
    
    def generate_plan(self, owner: Owner) -> dict:
        """
        Retrieves all tasks across pets, sorts them by priority (1 is highest),
        fits them into the owner's available_time, and returns a structured plan.
        """
        all_tasks = owner.get_all_tasks()
        
        # Sort uncompleted tasks first by priority (1 is best) 
        # and then by duration (shorter tasks are easier to fit in)
        uncompleted_tasks = [t for t in all_tasks if not t.is_completed]
        sorted_tasks = sorted(uncompleted_tasks, key=lambda t: (t.priority, t.duration))
        
        scheduled = []
        omitted = []
        time_remaining = owner.available_time
        
        for task in sorted_tasks:
            if task.duration <= time_remaining:
                scheduled.append(task)
                time_remaining -= task.duration
            else:
                omitted.append(task)
                
        reasoning = (
            f"Scheduled {len(scheduled)} tasks out of {len(uncompleted_tasks)} pending tasks, "
            f"prioritizing high-priority tasks (Priority 1 first) to fit within your {owner.available_time} minutes limit."
        )
        
        return {
            "scheduled_tasks": scheduled,
            "omitted_tasks": omitted,
            "total_duration": owner.available_time - time_remaining,
            "reasoning": reasoning
        }
