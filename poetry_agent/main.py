from agents import Agent, Runner, trace
from connection import config
import asyncio
from dotenv import load_dotenv

load_dotenv()

# 👩‍🎤 Poet Agent (Input poetry)
poet_agent = Agent(
    name="Poet Agent",
    instructions="""
        You are a poet who writes short poems in 2 stanzas.
        Each poem should express either emotions, tell a short story,
        or be written like a drama script.
    """
)

# 📘 Lyric Analyst
lyric_agent = Agent(
    name="Lyric Analyst",
    instructions="""
        You analyze poems to check if they are Lyric poetry.
        Lyric poetry expresses personal emotions or thoughts.
        If it is, explain why. If not, say 'Not Lyric.'
    """
)

# 📖 Narrative Analyst
narrative_agent = Agent(
    name="Narrative Analyst",
    instructions="""
        You analyze poems to check if they are Narrative poetry.
        Narrative poetry tells a story with characters or events.
        If it is, explain why. If not, say 'Not Narrative.'
    """
)

# 🎭 Dramatic Analyst
dramatic_agent = Agent(
    name="Dramatic Analyst",
    instructions="""
        You analyze poems to check if they are Dramatic poetry.
        Dramatic poetry is written like a performance or a dialogue by a character.
        If it is, explain why. If not, say 'Not Dramatic.'
    """
)

# 👨‍👩‍👧 Parent Agent
parent_agent = Agent(
    name="Parent Agent",
    instructions="""
        You are the triage agent.
        Your job is to read the poem and send it to the correct analyst agent.

        - If the poem is about feelings → send to Lyric Analyst.
        - If it tells a story → send to Narrative Analyst.
        - If it sounds like a drama or stage performance → send to Dramatic Analyst.
        - If it does not match any → reject and explain.

        Respond briefly and then handoff.
    """,
    handoffs=[lyric_agent, narrative_agent, dramatic_agent]
)

# 🏁 Main runner
async def main():
    print("📝 Welcome to Poetry Analyzer!")
    print("👉 Type your 2-stanza poem below:")

    user_poem = ""
    while True:
        line = input(">>> ")
        if line.strip() == "":
            break
        user_poem += line + "\n"

    with trace("Poetry Analysis"):
        # Parent agent processes input and decides handoff
        result = await Runner.run(parent_agent, user_poem, run_config=config)

        print("\n📌 Final Analysis:")
        print("Agent:", result.last_agent.name)
        print("Response:\n", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
