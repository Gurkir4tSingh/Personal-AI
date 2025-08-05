import discord
import requests
import json
from duckduckgo_search import DDGS

# ===== CONFIG =====
DISCORD_BOT_TOKEN = "discord DISCORD_BOT_TOKEN"
OLLAMA_MODEL = "mistral:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

# ===== DISCORD BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ===== WEB SEARCH FUNCTION =====
def web_search(query, max_results=3):
    """Search DuckDuckGo and return a text summary of results."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No relevant search results found."

        summaries = []
        for r in results:
            summaries.append(f"{r['title']} - {r['href']}\n{r['body']}")
        return "\n\n".join(summaries)
    except Exception as e:
        return f"Web search error: {str(e)}"

# ===== OLLAMA QUERY FUNCTION =====
def query_ollama(prompt):
    """Send a prompt to Ollama's API and return the generated text."""
    try:
        response = requests.post(
            OLLAMA_URL,
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

# ===== DISCORD EVENTS =====
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

        # Check if user wants to search the web
        if prompt.lower().startswith("search from web"):
            search_query = prompt[len("search from web"):].strip()
            search_results = web_search(search_query, max_results=3)

            combined_prompt = (
                
            )

            reply = query_ollama(combined_prompt)
        else:
            # Normal mode (no search)
            reply = query_ollama(prompt)

        if reply:
            await message.channel.send(reply)
        else:
            await message.channel.send("I didn't get a response.")

# ===== RUN BOT =====
client.run("discord token")
