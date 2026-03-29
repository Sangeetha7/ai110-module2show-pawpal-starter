from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Pet:
    name: str
    species_or_breed: str
    age: int
    notes: str = ""

    def update_info(self, details: dict) -> None:
        """Updates the pet's basic information."""
        pass

@dataclass
class Task:
    name: str
    duration: int  # in minutes
    priority: int  # e.g., 1 (High), 2 (Medium), 3 (Low)
    description: str = ""

    def edit_task(self, new_duration: int, new_priority: int) -> None:
        """Updates the time or importance of the task."""
        pass

class Owner:
    def __init__(self, name: str, available_time: int):
        self.name: str = name
        self.available_time: int = available_time  # in minutes
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Links a new pet to the owner."""
        pass

    def update_available_time(self, minutes: int) -> None:
        """Changes the amount of time the owner has available."""
        pass

class Scheduler:
    def __init__(self):
        self.task_list: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Adds a new care task to the pool."""
        pass

    def remove_task(self, task: Task) -> None:
        """Deletes a task from the pool."""
        pass

    def generate_plan(self, available_time: int) -> dict:
        """
        Sorts tasks by priority, fits them into the available_time,
        and returns a structured schedule/plan.
        """
        pass
