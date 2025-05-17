import discord
import openai

openai.api_key = "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"
DISCORD_TOKEN = "MTM3MzE1NjQ2NDE2ODAwOTc4OA.G0B-Qh.PZ9t-jAjwoRLph3Tpz497zecv8rp5Vbnm9n9F8"

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )

        reply = response["choices"][0]["message"]["content"]
        await message.channel.send(reply)

client.run(DISCORD_TOKEN)
