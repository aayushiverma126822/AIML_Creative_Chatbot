import streamlit as st

st.title("Test: Affiliate Creatives Chatbot MVP")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login (dummy)")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state.logged_in = True
        st.success(f"Logged in as {email}")
else:
    st.subheader("Chat interface placeholder")
    question = st.text_input("Ask a question about creatives in affiliate marketing")
    if st.button("Send"):
        st.markdown(f"**You asked:** {question}")
        st.markdown("**Bot answer:** Creatives matter because they are the first impression, drive engagement, and improve conversion.")
