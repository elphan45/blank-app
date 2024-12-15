import streamlit as st
from datetime import datetime, timedelta
import json

# File for persistent storage of tasks
DATA_FILE = "task_data.json"
REFERENCE_DATE = "2023-12-09"  # Starting from Dec 9, 2023
BATHROOM_START_DATE = "2023-12-16"  # First bathroom duty (Zimmer 3)

# Initialize data with default values
initial_data = {
    "last_bathroom_zimmer": "Zimmer 3"  # Initial state
}

# Load or create task data
try:
    with open(DATA_FILE, "r") as file:
        task_data = json.load(file)
        if "last_bathroom_zimmer" not in task_data:
            task_data["last_bathroom_zimmer"] = initial_data["last_bathroom_zimmer"]
except FileNotFoundError:
    task_data = initial_data.copy()
    with open(DATA_FILE, "w") as file:
        json.dump(task_data, file)

# Custom CSS for styling
st.markdown("""
<style>
    .task-card {
        padding: 20px;
        margin: 12px 0;
        border: 1px solid #333;
        border-radius: 8px;
    }
    
    .progress-container {
        width: 100%;
        height: 6px;
        background-color: #333;
        border-radius: 3px;
        margin: 8px 0;
    }
    
    .progress-bar {
        height: 100%;
        background-color: #4f8bf9;
        border-radius: 3px;
    }
    
    .task-text {
        font-size: 16px;
        line-height: 1.5;
    }
    
    .footer-container {
        padding: 2rem 0;
        text-align: center;
        background-color: rgba(49, 51, 63, 0.4);
        border-radius: 10px;
        margin-top: 2rem;
    }
    
    .social-button {
        display: inline-flex;
        align-items: center;
        background-color: #25D366;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.3s ease;
        font-weight: 500;
        margin: 10px 0;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .button-icon {
        width: 20px;
        height: 20px;
        margin-right: 12px;
    }
    
    .footer-text {
        margin-bottom: 1rem;
        color: #888;
        font-size: 0.9rem;
    }
    
    .footer-divider {
        width: 50px;
        height: 2px;
        background-color: #4f8bf9;
        margin: 1rem auto;
        border-radius: 1px;
    }
</style>
""", unsafe_allow_html=True)

def generate_schedule(start_date, num_weeks):
    rooms = ["Zimmer 1", "Zimmer 2", "Zimmer 3"]
    schedule = []

    last_garbage_kitchen = -1  # Index of the last room assigned Garbage & Kitchen
    last_bathroom = 2  # Bathroom starts with Zimmer 3 in Week 2

    for week in range(num_weeks):
        week_schedule = {room: "Free" for room in rooms}

        # Assign Garbage & Kitchen
        last_garbage_kitchen = (last_garbage_kitchen + 1) % 3
        garbage_kitchen_room = rooms[last_garbage_kitchen]
        week_schedule[garbage_kitchen_room] = "Garbage & Kitchen Cleaning"

        # Assign Bathroom biweekly
        if week % 2 == 1:  # Bathroom starts Week 2 (1-based index)
            bathroom_room = (last_bathroom + 1) % 3

            if bathroom_room == last_garbage_kitchen:
                bathroom_room = (bathroom_room + 1) % 3  # Resolve conflict

            week_schedule[rooms[bathroom_room]] = "Bathroom Cleaning"
            last_bathroom = bathroom_room

        schedule.append(week_schedule)

    return schedule

def calculate_week_dates(reference_date, week_offset):
    start_of_week = reference_date + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

# Inputs
st.title("Task Manager")
st.markdown("Ludwigstraße 57")

num_weeks = st.number_input("Number of weeks to generate the schedule:", min_value=1, max_value=52, value=4, step=1)
current_date = datetime.now()
reference_date = datetime.strptime(REFERENCE_DATE, "%Y-%m-%d")
week_offset = ((current_date - reference_date).days // 7)

schedule = generate_schedule(reference_date, num_weeks)

# Display current and next week's tasks
current_week_index = week_offset % num_weeks

st.markdown(f"### Current Week: {calculate_week_dates(reference_date, week_offset)[0].strftime('%d.%m.%Y')} - {calculate_week_dates(reference_date, week_offset)[1].strftime('%d.%m.%Y')}")
for room, task in schedule[current_week_index].items():
    st.markdown(f"- **{room}**: {task}")

with st.expander("Next Week"):
    next_week_index = (current_week_index + 1) % num_weeks
    st.markdown(f"### Next Week: {calculate_week_dates(reference_date, week_offset + 1)[0].strftime('%d.%m.%Y')} - {calculate_week_dates(reference_date, week_offset + 1)[1].strftime('%d.%m.%Y')}")
    for room, task in schedule[next_week_index].items():
        st.markdown(f"- **{room}**: {task}")

# Modern Footer
st.markdown("""
<div class="footer-container">
    <p class="footer-text">Connect with your housemates</p>
    <div class="footer-divider"></div>
    <a href="https://chat.whatsapp.com/JlYvcKdVrVbFxC6p5dCDZc" 
       class="social-button" 
       target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" 
             class="button-icon" 
             alt="WhatsApp">
        Join WhatsApp Group
    </a>
</div>
""", unsafe_allow_html=True)
