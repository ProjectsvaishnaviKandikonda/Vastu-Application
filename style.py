import streamlit as st

def load_custom_styles():
    st.markdown(
        """
        <style>

        /* -----------------------------------------------------------
           FONTS (Telugu + English clean UI)
        ------------------------------------------------------------*/
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@300;400;600&family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Noto Sans Telugu', 'Poppins', sans-serif !important;
        }

        /* -----------------------------------------------------------
           COLOR PALETTE (Premium Vastu Theme)
        ------------------------------------------------------------*/
        :root {
            --gold: #e0b44c;
            --dark-blue: #182952;
            --light-blue: #edf2ff;
            --white: #ffffff;
            --green-good: #c6f5d3;
            --red-bad: #f5c6c6;
            --border-light: #dcdcdc;
            --soft-grey: #f8f8f8;
        }

        /* -----------------------------------------------------------
           MAIN TITLE STYLE
        ------------------------------------------------------------*/
        .main-title {
            color: var(--dark-blue);
            font-size: 30px;
            font-weight: 700;
            padding-bottom: 8px;
            border-bottom: 4px solid var(--gold);
            margin-bottom: 20px;
        }

        /* -----------------------------------------------------------
           SECTION HEADINGS
        ------------------------------------------------------------*/
        .section-title {
            color: var(--dark-blue);
            font-size: 20px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        /* -----------------------------------------------------------
           CARD BOXES
        ------------------------------------------------------------*/
        .styled-card {
            background-color: var(--white);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid var(--border-light);
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 18px;
        }

        /* -----------------------------------------------------------
           TABLE HEADER STYLING
        ------------------------------------------------------------*/
        thead tr th {
            background-color: var(--dark-blue) !important;
            color: white !important;
            font-size: 14px !important;
            padding: 8px !important;
        }

        /* -----------------------------------------------------------
           TABLE GOOD/BAD COLORING
        ------------------------------------------------------------*/
        .good-row td {
            background-color: var(--green-good) !important;
        }

        .bad-row td {
            background-color: var(--red-bad) !important;
        }

        /* -----------------------------------------------------------
           BUTTON STYLING
        ------------------------------------------------------------*/
        div.stButton > button {
            background-color: var(--dark-blue) !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 22px;
            font-size: 15px;
            border: none;
            transition: 0.2s ease-in-out;
        }

        div.stButton > button:hover {
            background-color: var(--gold) !important;
            color: black !important;
            transform: scale(1.03);
        }

        /* -----------------------------------------------------------
           SELECTBOX & NUMBER INPUT
        ------------------------------------------------------------*/
        .stSelectbox div[data-baseweb="select"],
        .stNumberInput div[data-baseweb="input"] {
            height: 45px !important;
        }

        /* -----------------------------------------------------------
           RADIO / CHECKBOX FONT
        ------------------------------------------------------------*/
        .stRadio label, .stCheckbox label {
            font-size: 15px !important;
            font-weight: 500 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
