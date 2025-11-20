import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Data import telugu_letters, mul, div, CSUB, CVFMAE, meaning_map, letter_range_rashi_dynamic, good_areas
from style import load_custom_styles

load_custom_styles()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🛕 తెలుగు వాస్తు షోడశవర్గులు", layout="wide")
st.markdown('<div class="main-title">🛕 తెలుగు వాస్తు - షోడశ వర్గాలు</div>', unsafe_allow_html=True)
# st.title("🛕 తెలుగు వాస్తు - షోడశ వర్గాలు (Shodasha Vargas)")

# -----------------------------
# Helper Functions
# -----------------------------
def lookup_letter_value(letter):
    return telugu_letters.get(letter, 0)

def calculate_money_expense(v_val, n_val):
    v_minus = v_val - CSUB
    n_minus = n_val - CSUB
    Money = v_minus if v_minus != 0 else 52
    Person_Name = n_minus if n_minus != 0 else 52
    money_concat = int(f"{Money}{Person_Name}")
    expense_concat = int(f"{Person_Name}{Money}")
    Money_Value = money_concat % CVFMAE
    Expense_Value = expense_concat % CVFMAE
    return Money_Value, Expense_Value

def calculate_vastu(area):
    results = {}
    for key in mul.keys():
        computed = (area * mul[key]) % div[key]
        results[key] = computed if computed != 0 else div[key]
    return results

def style_vastu(row):
    if row['Verdict'] == 'మంచిది':
        return ['background-color: #c6f5d3'] * len(row)
    elif row['Verdict'] == 'మంచిదికాదు':
        return ['background-color: #f5c6c6'] * len(row)
    else:
        return ['background-color: #f0f0f0'] * len(row)

def create_radar_chart_plotly(vastu_results):
    categories = [key.capitalize() for key in vastu_results.keys()]
    values = [vastu_results[key] for key in vastu_results.keys()]
    values += values[:1]

    # Colors based on favourable/unfavourable
    colors = []
    for key in vastu_results.keys():
        meaning = meaning_map.get(key, {}).get(vastu_results[key], "")
        if "మంచిదికాదు" in meaning:
            colors.append('red')
        elif "మంచిది" in meaning:
            colors.append('green')
        else:
            colors.append('grey')
    colors += colors[:1]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        line_color='blue',
        fillcolor='rgba(0,0,255,0.1)',
        hovertemplate='%{theta}: %{r}<extra></extra>'
    ))

    for i, val in enumerate(values[:-1]):
        fig.add_trace(go.Scatterpolar(
            r=[val],
            theta=[categories[i]],
            mode='markers',
            marker=dict(color=colors[i], size=10),
            showlegend=False,
            hovertemplate=f"{categories[i]}: {val}<extra></extra>"
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(div.values())])),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        width=360
    )
    return fig

def get_letter_group_info(selected_letter):
    """Returns all letters and Rashi/Nakshatram groups for the selected letter."""
    if selected_letter not in letter_range_rashi_dynamic:
        return []
    letter_groups_info = []
    for rashi, letters in letter_range_rashi_dynamic[selected_letter].items():
        letter_groups_info.append({
            "Letters": ", ".join(letters),
            "Rashi": rashi,
            "Nakshatram": rashi
        })
    return letter_groups_info

# -----------------------------
# Input Section
# -----------------------------
with st.form("input_form"):
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        village_letter = st.selectbox("🏡 గ్రామం మొదటి అక్షరం", list(telugu_letters.keys()))
    with c2:
        person_letter = st.selectbox("👤 వ్యక్తి పేరు మొదటి అక్షరం", list(telugu_letters.keys()))
    with c3:
        area = st.number_input("📏 స్థల పరిమాణం (sq. ft)", min_value=1, step=1)
    with c4:
        st.markdown("""
            <style>
            div.stButton > button {width:100%; height:38px; font-size:14px; margin-top:6px}
            .stSelectbox div[data-baseweb="select"] {height:38px}
            .stNumberInput div[data-baseweb="input"] {height:38px}
            </style>
        """, unsafe_allow_html=True)
        calc = st.form_submit_button("Calculate")

# -----------------------------
# Calculation Logic
# -----------------------------
if calc:

    # 1️⃣ Plot Info
    if area in good_areas:
        st.success("✅ ఈ స్థల పరిమాణం మంచి క్షేత్రం (Good Plot)")
    else:
        st.info("ℹ️ స్థల పరిమాణం సాధారణ (Normal Plot)")

    # 2️⃣ Rashi / Nakshatra Table
    letter_groups_info = get_letter_group_info(person_letter)
    if letter_groups_info:
        st.subheader(f"✨ '{person_letter}' అక్షరానికి సంబంధించిన రాశి & నక్షత్ర సమాచారము")
        st.table(pd.DataFrame(letter_groups_info))

    # 3️⃣ Money & Expense Values
    v_val = lookup_letter_value(village_letter)
    n_val = lookup_letter_value(person_letter)
    Money_Value, Expense_Value = calculate_money_expense(v_val, n_val)

    st.subheader("స్థల విలువలు – ధనం & వ్యయం (గ్రామం & పేరుల ఆధారంగా)")
    table_df = pd.DataFrame({
        "Item": ["ధనం", "వ్యయం"],
        "Value": [Money_Value, Expense_Value]
    })
    st.table(table_df)

    # 4️⃣ Vastu Results Table + Radar Chart
    col_vastu_table, col_radar = st.columns([3, 2])

    vastu_results = calculate_vastu(area)
    vastu_items = []

    for key in mul.keys():
        val = vastu_results[key]
        meaning = meaning_map.get(key, {}).get(val, "—")

        # Verdict
        if "మంచిదికాదు" in meaning:
            verdict = "మంచిదికాదు"
        elif "మంచిది" in meaning:
            verdict = "మంచిది"
        else:
            verdict = "-"

        vastu_items.append({
            "Vastu Item": key.capitalize(),
            "Value": val,
            "Meaning": meaning,
            "Verdict": verdict
        })

    vastu_df = pd.DataFrame(vastu_items)

    with col_vastu_table:
        st.subheader("స్థల పరిమాణానికి సంబంధించిన వాస్తు ఫలితాలు")
        st.dataframe(vastu_df.style.apply(style_vastu, axis=1))

    with col_radar:
        st.subheader("షోడశ వర్గ ఫలితాల రాడార్ చార్ట్")
        radar_fig = create_radar_chart_plotly(vastu_results)
        st.plotly_chart(radar_fig, use_container_width=True)
