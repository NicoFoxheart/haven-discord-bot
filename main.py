import discord
from discord import app_commands
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Create bot instance
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Affirmations list
affirmations = [
    "You are enough, exactly as you are. 💙",
    "This feeling will pass. You've survived 100% of your hard days. 🦊",
    "You're doing your best, and that's all anyone can ask. ✨",
    "It's okay to not be okay. You're still worthy of love and care. 🥹",
    "You are not alone. There are people who care about you. 💕",
    "Take it one breath at a time. You've got this. 🌙",
    "Your feelings are valid. All of them. 💙",
    "You are stronger than you know. 🦊",
    "Be gentle with yourself. You're doing the best you can. ✨",
    "You matter. Your life has value and purpose. 💕"
]

# Calming messages
calming_messages = [
    "Take a deep breath. You're safe right now. 🌙",
    "Ground yourself. Feel your feet on the floor. You're here. You're okay. 💙",
    "This moment will pass. Breathe through it. 🦊",
    "You've weathered storms before. You'll get through this one too. ✨",
    "It's okay to rest. It's okay to take a break. You deserve peace. 💕"
]

@client.event
async def on_ready():
    print(f'Haven Bot is online as {client.user}! 🦊💙')
    print('Ready to help your communities! ✨')
    try:
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s) ✨')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

# /breathe command
@tree.command(name="breathe", description="Guided breathing exercise to help you calm down 🌙")
async def breathe(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Let's Breathe Together",
        description="Follow along with this breathing exercise. Take your time. 💙",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Box Breathing (4-4-4-4)",
        value=(
            "**Breathe IN** for 4 seconds 🌬️\n"
            "**HOLD** for 4 seconds ⏸️\n"
            "**Breathe OUT** for 4 seconds 🍃\n"
            "**HOLD** for 4 seconds ⏸️\n\n"
            "Repeat this cycle 4 times. You're doing great. 🦊"
        ),
        inline=False
    )
    embed.set_footer(text="You're safe. You're okay. Just breathe. 💙")
    await interaction.response.send_message(embed=embed)

# /affirmation command
@tree.command(name="affirmation", description="Receive a positive affirmation 💙")
async def affirmation(interaction: discord.Interaction):
    message = random.choice(affirmations)
    embed = discord.Embed(
        title="💙 For You",
        description=message,
        color=discord.Color.green()
    )
    embed.set_footer(text="You needed to hear this today. 🦊")
    await interaction.response.send_message(embed=embed)

# /grounding command
@tree.command(name="grounding", description="5-4-3-2-1 grounding technique for anxiety 🦊")
async def grounding(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🦊 Grounding Exercise",
        description="Use your senses to ground yourself in the present moment.",
        color=discord.Color.purple()
    )
    embed.add_field(
        name="5-4-3-2-1 Technique",
        value=(
            "**5 things** you can SEE 👀\n"
            "**4 things** you can TOUCH ✋\n"
            "**3 things** you can HEAR 👂\n"
            "**2 things** you can SMELL 👃\n"
            "**1 thing** you can TASTE 👅\n\n"
            "Take your time. Notice each one. You're here. You're present. 💙"
        ),
        inline=False
    )
    embed.set_footer(text="Ground yourself. You're safe. 🦊")
    await interaction.response.send_message(embed=embed)

# /calm command
@tree.command(name="calm", description="Receive a calming message ✨")
async def calm(interaction: discord.Interaction):
    message = random.choice(calming_messages)
    embed = discord.Embed(
        title="✨ A Moment of Peace",
        description=message,
        color=discord.Color.teal()
    )
    embed.set_footer(text="Breathe. You're going to be okay. 💙")
    await interaction.response.send_message(embed=embed)

