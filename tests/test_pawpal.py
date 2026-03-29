import unittest
import sys
import os

# Ensure the parent directory is in the path so we can import pawpal_system
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pawpal_system import Task, Pet

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

if __name__ == '__main__':
    unittest.main()