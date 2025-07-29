import discord
import requests
import json

DISCORD_BOT_TOKEN = "MTM3MzE1NjQ2NDE2ODAwOTc4OA.G5BA9o.n--revASCsiG5FquVUEIwTElhU690Y1GdwHnUo"
OLLAMA_MODEL = "llama2-uncensored:7b"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

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
        reply = query_ollama(prompt)

        if reply:
            await message.channel.send(reply)
        else:
            await message.channel.send("I didn't get a response.")

client.run("MTM3MzE1NjQ2NDE2ODAwOTc4OA.G5BA9o.n--revASCsiG5FquVUEIwTElhU690Y1GdwHnUo")