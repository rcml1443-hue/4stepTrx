import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Smart Alert Pro", layout="wide")

# ၁။ Betting Settings & Logic
special_pats = {"BSSS": "S", "SSSB": "B", "SBBB": "S", "BBBS": "B"}
normal_pats = {
    "BBSS": "B", "SSBB": "B", "BSBS": "B", "SBSB": "S",
    "BSSB": "B", "SBBS": "S", "BBSB": "S", "SSBS": "B",
    "BSBB": "S", "SBSS": "S"
}
skip_pats = ["BBBB", "SSSS"]
bet_amounts = [500, 1000, 2000, 4500, 10000]

# ၂။ Session State Initialization
if 'bet_step' not in st.session_state: st.session_state.bet_step = 0
if 'last_result' not in st.session_state: st.session_state.last_result = None
if 'special_history' not in st.session_state: st.session_state.special_history = []
if 'normal_history' not in st.session_state: st.session_state.normal_history = []

# --- UI Layout ---
st.title("🎯 TRX Professional Strategy Dashboard")

# ၃။ Top Alert Section (Enter နှိပ်ရင် ဒီနေရာမှာ အရင်ပေါ်မယ်)
alert_area = st.container()

st.divider()

# ၄။ History Display Section (သီးသန့်စီ ခွဲပြပြီး တစ်လုံးချင်း ဖျက်နိုင်ရန်)
col_left, col_right = st.columns(2)

def draw_history(title, history_list, key_prefix):
    st.subheader(title)
    if history_list:
        # နိုင်/ရှုံး အစက်လေးများ summary
        dots = "".join(["🟢" if x == "W" else "🔴" for x in history_list])
        st.markdown(f"<div style='font-size:20px;'>Summary: {dots}</div>", unsafe_allow_html=True)
        
        # တစ်လုံးချင်းဖျက်ရန် ခလုတ်များ (နောက်ဆုံး ၁၀ ခု)
        cols = st.columns(10)
        for i, val in enumerate(history_list[-10:]):
            actual_index = len(history_list) - len(history_list[-10:]) + i
            with cols[i]:
                if st.button(f"{val}x", key=f"{key_prefix}_{actual_index}"):
                    history_list.pop(actual_index)
                    st.rerun()
    else:
        st.write("No record yet.")

with col_left:
    draw_history("🔥 Special Patterns History", st.session_state.special_history, "spec")

with col_right:
    draw_history("📊 Normal Patterns History", st.session_state.normal_history, "norm")

st.divider()

# ၅။ Manual Pattern Input
st.subheader("၁။ Pattern ရိုက်ထည့်ပါ (Manual)")
input_pat = st.text_input("Pattern ၄ လုံး ရိုက်ပြီး Enter နှိပ်ပါ (ဥပမာ- BSSS)", "").upper()

if len(input_pat) == 4:
    # ၆။ Alert Logic ကို အပေါ်ဆုံး Container ထဲ ထည့်ခြင်း
    with alert_area:
        st.info(f"လက်ရှိ Pattern: **{input_pat}**")
        a_col1, a_col2 = st.columns([2, 1])
        
        is_special = input_pat in special_pats
        prediction = None
        
        with a_col1:
            if is_special:
                prediction = special_pats[input_pat]
                st.error(f"🚨 SPECIAL ALERT: Next Bet **{ 'BIG (B)' if prediction == 'B' else 'SMALL (S)' }**")
            elif input_pat in normal_pats:
                prediction = normal_pats[input_pat]
                if st.session_state.last_result == "W":
                    amt = bet_amounts[st.session_state.bet_step]
                    st.success(f"✅ WIN NEXT: Bet **{ 'BIG (B)' if prediction == 'B' else 'SMALL (S)' }**")
                    st.metric("ထိုးရမည့် ပမာဏ", f"{amt} MMK")
                else:
                    st.info("📉 LOSE SKIP: တစ်ခါနိုင်မှ နောက်တစ်ပွဲ လိုက်ထိုးပါ")
            elif input_pat in skip_pats:
                st.markdown("### ⛔ SKIP: စောင့်ကြည့်ပါ")
        
        with a_col2:
            st.write("ရလဒ် မှတ်တမ်းတင်ရန်")
            bw, bl = st.columns(2)
            if bw.button("✅ WON", use_container_width=True):
                if is_special: st.session_state.special_history.append("W")
                else: st.session_state.normal_history.append("W")
                st.session_state.last_result = "W"
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
                st.rerun()
            if bl.button("❌ LOST", use_container_width=True):
                if is_special: st.session_state.special_history.append("L")
                else: st.session_state.normal_history.append("L")
                st.session_state.last_result = "L"
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
                st.rerun()

# ၇။ Sidebar Info
with st.sidebar:
    st.header("⚙️ Betting Info")
    st.write(f"လက်ရှိ Step: **{st.session_state.bet_step + 1}**")
    st.write(f"နောက်ထိုးရမည့် ပမာဏ: **{bet_amounts[st.session_state.bet_step]}**")
    if st.button("Reset All Data"):
        st.session_state.bet_step = 0
        st.session_state.special_history = []
        st.session_state.normal_history = []
        st.session_state.last_result = None
        st.rerun()
