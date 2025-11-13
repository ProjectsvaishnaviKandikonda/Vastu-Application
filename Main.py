import streamlit as st
import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from Data import telugu_letters, mul, div, CSUB, CVFMAE, meaning_map

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🛕 తెలుగు వాస్తు షోడశవర్గులు", layout="wide")
st.title("🛕 తెలుగు వాస్తు - షోడశవర్గులు (Shodasha Vargas)")

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

def get_verdict(Money_Value, Expense_Value):
    if Money_Value > Expense_Value:
        return "Favourable"
    elif Money_Value == Expense_Value:
        return "Neutral"
    else:
        return "Unfavourable"

def style_vastu(row):
    if row['Verdict'] == 'Favourable':
        return ['background-color: #c6f5d3']*len(row)
    elif row['Verdict'] == 'Unfavourable':
        return ['background-color: #f5c6c6']*len(row)
    else:
        return ['background-color: #f0f0f0']*len(row)

def create_radar_chart_plotly(vastu_results):
    categories = [key.capitalize() for key in vastu_results.keys()]
    values = [vastu_results[key] for key in vastu_results.keys()]
    values += values[:1]

    colors = []
    for key in vastu_results.keys():
        if vastu_results[key] == div[key]:
            colors.append('green')
        else:
            colors.append('red')
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
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(div.values())])
        ),
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        width=360
    )

    return fig

# -----------------------------
# Input Section
# -----------------------------
# Group inputs into a form so the submit button aligns nicely with inputs
with st.form("input_form"):
    # use equal-width columns so the Calculate button lines up with inputs
    c1, c2, c3, c4 = st.columns([1,1,1,1])
    with c1:
        village_letter = st.selectbox("🏡 గ్రామం మొదటి అక్షరం", list(telugu_letters.keys()))
    with c2:
        person_letter = st.selectbox("👤 వ్యక్తి పేరు మొదటి అక్షరం", list(telugu_letters.keys()))
    with c3:
        area = st.number_input("📏 స్థల పరిమాణం (sq. ft)", min_value=1, step=1)
    with c4:
        # ensure the button fills the column and matches input height
        st.markdown(
            """
            <style>
            /* Target form widgets so the button height and inputs match */
            div.stButton > button {width:100%; height:38px; font-size:14px; margin-top:6px}
            /* Smaller selectbox/number input inner height to better match button */
            .stSelectbox div[data-baseweb="select"] {height:38px}
            .stNumberInput div[data-baseweb="input"] {height:38px}
            </style>
            """,
            unsafe_allow_html=True,
        )
        calc = st.form_submit_button("Calculate")

good_areas = [
    9,21,39,63,87,93,129,141,171,183,207,209,213,237,249,261,279,303,329,333,357,381,
    423,447,449,489,501,519,543,567,569,573,597,609,639,687,693,711,717,729,783,807,
    809,813,821,837,849,861,879,893,903,927,945,981,1023,1047,1049,1053,1077,1089,
    1101,1119,1143,1145,1169,1173,1197,1221,1239,1287,1289,1329,1359,1383,1393,1407,
    1413,1437,1449,1527,1529,1533,1551,1557,1589,1599,1613,1623,1649,1653,1679,1689,
    1701,1713,1717,1741,1767,1773,1809,1821,1863,1879,1887,1889,1893,1929,1967,1983,
    2009,2013,2037,2061
]

# -----------------------------
# Calculation Logic
# -----------------------------
if calc:
    v_val = lookup_letter_value(village_letter)
    n_val = lookup_letter_value(person_letter)

    Money_Value, Expense_Value = calculate_money_expense(v_val, n_val)

    if area in good_areas:
        st.success("✅ ఈ స్థల పరిమాణం మంచి క్షేత్రం (Good Plot)")
    else:
        st.info("ℹ️ స్థల పరిమాణం సాధారణ (Normal Plot)")

    # -----------------------------
    # Intermediate Bar Chart + Table side by side
    # -----------------------------
    st.subheader("📊 మధ్యంతర గణనలు (Intermediate Values)")
    # make the bar plot a bit narrower so it doesn't dominate the row
    col_bar, col_table = st.columns([2,1])

    intermediate_values = {"Money Value": Money_Value, "Expense Value": Expense_Value}

    # Bar chart
    with col_bar:
        st.markdown("### Money vs Expense")
        # more compact figure: fewer inches, tighter margins, smaller bars
        fig_intermediate, ax = plt.subplots(figsize=(2.2, 1.3), dpi=90)
        keys = list(intermediate_values.keys())
        vals = list(intermediate_values.values())
        indices = np.arange(len(keys))
        bars = ax.bar(indices, vals, color=["green", "red"], width=0.35)
        ax.set_xticks(indices)
        ax.set_xticklabels(keys)
        ax.set_ylabel("Value")

        # tighten spacing around bars
        ax.margins(x=0.12)

        # set a comfortable y-limit so annotations fit inside the figure
        max_val = max(vals) if len(vals) > 0 else 1
        ax.set_ylim(0, max_val * 1.08 + 0.3)

        # style axes for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # slightly smaller tick labels for compactness
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        # Use annotation with offset points so numbers are centered above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # smaller vertical offset
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='black'
            )

        fig_intermediate.tight_layout(pad=0.1)
        st.pyplot(fig_intermediate)

    # Table (centered)
    with col_table:
        table_df = pd.DataFrame({
            "Item": list(intermediate_values.keys()),
            "Value": list(intermediate_values.values())
        })
        # Vertically center the table beside the plot by using a fixed-height
        # flex container. The height here should roughly match the plot's
        # rendered height; adjust if necessary.
        st.markdown("<div style='height:150px; display:flex; align-items:center; justify-content:center;'>", unsafe_allow_html=True)
        st.markdown("<div style='width:90%;'>", unsafe_allow_html=True)
        st.markdown("#### Values", unsafe_allow_html=True)
        st.table(table_df)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Vastu Results Table + Radar Chart side by side
    # -----------------------------
    col_vastu_table, col_radar = st.columns([3,2])  # Table bigger, Radar smaller

    # Vastu Table
    vastu_results = calculate_vastu(area)
    vastu_items = []
    for key in mul.keys():
        val = vastu_results[key]
        meaning = meaning_map.get(key, {}).get(val, "—")
        verdict = "Favourable" if val == div[key] else "Unfavourable"
        vastu_items.append({
            "Vastu Item": key.capitalize(),
            "Value": val,
            "Meaning": meaning,
            "Verdict": verdict
        })
    vastu_df = pd.DataFrame(vastu_items)

    with col_vastu_table:
        st.subheader("📜 వాస్తు ఫలితాలు (Vastu Results)")
        st.dataframe(vastu_df.style.apply(style_vastu, axis=1))

    # Radar Chart
    radar_fig = create_radar_chart_plotly(vastu_results)
    with col_radar:
        st.subheader("📊 Shodasha Varga Radar Chart")
        # render radar chart smaller and fixed width so it doesn't dominate
        st.plotly_chart(radar_fig, width=360)

    # Final Verdict
    final_verdict = get_verdict(Money_Value, Expense_Value)
    st.markdown("---")
    st.markdown(f"### 🔮 తుది ఫలితం (Final Verdict): **{final_verdict}**")
