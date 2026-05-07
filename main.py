import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Smart Strategy Pro", layout="wide")

# ၁။ သင်ပေးထားသော Pattern အသစ်များ (Updated Prediction Logic)
special_pats = {
    "BSSS": "S", 
    "SSSB": "S", 
    "SBBB": "B", 
    "BBBS": "B"
}

normal_pats = {
    "BBSS": "S", 
    "SSBB": "S", 
    "BSBS": "S", 
    "SBSB": "B",
    "BSSB": "S", 
    "SBBS": "B", 
    "BBSB": "B", 
    "SSBS": "S",
    "BSBB": "B", 
    "SBSS": "B"
}

skip_pats = ["BBBB", "SSSS"]

# ၂။ Session State Initialization
if 'special_history' not in st.session_state: st.session_state.special_history = []
if 'normal_history' not in st.session_state: st.session_state.normal_history = []

# --- UI SECTION ၁: HISTORY (အပေါ်ဆုံး) ---
st.title("🎯 TRX Professional Dashboard")
h_col1, h_col2 = st.columns(2)

# Special History
with h_col1:
    st.subheader("🔥 Special History")
    dots_spec = "".join(["🟢" if x == "W" else "🔴" for x in st.session_state.special_history])
    st.markdown(f"<div style='font-size:20px; word-wrap: break-word;'>{dots_spec if dots_spec else '➖'}</div>", unsafe_allow_html=True)
    if st.button("Clear Special History"):
        st.session_state.special_history = []
        st.rerun()

# Normal History
with h_col2:
    st.subheader("📊 Normal History")
    dots_norm = "".join(["🟢" if x == "W" else "🔴" for x in st.session_state.normal_history])
    st.markdown(f"<div style='font-size:20px; word-wrap: break-word;'>{dots_norm if dots_norm else '➖'}</div>", unsafe_allow_html=True)
    if st.button("Clear Normal History"):
        st.session_state.normal_history = []
        st.rerun()

st.divider()

# --- UI SECTION ၂: PREDICTION & W/L BUTTONS (အလယ်) ---
input_pat = st.text_input("Pattern ၄ လုံး ရိုက်ထည့်ပါ (ဥပမာ- BSSS)", key="main_input").upper()

if len(input_pat) == 4:
    is_special = input_pat in special_pats
    is_normal = input_pat in normal_pats
    is_skip = input_pat in skip_pats
    prediction = None
    
    # Prediction Alert Logic
    if is_special:
        prediction = special_pats[input_pat]
        st.error(f"🚨 SPECIAL ALERT: Next Bet **{ 'BIG (B)' if prediction == 'B' else 'SMALL (S)' }**")
    elif is_normal:
        prediction = normal_pats[input_pat]
        st.success(f"✅ NEXT BET: Bet **{ 'BIG (B)' if prediction == 'B' else 'SMALL (S)' }**")
    elif is_skip:
        st.warning(f"⛔ {input_pat} SKIP: ဒီတစ်ပွဲ မထိုးဘဲ စောင့်ကြည့်ပါ")
    else:
        st.info("Pattern မတွေ့ပါ။")

    # Win / Lose နှိပ်ရန် Button များ (Skip pattern မဟုတ်မှ ပေါ်မည်)
    if prediction:
        st.write("---")
        st.write("ရလဒ် မှတ်တမ်းတင်ရန် (W/L နှိပ်ပါ)")
        b1, b2 = st.columns(2)
        
        if b1.button("✅ WON (W)", use_container_width=True):
            if is_special: st.session_state.special_history.append("W")
            else: st.session_state.normal_history.append("W")
            st.rerun()
            
        if b2.button("❌ LOST (L)", use_container_width=True):
            if is_special: st.session_state.special_history.append("L")
            else: st.session_state.normal_history.append("L")
            st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.write("### Strategy Summary")
    st.write("- **Special:** BSSS, SSSB, SBBB, BBBS")
    st.write("- **Skip:** BBBB, SSSS")
    st.write("- **Normal:** Others")
    if st.button("Reset All Data"):
        st.session_state.special_history = []
        st.session_state.normal_history = []
        st.rerun()
