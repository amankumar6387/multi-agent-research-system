
import re
import time

from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


# =========================================================
# URL EXTRACTION
# =========================================================

def extract_urls(text: str) -> list[str]:
    """Extract unique and clean URLs from text."""

    pattern = r"https?://[^\s]+"
    urls = re.findall(pattern, text)

    unique_urls = []

    for url in urls:
        # Remove common punctuation and Markdown symbols
        url = url.rstrip(".,)>]}\"'")

        if url not in unique_urls:
            unique_urls.append(url)

    return unique_urls


# =========================================================
# TIMING HELPER
# =========================================================

def show_time(step_name: str, start_time: float):
    elapsed = time.perf_counter() - start_time
    print(f"✅ {step_name} completed in {elapsed:.2f} seconds")


# =========================================================
# MAIN RESEARCH PIPELINE
# =========================================================

def run_research_pipeline(topic: str) -> dict:

    total_start = time.perf_counter()

    state = {
        "topic": topic,
        "search_results": "",
        "urls": [],
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "execution_time": 0,
    }

    print("\n" + "=" * 70)
    print("🔬 RESEARCHMIND")
    print("MULTI-AGENT RESEARCH SYSTEM")
    print("=" * 70)
    print(f"\n📌 Topic: {topic}")

    try:

        # =====================================================
        # STEP 1: SEARCH AGENT
        # =====================================================

        print("\n" + "-" * 70)
        print("🔎 STEP 1: SEARCH AGENT")
        print("-" * 70)

        step_start = time.perf_counter()

        search_agent = build_search_agent()

        print("⏳ Searching the web...")

        search_result = search_agent.invoke({
            "messages": [
                (
                    "user",
                    f"""
Research this topic:

{topic}

Find recent and reliable information.

Return:
- Important findings
- Relevant sources
- Source URLs

Keep the response concise.
"""
                )
            ]
        })

        state["search_results"] = (
            search_result["messages"][-1].content
        )

        show_time("Search", step_start)

        # =====================================================
        # STEP 2: URL EXTRACTION
        # =====================================================

        print("\n" + "-" * 70)
        print("🔗 STEP 2: SOURCE EXTRACTION")
        print("-" * 70)

        step_start = time.perf_counter()

        urls = extract_urls(state["search_results"])

        # Use only two URLs to reduce token usage
        state["urls"] = urls[:2]

        print(f"✅ Found {len(state['urls'])} sources.")

        for index, url in enumerate(state["urls"], start=1):
            print(f"{index}. {url}")

        show_time("URL extraction", step_start)

        # =====================================================
        # STEP 3: READER AGENT
        # =====================================================

        print("\n" + "-" * 70)
        print("📖 STEP 3: READER AGENT")
        print("-" * 70)

        step_start = time.perf_counter()

        if not state["urls"]:

            print("⚠️ No URLs found. Skipping reader agent.")

            state["scraped_content"] = (
                "No source URLs were found."
            )

        else:

            reader_agent = build_reader_agent()

            url_text = "\n".join(
                f"{index}. {url}"
                for index, url in enumerate(
                    state["urls"],
                    start=1
                )
            )

            print("⏳ Reading web sources...")

            reader_prompt = f"""
Topic: {topic}

Read these sources using the scrape_url tool:

{url_text}

Extract only:
1. Important facts
2. Key findings
3. Useful statistics
4. Recent developments

Do not invent information.
Mention the source URL for each finding.
Keep the response under 500 words.
"""

            reader_result = reader_agent.invoke({
                "messages": [
                    ("user", reader_prompt)
                ]
            })

            state["scraped_content"] = (
                reader_result["messages"][-1].content
            )

        show_time("Reading", step_start)

        # =====================================================
        # STEP 4: WRITER AGENT
        # =====================================================

        print("\n" + "-" * 70)
        print("✍️ STEP 4: WRITER AGENT")
        print("-" * 70)

        step_start = time.perf_counter()

        research_material = f"""
SEARCH RESULTS:
{state["search_results"]}

SOURCE URLS:
{chr(10).join(state["urls"])}

DETAILED RESEARCH:
{state["scraped_content"]}
"""

        print("⏳ Generating report...")

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_material
        })

        show_time("Report generation", step_start)

        # =====================================================
        # STEP 5: CRITIC AGENT
        # =====================================================

        print("\n" + "-" * 70)
        print("🧐 STEP 5: CRITIC AGENT")
        print("-" * 70)

        step_start = time.perf_counter()

        print("⏳ Reviewing report...")

        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        show_time("Review", step_start)

        # =====================================================
        # FINAL RESULT
        # =====================================================

        total_time = time.perf_counter() - total_start
        state["execution_time"] = total_time

        print("\n" + "=" * 70)
        print("🎉 RESEARCH PIPELINE COMPLETED")
        print("=" * 70)

        print(f"\n⏱️ Total execution time: {total_time:.2f} seconds")

        print("\n📄 FINAL REPORT")
        print("-" * 70)
        print(state["report"])

        print("\n🧐 CRITIC FEEDBACK")
        print("-" * 70)
        print(state["feedback"])

        return state

    except Exception as error:

        elapsed = time.perf_counter() - total_start

        print("\n❌ PIPELINE ERROR")
        print(f"Error: {error}")
        print(f"Time before failure: {elapsed:.2f} seconds")

        # Return the current state instead of immediately crashing
        state["error"] = str(error)
        state["execution_time"] = elapsed

        return state


# =========================================================
# TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    print("\n🔬 ResearchMind")

    topic = input("\nEnter a research topic: ").strip()

    if not topic:
        print("❌ Please enter a research topic.")
    else:
        result = run_research_pipeline(topic)

        if "error" in result:
            print("\n⚠️ Pipeline stopped because of an error.")
        else:
            print("\n✅ Pipeline finished successfully.")