import unittest
import sys
import os
import datetime

# Ensure the parent directory is in the path so we can import pawpal_system
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Task, Pet, Scheduler

class TestPawPalSystem(unittest.TestCase):
    
    def test_task_completion(self):
        """Verify that calling mark_complete() actually changes the task's status."""
        task = Task(name="Brush Teeth", duration=5, priority=2)
        
        # Verify initial state is False
        self.assertFalse(task.is_completed)
        
        # Call the method
        task.mark_complete()
        
        # Verify it changed to True
        self.assertTrue(task.is_completed)

    def test_task_addition(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        pet = Pet(name="Rex", species_or_breed="German Shepherd", age=4)
        task = Task(name="Evening Walk", duration=30, priority=1)
        
        # Capture the initial count
        initial_count = len(pet.tasks)
        
        # Add the task
        pet.add_task(task)
        
        # Verify the count increased by 1
        self.assertEqual(len(pet.tasks), initial_count + 1)
        
        # Verify the task is actually in the pet's list
        self.assertIn(task, pet.tasks)
        
        # Verify the task's pet_name attribute was updated automatically
        self.assertEqual(task.pet_name, "Rex")

    def test_sorting_correctness(self):
        """Verify tasks are returned in chronological order."""
        scheduler = Scheduler()
        t1 = Task(name="Morning Walk", duration=30, priority=1, time="08:00")
        t2 = Task(name="Evening Walk", duration=30, priority=1, time="18:00")
        t3 = Task(name="Lunch Feeding", duration=15, priority=1, time="12:00")
        
        unsorted = [t2, t1, t3]
        sorted_tasks = scheduler.sort_by_time(unsorted)
        
        self.assertEqual(sorted_tasks[0].name, "Morning Walk")
        self.assertEqual(sorted_tasks[1].name, "Lunch Feeding")
        self.assertEqual(sorted_tasks[2].name, "Evening Walk")

    def test_recurrence_logic(self):
        """Confirm that marking a daily task complete creates a new task for the following day."""
        scheduler = Scheduler()
        pet = Pet(name="Buddy", species_or_breed="Golden Retriever", age=3)
        today = datetime.date.today()
        task = Task(name="Give Medication", duration=5, priority=1, time="10:00", frequency="Daily", due_date=today)
        pet.add_task(task)
        
        self.assertFalse(task.is_completed)
        self.assertEqual(len(pet.tasks), 1)
        
        # Complete the task
        scheduler.complete_task(pet, task)
        
        # The original task should be marked complete
        self.assertTrue(task.is_completed)
        
        # A new recurring instance should be spawned
        self.assertEqual(len(pet.tasks), 2)
        new_task = pet.tasks[1]
        self.assertFalse(new_task.is_completed)
        self.assertEqual(new_task.due_date, today + datetime.timedelta(days=1))

    def test_conflict_detection(self):
        """Verify that the Scheduler flags duplicate times."""
        scheduler = Scheduler()
        t1 = Task(name="Checkup", duration=30, priority=1, time="12:00")
        t2 = Task(name="Grooming", duration=60, priority=2, time="12:00")
        t3 = Task(name="Playtime", duration=15, priority=3, time="14:00")
        
        warnings = scheduler.detect_conflicts([t1, t2, t3])
        
        self.assertEqual(len(warnings), 1)
        self.assertIn("Conflict detected at 12:00!", warnings[0])

if __name__ == '__main__':
    unittest.main()