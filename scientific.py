# scientific_calculator_app.py
import streamlit as st
import math

# ------------------------------
# 1️⃣ Safe Evaluator with Mode Selection (Degree or Radian)
# ------------------------------
def preprocess_expression(expr, mode):
    """
    Convert expressions like "sin90" to "sin(radians(90))" or "sin(degrees(90))" depending on mode.
    """
    import re
    functions = ["sin", "cos", "tan", "asin", "acos", "atan"]
    for func in functions:
        if mode == "Degree":
            expr = re.sub(rf"{func}(\d+(\.\d+)?)", rf"{func}(radians(\1))", expr)
        else:
            expr = re.sub(rf"{func}(\d+(\.\d+)?)", rf"{func}(\1)", expr)
    return expr

def safe_eval(expr, mode):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names.update({"pi": math.pi, "e": math.e, "radians": math.radians})
    expr = preprocess_expression(expr, mode)

    try:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return result
    except Exception as e:
        return f"Error: {str(e)}"

# ------------------------------
# 2️⃣ Streamlit Layout
# ------------------------------
st.set_page_config(page_title="🧮 Scientific Calculator", layout="centered")
st.title("🧠 Easy Scientific Calculator for Students")

# Expression display state
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "mode" not in st.session_state:
    st.session_state.mode = "Degree"

# ------------------------------
# 3️⃣ Mode Selection (Degree / Radian)
# ------------------------------
st.sidebar.title("🧭 Settings")
st.session_state.mode = st.sidebar.radio("Select Angle Mode:", ["Degree", "Radian"])

# ------------------------------
# 4️⃣ Button Rows (Styled Equally)
# ------------------------------
buttons = [
    ["7", "8", "9", "/", "sqrt"],
    ["4", "5", "6", "*", "log"],
    ["1", "2", "3", "-", "log10"],
    ["0", ".", "+", "**", "exp"],
    ["sin", "cos", "tan", "pi", "e"],
    ["Clear", "←", "=", "(", ")"]
]

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 3em;
        font-size: 1.2em;
        font-weight: bold;
        border-radius: 8px;
        margin: 4px;
    }
    .stButton button:hover {
        background-color: #ffcccb;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------
# 5️⃣ UI Buttons + Logic
# ------------------------------
st.markdown("### 💻 Current Expression")
st.code(st.session_state.expression, language="markdown")

for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        with cols[i]:
            if st.button(btn, key=f"btn_{btn}_{i}"):
                if btn == "Clear":
                    st.session_state.expression = ""
                elif btn == "←":
                    st.session_state.expression = st.session_state.expression[:-1]
                elif btn == "=":
                    result = safe_eval(st.session_state.expression, st.session_state.mode)
                    st.success(f"✅ Result: {result}")
                elif btn in ["sin", "cos", "tan", "log", "log10", "sqrt", "exp"]:
                    st.session_state.expression += f"{btn}"
                elif btn in ["pi", "e"]:
                    st.session_state.expression += f"{btn}"
                else:
                    st.session_state.expression += btn

# ------------------------------
# 6️⃣ Optional Manual Text Input
# ------------------------------
with st.expander("✍️ Or Enter Expression Manually"):
    manual = st.text_input("Type Expression", value=st.session_state.expression)
    if st.button("Calculate Manually"):
        result = safe_eval(manual, st.session_state.mode)
        st.success(f"✅ Result: {result}")
        st.session_state.expression = manual

# ------------------------------
# 7️⃣ Help Panel
# ------------------------------
with st.expander("📘 Help & Guide"):
    st.markdown("""
    ### ℹ️ Usage Guide:
    - Type `sin90` — we auto-convert it to radians if Degree mode is selected
    - `log` = natural log; `log10` = base-10 log
    - `sqrt(x)` = square root
    - `exp(x)` = e^x

    ### 🔧 Angle Modes:
    - **Degree**: `sin90` is interpreted as sin(90 degrees)
    - **Radian**: `sin1.57` is sin(1.57 radians)

    Use buttons or type manually. All safe for students.
    """)

# ------------------------------
# 8️⃣ Footer
# ------------------------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit by Vimal Raj")
