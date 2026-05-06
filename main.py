import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Smart Alert Pro", layout="wide")

# ၁။ Betting Settings & Logic
# အုပ်စု (၁) - Special Patterns
special_pats = {
    "BSSS": "S", "SSSB": "B", "SBBB": "S", "BBBS": "B"
}
# အုပ်စု (၂) - Normal Patterns
normal_pats = {
    "BBSS": "B", "SSBB": "B", "BSBS": "B", "SBSB": "S",
    "BSSB": "B", "SBBS": "S", "BBSB": "S", "SSBS": "B",
    "BSBB": "S", "SBSS": "S"
}
skip_pats = ["BBBB", "SSSS"]

# Money Management (5 Steps)
bet_amounts = [500, 1000, 2000, 4500, 10000]

# ၂။ Session State Initialization
if 'bet_step' not in st.session_state: st.session_state.bet_step = 0
if 'last_result' not in st.session_state: st.session_state.last_result = None # WIN or LOSE
if 'special_history' not in st.session_state: st.session_state.special_history = []
if 'normal_history' not in st.session_state: st.session_state.normal_history = []

# --- UI Header ---
st.title("🎯 TRX Professional Strategy Dashboard")

# ၃။ Win/Loss History ပြသရန် (နှစ်ခြမ်းခွဲ)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🔥 Special Patterns History")
    # BSSS, SSSB, SBBB, BBBS အတွက်
    h_special = "".join(["🟢" if x == "W" else "🔴" for x in st.session_state.special_history[-10:]])
    st.markdown(f"<div style='font-size:24px;'>{h_special if h_special else '➖'}</div>", unsafe_allow_html=True)

with col_right:
    st.subheader("📊 Normal Patterns History")
    h_normal = "".join(["🟢" if x == "W" else "🔴" for x in st.session_state.normal_history[-10:]])
    st.markdown(f"<div style='font-size:24px;'>{h_normal if h_normal else '➖'}</div>", unsafe_allow_html=True)

st.divider()

# ၄။ Manual Pattern Input
st.subheader("၁။ Pattern ရိုက်ထည့်ပါ (Manual)")
input_pat = st.text_input("Pattern ၄ လုံး ရိုက်ပါ (ဥပမာ- BSSS)", "").upper()

if len(input_pat) == 4:
    st.info(f"လက်ရှိ Pattern: **{input_pat}**")
    
    # ၅။ Alert Logic
    alert_col1, alert_col2 = st.columns([2, 1])

    with alert_col1:
        # Case 1: Special Patterns (အနီရောင် Alert Box နဲ့ပြမယ်)
        if input_pat in special_pats:
            bet_move = special_pats[input_pat]
            st.error(f"🚨 SPECIAL ALERT: Next Bet **{ 'BIG (B)' if bet_move == 'B' else 'SMALL (S)' }**")
            st.warning("⚠️ Special Pattern ဖြစ်၍ တိုက်ရိုက်ထိုးရန်!")

        # Case 2: Normal Patterns (Win မှ လိုက်ထိုးမည့် စနစ်)
        elif input_pat in normal_pats:
            bet_move = normal_pats[input_pat]
            if st.session_state.last_result == "W":
                st.success(f"✅ WIN NEXT BET ALERT: Bet **{ 'BIG (B)' if bet_move == 'B' else 'SMALL (S)' }**")
                # ပမာဏပြသခြင်း
                amt = bet_amounts[st.session_state.bet_step]
                st.metric("ထိုးရမည့် ပမာဏ", f"{amt} MMK")
            else:
                st.info("📉 LOSE SKIP: တစ်ခါနိုင်မှ နောက်တစ်ပွဲ လိုက်ထိုးပါ")
        
        elif input_pat in skip_pats:
            st.markdown("### ⛔ SKIP: စောင့်ကြည့်ပါ")

    # ၆။ Result Recording (Win/Lose မှတ်တမ်းတင်ခြင်း)
    with alert_col2:
        st.write("ရလဒ် မှတ်တမ်းတင်ရန်")
        btn_w = st.button("✅ WON", use_container_width=True)
        btn_l = st.button("❌ LOST", use_container_width=True)

        if btn_w or btn_l:
            status = "W" if btn_w else "L"
            st.session_state.last_result = "W" if btn_w else "L"
            
            # History ထဲ ထည့်ခြင်း
            if input_pat in special_pats:
                st.session_state.special_history.append(status)
            else:
                st.session_state.normal_history.append(status)
            
            # Money Management Reset/Step Logic (၅ ခါပြည့်ရင် သို့မဟုတ် နိုင်ရင်/ရှုံးရင် reset လုပ်ချင်တဲ့အပေါ်မူတည်)
            if status == "W":
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
            else:
                # ရှုံးရင်လည်း Step တက်မလား သို့မဟုတ် Reset လား? (၅ ခါပဲလိုက်မယ်ဆိုတော့ Step တက်မယ်)
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
            
            if st.session_state.bet_step == 0:
                st.toast("Money Step Reset ဖြစ်သွားပါပြီ (၅ ကြိမ်ပြည့်)")
                
            st.rerun()

# ၇။ Sidebar Info
with st.sidebar:
    st.header("⚙️ Betting Info")
    st.write(f"လက်ရှိ Step: **{st.session_state.bet_step + 1}**")
    st.write(f"နောက်ထိုးရမည့် ပမာဏ: **{bet_amounts[st.session_state.bet_step]}**")
    if st.button("Reset Step & History"):
        st.session_state.bet_step = 0
        st.session_state.special_history = []
        st.session_state.normal_history = []
        st.session_state.last_result = None
        st.rerun()
