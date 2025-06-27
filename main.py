import streamlit as st
import plotly.graph_objects as go

# Grade thresholds
grade_thresholds = {
    "Distinction/Max":100,
    "A*": 90,
    "A": 80,
    "B": 70,
    "C": 60,
    "D": 50,
    "E": 40,
    "U": 0
}

def detect_grade(percentage):
    for grade, threshold in grade_thresholds.items():
        if percentage >= threshold:
            return grade
    return "U"
st.set_page_config(page_title="PaperPilot's Grade Calculator", layout="centered")
st.markdown("""
<style>
body {
    background-color: #000000;
}
[data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
}
[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
    padding: 1.5rem;
    color: white;
}
.block-container {
    background-color: #000000 !important;
    color: white !important;
}
h1, h2, h3, h4, h5, h6, p, div, label {
    color: white !important;
}
.sidebar-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.6rem;
    color: white;
}
.section-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #AAAAAA;
    margin-top: 1.2rem;
    margin-bottom: 0.3rem;
}
.stNumberInput > div {
    display: flex;
    align-items: center;
    border-radius: 10px;
    overflow: hidden;
    background-color: #111111 !important;
    border: 1px solid #333333;
}
.stNumberInput input {
    padding: 0.3rem 0.6rem !important;
    font-size: 0.85rem;
    border: none !important;
    background-color: transparent !important;
    color: white !important;
}
.stNumberInput button {
    background-color: #222222 !important;
    color: white !important;
    border-left: 1px solid #333333;
    width: 2rem;
    height: 2rem;
    font-size: 1rem;
}
.stNumberInput button:hover {
    background-color: #333333 !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #111111 !important;
    color: white !important;
    border-radius: 8px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -------------- SIDEBAR --------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Input Data</div>', unsafe_allow_html=True)

    percentage = st.number_input("Your Percentage (%)", min_value=0, max_value=100, step=1, format="%d")
    current_grade = detect_grade(percentage)
    st.markdown(f'<div class="section-title">Grade: {current_grade}</div>', unsafe_allow_html=True)

    grade_keys = list(grade_thresholds.keys())
    grade_index = grade_keys.index(current_grade)
    next_grade = grade_keys[max(grade_index - 1, 0)]

    st.markdown('<div class="section-title">Grade Threshold Marks</div>', unsafe_allow_html=True)
    x1 = st.number_input(f"{current_grade} starts at:", key="x1", step=1, format="%d")
    x2 = st.number_input(f"{next_grade} starts at:", key="x2", step=1, format="%d")

    y1 = grade_thresholds[current_grade]
    y2 = grade_thresholds[next_grade]

    st.checkbox(f"{current_grade} = {y1}%, {next_grade} = {y2}%", value=True)

# ---------------- PLOT ----------------
slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 1
marks_at_percentage = x1 + (percentage - y1) / slope
x_vals = [x1, x2]
y_vals = [y1, y2]

# Colors for dark theme
color_line = "#3FAEFF"        # Cyan
color_percentage = "#A5FFBF"  # Mint green
color_marks = "#F7DC6F"       # Pale yellow
color_dot = "#FF7F7F"         # Coral

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x_vals, y=y_vals,
    mode='lines',
    name=f"{current_grade} → {next_grade}",
    line=dict(color=color_line, width=3)
))

fig.add_trace(go.Scatter(
    x=[x_vals[0], x_vals[-1]],
    y=[percentage, percentage],
    mode='lines',
    name=f"{percentage}%",
    line=dict(color=color_percentage, width=2, dash='dash')
))

fig.add_trace(go.Scatter(
    x=[marks_at_percentage, marks_at_percentage],
    y=[min(y1, y2) - 5, max(y1, y2) + 5],
    mode='lines',
    name=f"{round(marks_at_percentage)} Marks",
    line=dict(color=color_marks, width=2, dash='dash')
))

fig.add_trace(go.Scatter(
    x=[marks_at_percentage],
    y=[percentage],
    mode='markers+text',
    marker=dict(size=10, color=color_dot),
    text=[f"{round(marks_at_percentage)}"],
    textposition="top right",
    name="You"
))

fig.update_layout(
    title="CAIE RAW MARK CALCULATOR",
    xaxis_title="Marks",
    yaxis_title="Percentage (%)",
    plot_bgcolor="#000000",
    paper_bgcolor="#000000",
    font=dict(color="white"),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    ),
    width=1200,
    height=500  # adjust this number to your liking
)

# ------------- MAIN DISPLAY -------------
st.plotly_chart(fig, use_container_width=False)
