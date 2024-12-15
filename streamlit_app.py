import streamlit as st
from datetime import datetime, timedelta, timezone

# Fixed Task Rotation Pattern
TASK_PATTERN = [
    {"Zimmer 1": "🗑️ Garbage & Kitchen", "Zimmer 2": "✨ Free", "Zimmer 3": "✨ Free"},  # Week 1
    {"Zimmer 1": "✨ Free", "Zimmer 2": "🗑️ Garbage & Kitchen", "Zimmer 3": "🚿 Bathroom"},  # Week 2
    {"Zimmer 1": "✨ Free", "Zimmer 2": "✨ Free", "Zimmer 3": "🗑️ Garbage & Kitchen"},  # Week 3
    {"Zimmer 1": "🗑️ Garbage & Kitchen", "Zimmer 2": "🚿 Bathroom", "Zimmer 3": "✨ Free"},  # Week 4
]

# Germany Timezone Offset (UTC+1)
GERMAN_TIMEZONE_OFFSET = 1  # UTC+1

# Function to get the tasks for the current week
def get_current_week_tasks(start_date):
    """
    Calculates tasks for the current Monday-Sunday week based on a 4-week rotation.
    :param start_date: Start date of Week 1 (Dec 9, 2023).
    :return: Tasks for the current week and its date range.
    """
    # Adjust for German time (UTC+1)
    today = datetime.now(timezone.utc) + timedelta(hours=GERMAN_TIMEZONE_OFFSET)

    # Align today to the current Monday
    this_monday = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    
    # Calculate weeks passed since the start date
    weeks_since_start = (this_monday - start_date).days // 7

    # Determine the current week in the 4-week cycle
    current_week_index = weeks_since_start % len(TASK_PATTERN)

    # Calculate the current week's range
    week_start = this_monday
    week_end = this_monday + timedelta(days=6)

    # Return tasks for the current week and its date range
    return TASK_PATTERN[current_week_index], week_start.strftime("%b %d"), week_end.strftime("%b %d")

# Streamlit UI Configuration
st.set_page_config(page_title="Cleaning Duty Tracker", layout="centered")

# Injecting Computer Modern Font CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=CMU+Serif&display=swap');

    html, body, [class*="css"] {
        font-family: 'CMU Serif', serif;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Header
st.title("🧹 Cleaning Duty Tracker")
st.markdown("### Ludwigstraße 57")
#st.write("Efficiently track and rotate cleaning duties. 🤝")

# Define the start date of Week 1 (Dec 9, 2023)
START_DATE = datetime(2023, 12, 9, tzinfo=timezone.utc) + timedelta(hours=GERMAN_TIMEZONE_OFFSET)

# Get the tasks for the current week
current_tasks, week_start, week_end = get_current_week_tasks(START_DATE)

# Display the current week's tasks
st.write(" ##### This Week's Assignments")
st.write(f"**Week: {week_start} - {week_end}**")
for room, task in current_tasks.items():
    st.write(f"**{room}**: {task}")

# Footer with WhatsApp logo
st.markdown("---")
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" 
             width="25" style="margin-right: 10px;">
        <a href="https://chat.whatsapp.com/JlYvcKdVrVbFxC6p5dCDZc" target="_blank" 
           style="text-decoration: none; color: #25D366; font-weight: bold;">
           Join the WhatsApp Group
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


