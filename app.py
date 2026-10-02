import streamlit as st
import agent

st.set_page_config(page_title="Data Analyst Agent")
st.title("Olist Data Analyst Agent")
st.caption("Ask questions about Brazilian e-commerce data (2016-2018). Amounts are in BRL.")

q = st.text_input("Your question")

if st.button("Ask") and q:
    with st.spinner("Analyzing..."):
        answer = agent.ask(q)
    st.markdown(answer)
    if agent.LAST_CHART:
        st.image(agent.LAST_CHART)
    if agent.LAST_SQL:
        with st.expander("SQL used"):
            st.code(agent.LAST_SQL, language="sql")