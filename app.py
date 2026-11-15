import streamlit as st
from src.briefing import generate_briefing

st.set_page_config(page_title="Pre-Meeting Briefing Agent", page_icon="📋")
st.title("📋 Pre-Meeting Briefing Agent")

subject = st.text_input("Company or person", placeholder="e.g. Nebius")
c1, c2 = st.columns(2)
date = c1.date_input("Meeting date")
time = c2.time_input("Meeting time")
mtype = st.selectbox(
    "Meeting type",
    ["Sales call", "Partnership", "Investor meeting", "Business development", "General"],
)

if st.button("Generate briefing", type="primary"):
    if not subject.strip():
        st.warning("Enter a company or person.")
    else:
        with st.spinner("Researching the last 30 days..."):
            try:
                md = generate_briefing(subject.strip(), f"{date} {time:%H:%M}", mtype)
                st.markdown(md)
                st.download_button("Download .md", md, file_name="briefing.md")
            except Exception as e:
                st.error(f"Error: {e}")