import streamlit as st

# Import the backend logic classes
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**!

Managing a pet (or several!) on a tight schedule can be difficult. This app uses a custom-built 
greedy scheduling algorithm to prioritize your most urgent pet tasks within the time you have available today.
"""
)

with st.expander("How it works", expanded=True):
    st.markdown(
        """
1. **Set Capacity**: Define your available free time for the day.
2. **Add Pets & Tasks**: Create pets and assign them care tasks (like walks or grooming). Set task durations, time slots, and a priority level (1 is highest).
3. **Smart Scheduling**: The system warns you of time conflicts, sorts tasks chronologically, and finally builds a daily plan summarizing what fits and what needs to be omitted!
"""
    )

st.divider()

st.subheader("1. Profile Settings (Owner & Pet)")

# Initialize session state for our objects
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=60)
    
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

col_owner, col_pet = st.columns(2)

with col_owner:
    st.markdown("#### Owner Info")
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
    available_time = st.number_input("Available Time (minutes per day)", min_value=10, max_value=480, value=st.session_state.owner.available_time)
    
    # Update owner info on change
    if owner_name != st.session_state.owner.name:
        st.session_state.owner.name = owner_name
    if available_time != st.session_state.owner.available_time:
        st.session_state.owner.update_available_time(available_time)

with col_pet:
    st.markdown("#### Add a Pet")
    new_pet_name = st.text_input("New Pet Name", value="")
    new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
    new_pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
    
    if st.button("Add Pet"):
        if new_pet_name:
            new_pet = Pet(name=new_pet_name, species_or_breed=new_pet_species, age=new_pet_age)
            # Call the logic method from Phase 2
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet: {new_pet_name}!")
        else:
            st.error("Please provide a name for the pet.")

# Show current pets
if st.session_state.owner.pets:
    st.write("**Current Pets:**")
    for p in st.session_state.owner.pets:
        st.write(f"- {p.name} ({p.species_or_breed}, {p.age} yrs)")

st.divider()

st.subheader("2. Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col_4_pet, col_5_time = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_level = st.selectbox("Priority", ["High (1)", "Medium (2)", "Low (3)"])
    # Map priority text to our integer system
    priority_mapping = {"High (1)": 1, "Medium (2)": 2, "Low (3)": 3}
    priority = priority_mapping[priority_level]
with col_4_pet:
    # Select which pet this task is for
    if not st.session_state.owner.pets:
        st.warning("Add a pet first!")
        pet_options = []
    else:
        pet_options = [p.name for p in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("For Pet:", pet_options)
with col_5_time:
    time_val = st.text_input("Time (HH:MM)", value="12:00")

if st.button("Add task"):
    if not selected_pet_name:
        st.error("You must select a pet for this task.")
    else:
        # Create the Task object
        new_task = Task(name=task_title, duration=int(duration), priority=priority, time=time_val)
        
        # Find the pet and add it using the phase 2 logic
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet_name:
                pet.add_task(new_task)
                st.success(f"Added {task_title} to {pet.name} at {time_val}!")
                break

all_current_tasks = st.session_state.owner.get_all_tasks()

if all_current_tasks:
    st.write("Current pending tasks:")
    
    # Check for scheduling conflicts
    conflicts = st.session_state.scheduler.detect_conflicts(all_current_tasks)
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
            
    # Sort tasks chronologically using the Scheduler logic
    sorted_tasks = st.session_state.scheduler.sort_by_time(all_current_tasks)
    
    # Format for clean display using a Streamlit table
    task_data = [{"Time": t.time, "Task": t.name, "Pet": t.pet_name, "Duration": f"{t.duration}m", "Priority": t.priority} for t in sorted_tasks]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("3. Build Schedule")
st.caption("Let the system build your daily plan.")

if st.button("Generate schedule"):
    if not all_current_tasks:
        st.warning("Please add some tasks first!")
    else:
        # Call the logic method from Phase 2
        plan = st.session_state.scheduler.generate_plan(st.session_state.owner)
        
        st.write("### 📅 Today's Plan")
        st.info(plan["reasoning"])
        
        col_success, col_omitted = st.columns(2)
        with col_success:
            st.success(f"**Scheduled ({plan['total_duration']} mins)**")
            for t in plan["scheduled_tasks"]:
                st.write(f"- ✅ **{t.name}** for {t.pet_name} ({t.duration}m)")
                
        with col_omitted:
            st.error(f"**Omitted (Not enough time)**")
            if not plan["omitted_tasks"]:
                st.write("None! Everything fits.")
            for t in plan["omitted_tasks"]:
                st.write(f"- ❌ **{t.name}** for {t.pet_name} ({t.duration}m)")
