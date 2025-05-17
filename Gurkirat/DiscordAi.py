import discord
import os
from openai import OpenAI

openai_client = OpenAI(api_key="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")

DISCORD_TOKEN = "MTM3MzE1NjQ2NDE2ODAwOTc4OA.GfCm7P._F5ZhSkAiz2zNhREwcGyiGMXdNZHFv1LWo51Dw"  

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        user_input = message.content.replace(f"<@{client.user.id}>", "").strip()

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_input}],
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("⚠️ Error getting response from AI.")
            print("OpenAI error:", e)

client.run(DISCORD_TOKEN)
