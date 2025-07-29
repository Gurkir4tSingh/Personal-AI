import discord
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("MTM3MzE1NjQ2NDE2ODAwOTc4OA.G5BA9o.n--revASCsiG5FquVUEIwTElhU690Y1GdwHnUo")

# Ollama Model
OLLAMA_MODEL = "llama3"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Query Ollama locally
def query_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt},
            stream=True
        )

        full_reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    full_reply += data.get("response", "")
                except json.JSONDecodeError as e:
                    print("JSON decode error:", e)
                    print("Offending line:", line.decode('utf-8'))

        return full_reply.strip()
    except Exception as e:
        return f"Error contacting model: {str(e)}"

# Search using DuckDuckGo Instant Answer API
def search_web_duckduckgo(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&skip_disambig=1"
    try:
        response = requests.get(url)
        data = response.json()

        abstract = data.get("AbstractText", "")
        related = data.get("RelatedTopics", [])

        if abstract:
            return abstract
        elif related:
            summaries = []
            for topic in related[:3]:  # limit to 3 suggestions
                if "Text" in topic:
                    summaries.append(topic["Text"])
                elif "Topics" in topic:  # nested related topics
                    for subtopic in topic["Topics"][:2]:
                        summaries.append(subtopic.get("Text", ""))
            return "\n".join(summaries)
        else:
            return "No relevant search results found."
    except Exception as e:
        return f"Error during search: {str(e)}"

# Trigger search for informational queries
def needs_web_search(prompt):
    keywords = ["what is", "who is", "define", "explain", "how does", "capital of", "population", "meaning of"]
    return any(kw in prompt.lower() for kw in keywords)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not prompt:
            await message.channel.send("Ask me something.")
            return

        await message.channel.typing()

        # Check if web search is needed
        if needs_web_search(prompt):
            search_result = search_web_duckduckgo(prompt)
            prompt = f"Use the following info to answer:\n\n{search_result}\n\nQuestion: {prompt}"

        # Query the model
        reply = query_ollama(prompt)

        if reply:
            await message.channel.send(reply)
        else:
            await message.channel.send("I didn't get a response.")

client.run("MTM3MzE1NjQ2NDE2ODAwOTc4OA.G5BA9o.n--revASCsiG5FquVUEIwTElhU690Y1GdwHnUo")
