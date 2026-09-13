import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import date
from sklearn.ensemble import RandomForestClassifier


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nagpur RoadSync",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# FUTURISTIC DARK UI
# ============================================================

st.markdown("""
<style>

/* ==============================
   MAIN BACKGROUND
   ============================== */

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            #10253d 0%,
            #07111f 35%,
            #030811 75%
        );

    color: #EAF6FF;
}


/* ==============================
   SIDEBAR
   ============================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #071625,
            #030a13
        );

    border-right: 1px solid #123B5A;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #00D9FF;
}


/* ==============================
   TITLE
   ============================== */

.main-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #00D9FF;

    text-shadow:
        0 0 8px rgba(0,217,255,0.8),
        0 0 20px rgba(0,217,255,0.35);

    margin-bottom: 0;
}


.subtitle {
    font-size: 15px;
    color: #8AA9C2;
    letter-spacing: 1px;
    margin-bottom: 25px;
}


.live-status {
    color: #00FF88;
    font-weight: 700;
}


/* ==============================
   METRIC CARDS
   ============================== */

.metric-card {
    background:
        linear-gradient(
            145deg,
            rgba(13,32,52,0.95),
            rgba(4,13,24,0.95)
        );

    border: 1px solid #164466;
    border-radius: 14px;

    padding: 20px;

    min-height: 115px;

    box-shadow:
        0 0 20px rgba(0,217,255,0.08);

    transition: 0.3s;
}


.metric-card:hover {
    border-color: #00D9FF;

    box-shadow:
        0 0 25px rgba(0,217,255,0.22);
}


.metric-title {
    color: #7895AB;
    font-size: 13px;
    letter-spacing: 1px;
}


.metric-value {
    color: #00D9FF;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}


.metric-green {
    color: #00FF88;
}


.metric-red {
    color: #FF405C;
}


.metric-yellow {
    color: #FFD84D;
}


/* ==============================
   SECTION HEADINGS
   ============================== */

.section-title {
    color: #00D9FF;

    font-size: 23px;

    font-weight: 750;

    border-left: 4px solid #00D9FF;

    padding-left: 12px;

    margin-top: 15px;
}


/* ==============================
   PANELS
   ============================== */

.panel {
    background:
        linear-gradient(
            145deg,
            rgba(10,28,46,0.96),
            rgba(4,12,22,0.96)
        );

    border: 1px solid #123B5A;

    border-radius: 15px;

    padding: 22px;

    margin-bottom: 15px;

    box-shadow:
        0 0 25px rgba(0,217,255,0.07);
}


/* ==============================
   AI PANEL
   ============================== */

.ai-panel {
    background:
        linear-gradient(
            135deg,
            #071C30,
            #06111E
        );

    border: 1px solid #00D9FF;

    border-radius: 15px;

    padding: 25px;

    box-shadow:
        0 0 25px rgba(0,217,255,0.13);
}


/* ==============================
   STATUS BADGES
   ============================== */

.status-conflict {
    color: #FF405C;
    font-weight: 800;
}

.status-risk {
    color: #FFD84D;
    font-weight: 800;
}

.status-safe {
    color: #00FF88;
    font-weight: 800;
}


/* ==============================
   BUTTONS
   ============================== */

.stButton > button {
    background:
        linear-gradient(
            90deg,
            #006C9C,
            #00A9D6
        );

    color: white;

    border: 1px solid #00D9FF;

    border-radius: 8px;

    font-weight: 700;

    min-height: 45px;

    box-shadow:
        0 0 12px rgba(0,217,255,0.15);
}


.stButton > button:hover {
    background:
        linear-gradient(
            90deg,
            #00A9D6,
            #00D9FF
        );

    border-color: #7CEFFF;
}


/* ==============================
   DATAFRAME
   ============================== */

div[data-testid="stDataFrame"] {
    border: 1px solid #123B5A;
    border-radius: 10px;
}


/* ==============================
   FOOTER
   ============================== */

.footer {
    text-align: center;

    color: #628198;

    font-size: 13px;

    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚧 NAGPUR INFRASYNC</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        AI-POWERED ROAD-DIGGING COORDINATION SYSTEM
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <span class="live-status">● SYSTEM LIVE</span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DEMO DATABASE
# ============================================================

data = {

    "Project": [
        "Water Pipeline",
        "Fiber Cable",
        "Electric Cable",
        "Drainage Work"
    ],

    "Department": [
        "Water Department",
        "Telecom Department",
        "Electricity Department",
        "NMC"
    ],

    "Road": [
        "Wardha Road",
        "Wardha Road",
        "Civil Lines Road",
        "Ring Road"
    ],

    "Start": [
        "2026-08-20",
        "2026-08-23",
        "2026-08-21",
        "2026-08-28"
    ],

    "End": [
        "2026-08-25",
        "2026-08-27",
        "2026-08-22",
        "2026-09-02"
    ]
}

df = pd.DataFrame(data)

df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])


# ============================================================
# AI DEMO MODEL
# ============================================================

# Features:
# [same road, date overlap, traffic level]

X = [
    [1, 1, 3],
    [1, 0, 2],
    [0, 1, 3],
    [0, 0, 1],
    [1, 1, 2],
    [0, 0, 2]
]

# 1 = conflict
# 0 = no conflict

y = [1, 1, 0, 0, 1, 0]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "## ➕ ADD NEW ROAD WORK"
)

st.sidebar.markdown(
    "---"
)

department = st.sidebar.selectbox(
    "Department",

    [
        "Water Department",
        "Telecom Department",
        "Electricity Department",
        "NMC"
    ]
)


road = st.sidebar.selectbox(
    "Road",

    [
        "Wardha Road",
        "Civil Lines Road",
        "Ring Road",
        "Kamptee Road",
        "Hingna Road"
    ]
)


work_type = st.sidebar.selectbox(
    "Work Type",

    [
        "Water Pipeline",
        "Fiber Cable",
        "Electric Cable",
        "Drainage Work"
    ]
)


start_date = st.sidebar.date_input(
    "Start Date",
    date(2026, 8, 20)
)


end_date = st.sidebar.date_input(
    "End Date",
    date(2026, 8, 25)
)


traffic = st.sidebar.slider(
    "Expected Traffic Level",
    1,
    3,
    2
)


if end_date < start_date:

    st.sidebar.error(
        "End Date cannot be before Start Date."
    )


# ============================================================
# FUNCTION: FIND CONFLICTS
# ============================================================

def find_conflicts(dataframe):

    conflicts = []

    for i in range(len(dataframe)):

        for j in range(i + 1, len(dataframe)):

            project1 = dataframe.iloc[i]

            project2 = dataframe.iloc[j]

            same_road = (
                project1["Road"]
                == project2["Road"]
            )

            overlap = (

                project1["Start"]
                <= project2["End"]

                and

                project1["End"]
                >= project2["Start"]
            )

            if same_road and overlap:

                conflicts.append({

                    "Road":
                        project1["Road"],

                    "Project 1":
                        project1["Project"],

                    "Project 2":
                        project2["Project"]

                })

    return conflicts


conflicts = find_conflicts(df)

conflict_count = len(conflicts)


# ============================================================
# TOP DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">📡 CITY INFRASTRUCTURE OVERVIEW</div>',
    unsafe_allow_html=True
)

st.write("")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        TOTAL PROJECTS
        </div>

        <div class="metric-value">
        {len(df):02d}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        ACTIVE ROADS
        </div>

        <div class="metric-value">
        {df["Road"].nunique():02d}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        DETECTED CONFLICTS
        </div>

        <div class="metric-value metric-red">
        {conflict_count:02d}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        """
        <div class="metric-card">

        <div class="metric-title">
        AI SYSTEM
        </div>

        <div class="metric-value metric-green">
        ● LIVE
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ROAD DATABASE
# ============================================================

st.markdown(
    '<div class="section-title">📊 ROAD WORK DATABASE</div>',
    unsafe_allow_html=True
)

st.write("")

display_df = df.copy()

display_df["Start"] = (
    display_df["Start"]
    .dt.strftime("%d-%b-%Y")
)

display_df["End"] = (
    display_df["End"]
    .dt.strftime("%d-%b-%Y")
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MAP DATA
# ============================================================

road_locations = {

    "Wardha Road":
        [21.1185, 79.0882],

    "Civil Lines Road":
        [21.1458, 79.0882],

    "Ring Road":
        [21.1350, 79.0700],

    "Kamptee Road":
        [21.1800, 79.1200],

    "Hingna Road":
        [21.1000, 78.9800]
}


map_data = []


for road_name, coordinates in road_locations.items():

    road_projects = df[
        df["Road"] == road_name
    ]

    status = "SAFE"

    color = [0, 255, 100]

    road_conflict = False


    for i in range(len(road_projects)):

        for j in range(i + 1, len(road_projects)):

            project1 = road_projects.iloc[i]

            project2 = road_projects.iloc[j]

            if (

                project1["Start"]
                <= project2["End"]

                and

                project1["End"]
                >= project2["Start"]

            ):

                road_conflict = True


    if road_conflict:

        status = "CONFLICT"

        color = [255, 40, 70]


    elif len(road_projects) > 0:

        status = "RISK"

        color = [255, 210, 40]


    map_data.append({

        "Road":
            road_name,

        "Latitude":
            coordinates[0],

        "Longitude":
            coordinates[1],

        "Status":
            status,

        "Color":
            color
    })


map_df = pd.DataFrame(map_data)


# ============================================================
# ROAD MAP
# ============================================================

st.markdown(
    '<div class="section-title">🗺️ NAGPUR ROAD CONFLICT MAP</div>',
    unsafe_allow_html=True
)

st.caption(
    "Prototype GIS visualization • Demo coordinates"
)


m1, m2, m3 = st.columns(3)


with m1:

    st.markdown(
        "🔴 **CONFLICT** — Overlapping projects"
    )


with m2:

    st.markdown(
        "🟡 **RISK** — Scheduled road work"
    )


with m3:

    st.markdown(
        "🟢 **SAFE** — No scheduled work"
    )


map_layer = pdk.Layer(

    "ScatterplotLayer",

    data=map_df,

    get_position=[
        "Longitude",
        "Latitude"
    ],

    get_fill_color="Color",

    get_radius=550,

    pickable=True,

    opacity=0.85
)


view_state = pdk.ViewState(

    latitude=21.1458,

    longitude=79.0882,

    zoom=11,

    pitch=35
)


deck = pdk.Deck(

    layers=[map_layer],

    initial_view_state=view_state,

    tooltip={

        "html":
        """
        <b>🚧 ROAD:</b> {Road}<br/>
        <b>STATUS:</b> {Status}
        """
    }
)


st.pydeck_chart(
    deck,
    use_container_width=True
)


# ============================================================
# TIMELINE
# ============================================================

st.markdown(
    '<div class="section-title">📅 ROAD WORK TIMELINE</div>',
    unsafe_allow_html=True
)

timeline_df = df.copy()


fig = px.timeline(

    timeline_df,

    x_start="Start",

    x_end="End",

    y="Road",

    color="Department",

    hover_data=[
        "Project",
        "Department",
        "Road"
    ],

    title="Infrastructure Work Schedule"
)


fig.update_yaxes(
    autorange="reversed"
)


fig.update_layout(

    height=420,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="#DCEEFF"
    ),

    title_font=dict(
        color="#00D9FF",
        size=20
    ),

    xaxis=dict(
        gridcolor="#18364F"
    ),

    yaxis=dict(
        gridcolor="#18364F"
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# AI CONFLICT DETECTION
# ============================================================

st.markdown(
    '<div class="section-title">🤖 AI CONFLICT DETECTION</div>',
    unsafe_allow_html=True
)

st.write("")


if st.button(
    "🔍 ANALYZE NEW PROJECT",
    use_container_width=True
):

    conflict_found = False

    new_start = pd.Timestamp(
        start_date
    )

    new_end = pd.Timestamp(
        end_date
    )


    for _, row in df.iterrows():

        same_road = (
            row["Road"] == road
        )

        date_overlap = (

            new_start <= row["End"]

            and

            new_end >= row["Start"]
        )


        if same_road and date_overlap:

            conflict_found = True


            st.error(
                f"""
                ⚠️ CONFLICT DETECTED

                Your **{work_type}** project overlaps with
                **{row['Project']}**

                🏢 Department:
                **{row['Department']}**

                📍 Road:
                **{road}**

                📅 Existing Work:
                **{row['Start'].strftime('%d-%b-%Y')}
                → {row['End'].strftime('%d-%b-%Y')}**
                """
            )


            st.warning(
                """
                🤖 AI Recommendation:
                Coordinate both projects and use
                ONE excavation window.
                """
            )


    if not conflict_found:

        st.success(
            "✅ NO MAJOR CONFLICT DETECTED"
        )

        st.info(
            """
            🤖 AI Recommendation:
            Project can proceed according to schedule.
            """
        )


# ============================================================
# AI RISK ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">📈 AI RISK ANALYSIS</div>',
    unsafe_allow_html=True
)

st.write("")


if st.button(
    "🤖 CALCULATE AI RISK SCORE",
    use_container_width=True
):

    same_road = (

        1
        if road in df["Road"].values
        else 0
    )


    date_overlap = 0


    for _, row in df.iterrows():

        if row["Road"] == road:

            if (

                pd.Timestamp(start_date)
                <= row["End"]

                and

                pd.Timestamp(end_date)
                >= row["Start"]

            ):

                date_overlap = 1


    prediction = model.predict(

        [[
            same_road,
            date_overlap,
            traffic
        ]]

    )[0]


    probability = model.predict_proba(

        [[
            same_road,
            date_overlap,
            traffic
        ]]

    )[0][1]


    score = round(
        probability * 100
    )


    risk1, risk2 = st.columns(2)


    with risk1:

        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-title">
            AI CONFLICT PROBABILITY
            </div>

            <div class="metric-value metric-red">
            {score}%
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with risk2:

        if prediction == 1:

            st.markdown(
                """
                <div class="metric-card">

                <div class="metric-title">
                AI DECISION
                </div>

                <div class="metric-value metric-red">
                HIGH RISK
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="metric-card">

                <div class="metric-title">
                AI DECISION
                </div>

                <div class="metric-value metric-green">
                LOW RISK
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    if prediction == 1:

        st.error(
            "🔴 HIGH RISK — Department coordination recommended."
        )

    else:

        st.success(
            "🟢 LOW RISK — No major conflict predicted."
        )


# ============================================================
# SMART RECOMMENDATION
# ============================================================

st.markdown(
    '<div class="section-title">💡 SMART AI RECOMMENDATION</div>',
    unsafe_allow_html=True
)

st.write("")


st.markdown(
    """
    <div class="ai-panel">

    <h2 style="color:#00D9FF;">
    🤖 AI COORDINATION CENTER
    </h2>

    <p>
    <b>1.</b> Coordinate departments working on
    the same road.
    </p>

    <p>
    <b>2.</b> Combine excavation activities
    wherever possible.
    </p>

    <p>
    <b>3.</b> Avoid repeated road cutting.
    </p>

    <p>
    <b>4.</b> Schedule work during lower-traffic
    periods.
    </p>

    <p>
    <b>5.</b> Track road restoration after
    completion.
    </p>

    <hr>

    <h2 style="color:#00FF88;">
    🎯 DIG ONCE → COMPLETE MULTIPLE WORKS
    → RESTORE ONCE
    </h2>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT IMPACT
# ============================================================

st.markdown(
    '<div class="section-title">🌆 EXPECTED SMART CITY IMPACT</div>',
    unsafe_allow_html=True
)

st.write("")


i1, i2, i3, i4 = st.columns(4)


with i1:

    st.markdown(
        """
        <div class="metric-card">

        <div class="metric-title">
        ROAD DAMAGE
        </div>

        <div class="metric-value metric-green">
        ↓
        </div>

        <p>Less repeated excavation</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with i2:

    st.markdown(
        """
        <div class="metric-card">

        <div class="metric-title">
        TRAFFIC DISRUPTION
        </div>

        <div class="metric-value metric-green">
        ↓
        </div>

        <p>Better scheduling</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with i3:

    st.markdown(
        """
        <div class="metric-card">

        <div class="metric-title">
        DEPARTMENT COORDINATION
        </div>

        <div class="metric-value metric-green">
        ↑
        </div>

        <p>Shared infrastructure planning</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with i4:

    st.markdown(
        """
        <div class="metric-card">

        <div class="metric-title">
        RESTORATION
        </div>

        <div class="metric-value metric-green">
        ↑
        </div>

        <p>Track road restoration</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🚧 <b>Nagpur RoadSync</b> |
    AI-Powered Smart Infrastructure Coordination

    <br><br>

    Dig Once • Coordinate Better • Restore Once

    </div>
    """,
    unsafe_allow_html=True
)
# ============================================================
# 🚀 AI ACTION & COORDINATION CENTER
# ============================================================

st.markdown("---")
st.header("🤖 AI Action & Coordination Center")

# -----------------------------
# 1. AI EXPLAINABILITY
# -----------------------------

st.subheader("🔍 Why is this Conflict HIGH RISK?")

risk_factors = [
    ("Same Road", True, "Both projects are planned on the same road"),
    ("Date Overlap", True, "Project schedules overlap"),
    ("Multiple Departments", True, "Different departments need excavation"),
    ("Traffic Impact", True, "Road has significant traffic"),
    ("Existing Infrastructure Work", True, "Another infrastructure activity is already planned")
]

for factor, detected, explanation in risk_factors:
    if detected:
        st.success(f"✅ **{factor}** — {explanation}")

st.markdown(
    """
    <div style="
        padding:20px;
        border-radius:15px;
        background:linear-gradient(135deg,#3b0000,#650000);
        border:1px solid #ff4b4b;
        margin-top:15px;
        text-align:center;
    ">
        <h2 style="margin:0;">⚠️ AI CONFLICT RISK: 96%</h2>
        <p style="font-size:18px;margin:8px;">
        HIGH RISK — Coordination Recommended
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 2. AI RECOMMENDATION
# -----------------------------

st.subheader("🧠 AI Recommended Coordination Plan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🚧 Conflict Detected

    **Project A:** Water Pipeline  
    **Project B:** Fiber Cable  

    **Road:** Wardha Road  
    **Departments:** Water + Telecom
    """)

with col2:
    st.markdown("""
    ### 💡 AI Recommendation

    **Action:** Joint Excavation

    **Recommended Window:**  
    23 – 25 August 2026

    **Traffic:** Prefer low-traffic hours

    **Restoration:** Single restoration cycle
    """)

# -----------------------------
# 3. APPROVE COORDINATION
# -----------------------------

st.subheader("🏛️ Municipal Decision")

if "coordination_approved" not in st.session_state:
    st.session_state.coordination_approved = False

if not st.session_state.coordination_approved:

    if st.button(
        "🟢 APPROVE COORDINATION PLAN",
        use_container_width=True
    ):
        st.session_state.coordination_approved = True
        st.rerun()

else:

    st.success("✅ Coordination Plan Approved")

    st.markdown("""
    ### 📢 Coordination Status

    ✅ Water Department notified  
    ✅ Telecom Department notified  
    ✅ Joint excavation scheduled  
    ✅ Low-traffic work window selected  
    ✅ Single road restoration planned
    """)

# -----------------------------
# 4. BEFORE vs AFTER
# -----------------------------

st.subheader("📊 Smart City Impact — Before vs After")

before, after = st.columns(2)

with before:
    st.markdown("""
    ### ❌ WITHOUT INFRA SYNC

    🔴 2 separate excavations  
    🔴 2 traffic disruptions  
    🔴 2 restoration cycles  
    🔴 Higher coordination cost  
    🔴 Longer road disturbance
    """)

with after:
    st.markdown("""
    ### ✅ WITH INFRA SYNC

    🟢 1 coordinated excavation  
    🟢 Reduced traffic disruption  
    🟢 1 restoration cycle  
    🟢 Better department coordination  
    🟢 Faster infrastructure completion
    """)

st.markdown(
    """
    <div style="
        padding:22px;
        border-radius:18px;
        margin-top:20px;
        text-align:center;
        background:linear-gradient(135deg,#062e16,#0b5e2b);
        border:2px solid #20c970;
    ">
        <h1 style="margin:0;">DIG ONCE → COMPLETE MULTIPLE WORKS → RESTORE ONCE</h1>
        <p style="font-size:17px;">
        AI-powered infrastructure coordination for smarter cities
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
