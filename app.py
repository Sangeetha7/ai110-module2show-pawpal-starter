import streamlit as st

# Import the backend logic classes
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
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

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_level = st.selectbox("Priority", ["High (1)", "Medium (2)", "Low (3)"])
    # Map priority text to our integer system
    priority_mapping = {"High (1)": 1, "Medium (2)": 2, "Low (3)": 3}
    priority = priority_mapping[priority_level]
with col4:
    # Select which pet this task is for
    if not st.session_state.owner.pets:
        st.warning("Add a pet first!")
        pet_options = []
    else:
        pet_options = [p.name for p in st.session_state.owner.pets]
    
    selected_pet_name = st.selectbox("For Pet:", pet_options)

if st.button("Add task"):
    if not selected_pet_name:
        st.error("You must select a pet for this task.")
    else:
        # Create the Task object
        new_task = Task(name=task_title, duration=int(duration), priority=priority)
        
        # Find the pet and add it using the phase 2 logic
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet_name:
                pet.add_task(new_task)
                st.success(f"Added {task_title} to {pet.name}!")
                break

all_current_tasks = st.session_state.owner.get_all_tasks()

if all_current_tasks:
    st.write("Current pending tasks:")
    # Format for clean display
    task_data = [{"Task": t.name, "Pet": t.pet_name, "Duration": f"{t.duration}m", "Priority": t.priority} for t in all_current_tasks]
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
