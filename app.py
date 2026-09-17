
import streamlit as st
from pipeline import run_research_pipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide"
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .report-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🔬 ResearchMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Multi-Agent AI Research Assistant</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header("⚙️ Settings")

    st.info(
        "ResearchMind uses multiple AI agents to search, "
        "read, write and review research reports."
    )

    st.markdown("### Pipeline Steps")
    st.write("1. 🔎 Search Agent")
    st.write("2. 🔗 Source Extraction")
    st.write("3. 📖 Reader Agent")
    st.write("4. ✍️ Writer Agent")
    st.write("5. 🧐 Critic Agent")


# =========================================================
# USER INPUT
# =========================================================

st.subheader("📝 Enter Your Research Topic")

topic = st.text_area(
    "What would you like to research?",
    placeholder=(
        "Example: Applications of Generative AI in Education"
    ),
    height=120
)


# =========================================================
# RUN PIPELINE
# =========================================================

if st.button("🚀 Generate Research Report", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        with st.spinner(
            "ResearchMind is searching, reading and "
            "generating your report..."
        ):

            result = run_research_pipeline(topic.strip())

        if "error" in result:
            st.error("The research pipeline encountered an error.")
            st.code(result["error"])

        else:
            st.success("Research report generated successfully!")

            # =================================================
            # RESULTS TABS
            # =================================================

            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "📄 Final Report",
                    "🔎 Search Results",
                    "🔗 Sources",
                    "🧐 Critic Feedback"
                ]
            )

            with tab1:
                st.markdown("## 📄 Final Research Report")
                st.markdown(result["report"])

                st.download_button(
                    label="📥 Download Report",
                    data=result["report"],
                    file_name="research_report.txt",
                    mime="text/plain"
                )

            with tab2:
                st.markdown("## 🔎 Search Results")
                st.write(result["search_results"])

            with tab3:
                st.markdown("## 🔗 Source URLs")

                if result["urls"]:
                    for index, url in enumerate(
                        result["urls"],
                        start=1
                    ):
                        st.write(f"{index}. {url}")
                else:
                    st.info("No source URLs were found.")

            with tab4:
                st.markdown("## 🧐 Critic Feedback")
                st.markdown(result["feedback"])

            st.metric(
                "Total Execution Time",
                f"{result['execution_time']:.2f} seconds"
            )