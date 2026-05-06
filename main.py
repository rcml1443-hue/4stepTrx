import streamlit as st
import pandas as pd

st.set_page_config(page_title="TRX Ultra Smart Predictor", layout="wide")

# ၁။ Betting Rules & Logic
special_pats = {"BSSS": "S", "SSSB": "B", "SBBB": "S", "BBBS": "B"}
normal_pats = {
    "BBSS": "B", "SSBB": "B", "BSBS": "B", "SBSB": "S",
    "BSSB": "B", "SBBS": "S", "BBSB": "S", "SSBS": "B",
    "BSBB": "S", "SBSS": "S"
}
bet_amounts = [500, 1000, 2000, 4500, 10000]

# ၂။ Session State Initialization
if 'bet_step' not in st.session_state: st.session_state.bet_step = 0
if 'last_result' not in st.session_state: st.session_state.last_result = None
if 'special_history' not in st.session_state: st.session_state.special_history = []
if 'normal_history' not in st.session_state: st.session_state.normal_history = []

# --- UI Layout ---
st.title("🎯 TRX Ultra Predictor")

# ၃။ Top Alert Section (Enter နှိပ်လိုက်ရင် ဒီမှာ တန်းပေါ်မယ်)
alert_placeholder = st.container()

# ၄။ History Display Section (နှစ်ခြမ်းခွဲပြီး တစ်ခုချင်းစီ ဖျက်လို့ရအောင်လုပ်မယ်)
st.divider()
col_left, col_right = st.columns(2)

def display_history_with_delete(title, history_list, key_prefix):
    st.subheader(title)
    # နိုင်/ရှုံး Summary အစက်လေးများ
    dots = "".join(["🟢" if x == "W" else "🔴" for x in history_list])
    st.write(f"Summary: {dots if dots else '➖'}")
    
    # တစ်ခုချင်းစီ ဖျက်ရန် ခလုတ်များ
    if history_list:
        cols = st.columns(len(history_list[-10:])) # နောက်ဆုံး ၁၀ ခုပဲပြမယ်
        for i, val in enumerate(history_list[-10:]):
            with cols[i]:
                color = "green" if val == "W" else "red"
                if st.button(f"{val}\n(x)", key=f"{key_prefix}_{i}"):
                    history_list.pop(i)
                    st.rerun()

with col_left:
    display_history_with_delete("🔥 Special Patterns", st.session_state.special_history, "spec")

with col_right:
    display_history_with_delete("📊 Normal Patterns", st.session_state.normal_history, "norm")

# ၅။ Input & Prediction Logic
st.divider()
input_pat = st.text_input("Pattern ၄ လုံး ရိုက်ပြီး Enter နှိပ်ပါ (ဥပမာ- BSSS)", "").upper()

if len(input_pat) == 4:
    # Prediction ဆွဲထုတ်ခြင်း
    prediction_move = None
    is_special = False
    
    if input_pat in special_pats:
        prediction_move = special_pats[input_pat]
        is_special = True
    elif input_pat in normal_pats:
        prediction_move = normal_pats[input_pat]
    
    # ၆။ Alert Placeholder ထဲသို့ အချက်အလက်များ ပို့ခြင်း
    with alert_placeholder:
        c1, c2 = st.columns([2, 1])
        with c1:
            if is_special:
                st.error(f"🚨 SPECIAL ALERT: Next Bet **{prediction_move}**")
            elif prediction_move:
                if st.session_state.last_result == "W":
                    amt = bet_amounts[st.session_state.bet_step]
                    st.success(f"✅ WIN NEXT: Bet **{prediction_move}** | Amount: {amt} MMK")
                else:
                    st.warning("📉 LOSE SKIP: စောင့်ကြည့်ပါ")
            else:
                st.info("➖ SKIP PATTERN")
        
        with c2:
            st.write("ရလဒ် မှတ်တမ်းတင်ရန်")
            rc1, rc2 = st.columns(2)
            if rc1.button("WON (W)", use_container_width=True):
                status = "W"
                st.session_state.last_result = "W"
                if is_special: st.session_state.special_history.append(status)
                else: st.session_state.normal_history.append(status)
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
                st.rerun()
            if rc2.button("LOST (L)", use_container_width=True):
                status = "L"
                st.session_state.last_result = "L"
                if is_special: st.session_state.special_history.append(status)
                else: st.session_state.normal_history.append(status)
                st.session_state.bet_step = (st.session_state.bet_step + 1) % 5
                st.rerun()

# ၇။ Sidebar Info
with st.sidebar:
    st.write(f"Current Money Step: **{st.session_state.bet_step + 1}**")
    st.write(f"Next Amount: **{bet_amounts[st.session_state.bet_step]}**")
    if st.button("Reset All Data"):
        st.session_state.bet_step = 0
        st.session_state.special_history = []
        st.session_state.normal_history = []
        st.session_state.last_result = None
        st.rerun()