# /resources command
@tree.command(name="resources", description="Mental health crisis resources and hotlines 📞")
async def resources(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📞 Crisis Resources",
        description="You don't have to face this alone. Help is available 24/7.",
        color=discord.Color.red()
    )
    embed.add_field(
        name="🇺🇸 United States",
        value=(
            "**988 Suicide & Crisis Lifeline**\n"
            "Call/Text: 988\n"
            "Chat: 988lifeline.org\n\n"
            "**Crisis Text Line**\n"
            "Text HOME to 741741"
        ),
        inline=False
    )
    embed.add_field(
        name="🌍 International",
        value=(
            "**Worldwide directory:**\n"
            "findahelpline.com\n\n"
            "**International Association for Suicide Prevention:**\n"
            "iasp.info/resources/Crisis_Centres"
        ),
        inline=False
    )
    embed.set_footer(text="Your life matters. Please reach out. 💙")
    await interaction.response.send_message(embed=embed)

# /checkin command — opens the full check-in form
@tree.command(name="checkin", description="Complete your mental health check-in 🥹")
async def checkin(interaction: discord.Interaction):
    await interaction.response.send_modal(CheckInForm())

# /mood command
@tree.command(name="mood", description="Rate your mood from 1 to 5 and get a tailored response 🥹")
@app_commands.describe(level="Your mood right now: 1 (really struggling) to 5 (doing great)")
@app_commands.choices(level=[
    app_commands.Choice(name="1 — Really struggling 😞", value=1),
    app_commands.Choice(name="2 — Not great 😟", value=2),
    app_commands.Choice(name="3 — Okay, getting by 😐", value=3),
    app_commands.Choice(name="4 — Pretty good 🙂", value=4),
    app_commands.Choice(name="5 — Doing great! 😊", value=5),
])
async def mood(interaction: discord.Interaction, level: int):
    responses = {
        1: {
            "title": "😞 I See You — You're Not Alone",
            "description": (
                "Thank you for being honest about how you're feeling. That takes courage. 💙\n\n"
                "Right now might feel really heavy, but you don't have to carry it alone.\n\n"
                "• Try `/breathe` to slow things down 🌙\n"
                "• Try `/grounding` to feel present 🦊\n"
                "• Try `/resources` if you need someone to talk to 📞\n\n"
                "Please be gentle with yourself. You matter. 💕"
            ),
            "color": discord.Color.red()
        },
        2: {
            "title": "😟 It's Okay to Not Be Okay",
            "description": (
                "Not great days are still valid days. Your feelings are real and they matter. 💙\n\n"
                "• Try `/affirmation` for a little encouragement 💕\n"
                "• Try `/calm` for a moment of peace ✨\n"
                "• Try `/breathe` to reset 🌙\n\n"
                "You've made it through hard days before. You can do this. 🦊"
            ),
            "color": discord.Color.orange()
        },
        3: {
            "title": "😐 Getting By — That's Enough",
            "description": (
                "Sometimes just getting through the day is a win, and that's perfectly okay. ✨\n\n"
                "• Try `/affirmation` to give yourself a little boost 💙\n"
                "• Try `/checkin` to check in with yourself 🥹\n\n"
                "You're doing better than you think. Keep going. 🦊"
            ),
            "color": discord.Color.yellow()
        },
        4: {
            "title": "🙂 Pretty Good — Keep It Up!",
            "description": (
                "That's wonderful to hear! Hold onto this feeling. 💙\n\n"
                "• Try `/affirmation` to keep the good vibes going ✨\n"
                "• Share a kind word with someone else today — it spreads! 💕\n\n"
                "You're doing great. Be proud of yourself. 🦊"
            ),
            "color": discord.Color.green()
        },
        5: {
            "title": "😊 Doing Great — Love to Hear It!",
            "description": (
                "This makes my fox heart so happy! 🦊💙\n\n"
                "Remember this feeling on harder days — you're capable of joy.\n\n"
                "• Maybe share some kindness with someone who needs it today 💕\n"
                "• Try `/affirmation` to celebrate yourself ✨\n\n"
                "Keep shining. You deserve every good moment. 🌙"
            ),
            "color": discord.Color.blurple()
        }
    }

    r = responses[level]
    embed = discord.Embed(title=r["title"], description=r["description"], color=r["color"])
    embed.set_footer(text="Thank you for checking in. We care about you. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /selfcare command
@tree.command(name="selfcare", description="Quick self-care ideas to help you feel a little better 💕")
async def selfcare(interaction: discord.Interaction):
    ideas = [
        "💧 Drink a full glass of water right now. Your body will thank you.",
        "🚶 Step outside for 5 minutes. Fresh air and a change of scenery can shift your mood.",
        "🧘 Stretch for 2 minutes. Roll your shoulders, stretch your neck. Let your body breathe.",
        "🍎 Eat something nourishing. Even a small snack counts — fuel yourself.",
        "📵 Put your phone down for 10 minutes. Just exist without a screen for a moment.",
        "🛁 Wash your face or take a shower. Sometimes a reset is all you need.",
        "📖 Write down 3 things that are on your mind. Get them out of your head and onto paper.",
        "🎵 Put on a song that makes you feel something good. Let yourself feel it.",
        "🌿 Tidy one small thing in your space. A cleaner space can bring a clearer mind.",
        "🤗 Reach out to someone you trust. Connection is self-care too. 💙"
    ]
    embed = discord.Embed(
        title="💕 A Little Self-Care For You",
        description=random.choice(ideas),
        color=discord.Color.pink()
    )
    embed.set_footer(text="Taking care of yourself is never selfish. 🦊💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /cope command
@tree.command(name="cope", description="Healthy coping strategies for different feelings 🌙")
async def cope(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Healthy Coping Strategies",
        description="Different feelings need different tools. Find what fits right now. 💙",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="😰 Anxiety / Overwhelm",
        value="• Try `/breathe` for box breathing\n• Try `/grounding` for the 5-4-3-2-1 technique\n• Write down what's worrying you — it shrinks when it's on paper",
        inline=False
    )
    embed.add_field(
        name="😔 Sadness / Low mood",
        value="• Be gentle with yourself — feeling sad is okay\n• Try `/affirmation` for a reminder of your worth\n• Do one small kind thing for yourself today 💕",
        inline=False
    )
    embed.add_field(
        name="😤 Anger / Frustration",
        value="• Take 10 slow deep breaths before responding to anything\n• Move your body — walk, stretch, or shake it out\n• Write out what you're feeling, then decide if you want to send it",
        inline=False
    )
    embed.add_field(
        name="😶 Numb / Disconnected",
        value="• Hold something cold or warm — it brings you back to your body\n• Try `/grounding` to reconnect with the present\n• Be patient with yourself. Numbness is also a valid feeling. 🦊",
        inline=False
    )
    embed.set_footer(text="You're allowed to feel all of it. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /safe command
@tree.command(name="safe", description="Our community safe space values and guidelines 🤝")
async def safe(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤝 This Is a Safe Space",
        description="Here's what that means in this community. 💙",
        color=discord.Color.teal()
    )
    embed.add_field(
        name="💙 We believe in:",
        value=(
            "• **No judgment** — every feeling is valid here\n"
            "• **Kindness first** — to others and to yourself\n"
            "• **Privacy** — what's shared here stays here\n"
            "• **Respect** — for everyone's experience and journey\n"
            "• **Support over advice** — listening matters more than fixing"
        ),
        inline=False
    )
    embed.add_field(
        name="🦊 Remember:",
        value=(
            "You don't have to share more than you're comfortable with.\n"
            "You don't have to be 'bad enough' to ask for support.\n"
            "You belong here, exactly as you are. 💕"
        ),
        inline=False
    )
    embed.set_footer(text="You are safe here. 🦊💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /sleep command
@tree.command(name="sleep", description="Sleep tips for when rest feels impossible 🌙")
async def sleep(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Having Trouble Sleeping?",
        description="Here are some gentle things that can help. 💙",
        color=discord.Color.dark_blue()
    )
    embed.add_field(
        name="Before bed:",
        value=(
            "• Put screens away 30 mins before sleeping if you can\n"
            "• Try the `/breathe` box breathing — it calms your nervous system\n"
            "• Keep your room cool and dark if possible\n"
            "• Write down tomorrow's worries so your brain can let go of them"
        ),
        inline=False
    )
    embed.add_field(
        name="If you can't switch off your mind:",
        value=(
            "• Try the `/grounding` exercise lying down\n"
            "• Count backwards slowly from 300 by 3s — it occupies the anxious part of your brain\n"
            "• Remind yourself: resting quietly still helps your body, even without sleep 🦊"
        ),
        inline=False
    )
    embed.add_field(
        name="If you wake up at night:",
        value=(
            "• Don't check the time — it creates pressure\n"
            "• Focus on slow breathing rather than trying to force sleep\n"
            "• Be kind to yourself. Sleep struggles are incredibly common. 💕"
        ),
        inline=False
    )
    embed.set_footer(text="Rest well. You deserve peaceful sleep. 🌙💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /hug command
@tree.command(name="hug", description="Send a warm virtual hug to someone 🤗")
@app_commands.describe(member="Who do you want to hug?")
async def hug(interaction: discord.Interaction, member: discord.Member):
    hug_messages = [
        f"🤗 {interaction.user.display_name} sends a big warm hug to {member.mention}! You are loved. 💙",
        f"🤗 {member.mention} — {interaction.user.display_name} wants you to know they're thinking of you. Here's a hug! 💕",
        f"🦊 A little fox hug from {interaction.user.display_name} to {member.mention}! You matter. 💙",
        f"🤗 {interaction.user.display_name} is wrapping {member.mention} in the warmest hug. You're not alone. ✨",
        f"💕 {member.mention} just got a hug from {interaction.user.display_name}! Sending you all the love. 🦊💙",
    ]
    await interaction.response.send_message(random.choice(hug_messages))

# /gratitude command
@tree.command(name="gratitude", description="A gentle gratitude prompt to shift your headspace ✨")
async def gratitude(interaction: discord.Interaction):
    prompts = [
        "Think of **one person** who made you feel seen or cared for recently. It could be a small moment. 💙",
        "What is **one thing your body did for you today** that you might usually take for granted?",
        "Think of **one small moment of beauty** you noticed recently — a sound, a smell, a feeling.",
        "What is **one thing you're quietly proud of yourself for** — even if no one else knows about it? 🦊",
        "Think of **one thing that brought you even a tiny bit of comfort** today. It doesn't have to be big.",
        "What is **one skill or quality you have** that has helped you through hard times? 💕",
        "Think of **one person you're grateful exists** in the world — and why. ✨",
        "What is **one thing about where you are right now** that you can appreciate, however small?"
    ]
    embed = discord.Embed(
        title="✨ A Moment of Gratitude",
        description=(
            f"{random.choice(prompts)}\n\n"
            "Take a moment. Really sit with it. You don't have to share — this is just for you. 💙"
        ),
        color=discord.Color.gold()
    )
    embed.set_footer(text="Small gratitude adds up. You're doing something good for yourself. 🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /journal command
@tree.command(name="journal", description="Privately log how you're feeling — only you can see this 🥹")
@app_commands.describe(feeling="How are you feeling right now? Share as much or as little as you'd like.")
async def journal(interaction: discord.Interaction, feeling: str):
    embed = discord.Embed(
        title="📓 Your Private Journal Entry",
        description=feeling,
        color=discord.Color.blurple()
    )
    embed.set_footer(text="This is just for you. Your feelings are valid. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /checkup command - NEW!
@tree.command(name="checkup", description="Check up on someone in your community 💙")
@app_commands.describe(member="Who do you want to check on?")
async def checkup(interaction: discord.Interaction, member: discord.Member):
    checkup_messages = [
        f"💙 Hey {member.mention} — {interaction.user.display_name} is thinking about you. How are you really doing?",
        f"👀 {member.mention}, {interaction.user.display_name} wanted to check in on you. Everything okay? 🦊",
        f"🦊 {interaction.user.display_name} is checking on you, {member.mention}. You don't have to be okay — just be honest. 💙",
        f"💙 {member.mention} — {interaction.user.display_name} cares about you. How's your heart today?",
        f"🌙 Hey {member.mention}, {interaction.user.display_name} noticed you and wanted to see how you're holding up. 💙",
    ]
    await interaction.response.send_message(random.choice(checkup_messages))

# /fortune command - NEW!
@tree.command(name="fortune", description="Receive a gentle uplifting fortune cookie message 🥠")
async def fortune(interaction: discord.Interaction):
    fortunes = [
        "🥠 Your kindness will return to you when you need it most.",
        "🥠 The storm you're in will pass. You've weathered worse.",
        "🥠 Someone is thinking of you right now, even if you don't know it. 💙",
        "🥠 Small steps still move you forward. Keep going. 🦊",
        "🥠 You are exactly where you need to be, even if it doesn't feel like it.",
        "🥠 The universe is conspiring to help you, not hurt you. ✨",
        "🥠 Your presence matters more than you know. 💙",
        "🥠 Tomorrow holds something good for you. Trust it. 🌙",
        "🥠 You will find rest soon. Hold on a little longer.",
        "🥠 The weight you carry will lighten. Be patient with yourself. 🦊",
        "🥠 You are not behind. You are not failing. You are surviving. 💙",
        "🥠 Someone's life is better because you exist. ✨",
        "🥠 Your feelings are temporary. Your worth is permanent. 💙",
        "🥠 The sun will rise again tomorrow. So will you. 🌅",
        "🥠 You are doing better than you think you are. 🦊💙"
    ]
    embed = discord.Embed(
        title="🥠 Your Fortune",
        description=random.choice(fortunes),
        color=discord.Color.gold()
    )
    embed.set_footer(text="You opened this fortune at the right time. 💙")
    await interaction.response.send_message(embed=embed)

# /pet command - NEW!
@tree.command(name="pet", description="A comforting story about a little animal friend 🦊")
async def pet(interaction: discord.Interaction):
    pet_stories = [
        {
            "title": "🦊 The Little Fox",
            "story": (
                "There's a little fox who lives at the edge of the forest. "
                "Every night, it sits under the stars and thinks about the people it cares about.\n\n"
                "Tonight, it's thinking about you. It wants you to know that even when you feel alone, "
                "you're not. The fox is out there, sending you quiet strength through the dark.\n\n"
                "You're going to be okay. The fox believes in you. 🦊💙"
            )
        },
        {
            "title": "🐱 The Sleepy Cat",
            "story": (
                "There's a little cat curled up on a warm windowsill, watching the world go by.\n\n"
                "It doesn't worry about tomorrow. It doesn't stress about yesterday. "
                "It just exists, peacefully, in this moment.\n\n"
                "The cat wants to remind you: it's okay to just be. "
                "You don't have to do anything right now. Just rest. Just breathe. 🐱💙"
            )
        },
        {
            "title": "🐶 The Loyal Dog",
            "story": (
                "There's a dog sitting by the door, waiting for its person to come home.\n\n"
                "It doesn't care if they had a bad day. It doesn't care if they're struggling. "
                "All it cares about is: they're here. They came back.\n\n"
                "You came back today too. You're still here. And that's enough. "
                "You're enough. 🐶💙"
            )
        },
        {
            "title": "🦊 The Brave Fox",
            "story": (
                "There's a little fox who's been through a lot. Harsh winters, hungry nights, storms that felt endless.\n\n"
                "But every morning, it wakes up and keeps going. Not because it's fearless — "
                "but because it's brave.\n\n"
                "You're like that fox. You've been through hard things. And you're still here. "
                "That's bravery. That's strength. 🦊💙"
            )
        },
        {
            "title": "🐱 The Curious Cat",
            "story": (
                "There's a little cat who finds wonder in the smallest things. "
                "A leaf. A shadow. A beam of light.\n\n"
                "It doesn't need grand things to feel joy. It finds magic in the ordinary.\n\n"
                "Maybe today, you can be like that cat. Find one small thing that feels good. "
                "That's enough. 🐱✨"
            )
        },
        {
            "title": "🐶 The Gentle Dog",
            "story": (
                "There's a dog who knows when someone is sad. It doesn't try to fix it. "
                "It doesn't give advice. It just sits close. Just stays.\n\n"
                "Sometimes that's all we need — someone to just be there.\n\n"
                "I'm here. The fox is here. You're not alone. 🐶💙"
            )
        },
        {
            "title": "🦊 The Tired Fox",
            "story": (
                "There's a little fox who's been running all day. It's exhausted. Its paws hurt. "
                "It just wants to rest.\n\n"
                "So it finds a quiet spot under a tree, curls up, and closes its eyes.\n\n"
                "It's okay to be tired. It's okay to stop. Rest isn't giving up — it's taking care of yourself. "
                "🦊🌙"
            )
        },
        {
            "title": "🐱 The Window Cat",
            "story": (
                "There's a cat who loves to watch the rain. It sits at the window, safe and warm inside, "
                "watching the storm outside.\n\n"
                "The rain doesn't scare it. It knows it's safe.\n\n"
                "You're safe too. The storm is outside. You're inside. You're okay. 🐱🌧️"
            )
        }
    ]
    
    story = random.choice(pet_stories)
    embed = discord.Embed(
        title=story["title"],
        description=story["story"],
        color=discord.Color.orange()
    )
    embed.set_footer(text="You are loved. You are seen. You matter. 💙🦊")
    await interaction.response.send_message(embed=embed)

# Check-in channel ID — set CHECKIN_CHANNEL_ID in Secrets
CHECKIN_CHANNEL_ID = os.environ.get("CHECKIN_CHANNEL_ID")

# Single full check-in modal
class CheckInForm(discord.ui.Modal, title="📋 Mental Health Check-In"):
    feeling_words = discord.ui.TextInput(
        label="Feeling word(s)",
        style=discord.TextStyle.short,
        placeholder="e.g. empty, lonely, anxious, hopeful...",
        required=True,
        max_length=150
    )
    scales = discord.ui.TextInput(
        label="Mood, Esteem, Self-harm, Harm others (0-10)",
        style=discord.TextStyle.paragraph,
        placeholder="Mood: 5 | Self-esteem: 4 | Self-harm: 0 | Harm-others: 0",
        required=True,
        max_length=200
    )
    doing_now = discord.ui.TextInput(
        label="Doing now? / Struggling with?",
        style=discord.TextStyle.paragraph,
        placeholder="Doing: listening to music\nStruggling: depression, hard to breathe",
        required=True,
        max_length=500
    )
    coping_and_care = discord.ui.TextInput(
        label="Coping skills / Self-care / Smile / Felt good",
        style=discord.TextStyle.paragraph,
        placeholder="Coping: music / Self-care: went outside / Smile: talked to Nico / Felt good: music",
        required=True,
        max_length=400
    )
    need_now = discord.ui.TextInput(
        label="What do you need right now?",
        style=discord.TextStyle.short,
        placeholder="e.g. rest, support, a distraction... or 'I don't know'",
        required=True,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"📋 Check In: {interaction.user.display_name}",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.add_field(name="Feeling word(s):", value=self.feeling_words.value, inline=False)
        embed.add_field(name="─────────────────────", value="\u200b", inline=False)
        embed.add_field(name="Scales (0-10):", value=self.scales.value, inline=False)
        embed.add_field(name="─────────────────────", value="\u200b", inline=False)
        embed.add_field(name="Right now / Struggling:", value=self.doing_now.value, inline=False)
        embed.add_field(name="Coping, care, smile, felt good:", value=self.coping_and_care.value, inline=False)
        embed.add_field(name="What I need:", value=self.need_now.value, inline=False)
        embed.set_footer(text="Thank you for checking in. You are seen and valued. 🦊💙")

        await interaction.response.send_message(
            "Your check-in has been submitted. Thank you for sharing. 💙🦊",
            ephemeral=True
        )

        if CHECKIN_CHANNEL_ID:
            channel = interaction.guild.get_channel(int(CHECKIN_CHANNEL_ID))
            if channel:
                await channel.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed)

# Keep-alive web server so Railway deployment health checks pass
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Haven Bot is running!")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_health_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# Run the bot
TOKEN = os.environ.get('DISCORD_TOKEN')
if TOKEN:
    client.run(TOKEN)
else:
    print("ERROR: No token found! Add DISCORD_TOKEN to Secrets.")
