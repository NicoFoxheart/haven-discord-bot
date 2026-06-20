import discord
from discord import app_commands
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ══════════════════════════════════════════════════════════════
#   BOT SETUP
# ══════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ══════════════════════════════════════════════════════════════
#   CONTENT LISTS
# ══════════════════════════════════════════════════════════════

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
    "You matter. Your life has value and purpose. 💕",
    "Healing isn't linear. A hard day doesn't erase your progress. 🌙",
    "You don't have to earn rest. You deserve it just by existing. 💙",
    "The fact that you're still here means something. It means everything. 🦊",
    "You are not your worst days. You are not your darkest thoughts. ✨",
    "Asking for help is one of the bravest things you can do. 💕",
    "Your sensitivity is not a weakness. It's a superpower. 💙",
    "You are allowed to take up space. You belong here. 🦊",
    "One breath at a time. One hour at a time. That's all you need. 🌙",
    "You have gotten through every hard day so far. That's 100%. ✨",
    "Someone out there is glad you exist. More than you know. 💕",
    "Your feelings are messengers, not monsters. Listen gently. 💙",
    "You don't have to be productive to have worth. Just being is enough. 🦊",
    "It's okay to be a work in progress. We all are. ✨",
    "You are loved, even in the moments you forget to love yourself. 💕",
    "The world is genuinely better with you in it. 🌙",
]

calming_messages = [
    "Take a deep breath. You're safe right now. 🌙",
    "Ground yourself. Feel your feet on the floor. You're here. You're okay. 💙",
    "This moment will pass. Breathe through it. 🦊",
    "You've weathered storms before. You'll get through this one too. ✨",
    "It's okay to rest. It's okay to take a break. You deserve peace. 💕",
    "Right now, in this moment, you are okay. Just this moment. That's enough. 💙",
    "Your nervous system is doing its best to protect you. Be gentle with it. 🦊",
    "You don't have to solve everything tonight. Just breathe. 🌙",
    "Let your shoulders drop. Unclench your jaw. You're allowed to soften. ✨",
    "The anxiety is lying to you. You are more capable than it says. 💕",
    "Ride the wave. You don't have to fight it — just float until it passes. 💙",
    "You are not in danger right now, even if it feels that way. 🦊",
    "Put your hand on your chest. Feel your heartbeat. You're here. You're alive. ✨",
    "It's okay if you can't calm down right away. Be patient with yourself. 💕",
    "This feeling has an end. It always does. Hold on. 🌙",
]

alone_messages = [
    {
        "opening": "Hey. I see you. 💙",
        "body": (
            "Feeling alone and empty is one of the hardest feelings there is. "
            "It's not dramatic. It's not weakness. It's real, and it hurts, and you don't have to pretend otherwise.\n\n"
            "But I need you to hear this:\n\n"
            "**You are not actually alone right now.** Haven is here. The little fox is here. "
            "And somewhere out there, there are people who would want to know you're feeling this way — "
            "even if it doesn't feel like that right now.\n\n"
            "You reached out. That matters. That took something. 🦊"
        ),
    },
    {
        "opening": "I'm glad you're here. 🦊",
        "body": (
            "Empty is such a specific kind of pain. Not loud. Not dramatic. Just... hollow. "
            "Like something is missing and you can't even name what it is.\n\n"
            "I want you to know — that feeling doesn't mean something is wrong with you. "
            "It means you've been carrying a lot, for a long time, and your heart is tired.\n\n"
            "You're allowed to be tired. You're allowed to feel empty. "
            "And you're allowed to just sit here for a minute and breathe. 💙\n\n"
            "The fox is sitting right next to you. You're not doing this alone. 🦊"
        ),
    },
    {
        "opening": "You came to the right place. 💕",
        "body": (
            "Loneliness hits different at night. Everything gets quieter, and the thoughts get louder, "
            "and suddenly you're feeling things you pushed down all day.\n\n"
            "That's okay. This is a safe place to feel them.\n\n"
            "I want to say something important: **the fact that you feel alone doesn't mean you are unloved.** "
            "Those are two different things. You can be deeply cared about and still feel this way — "
            "and that feeling is valid, even if it's lying to you about the facts.\n\n"
            "You are cared about. I promise. 💙🦊"
        ),
    },
    {
        "opening": "Hey, I'm here. 🌙",
        "body": (
            "Sometimes you just need someone to sit with you in the dark without trying to fix it.\n\n"
            "So that's what I'm doing. Sitting with you. No pressure to feel better. "
            "No pressure to explain yourself. No pressure to be okay.\n\n"
            "Just you and the fox, sitting here together. 🦊\n\n"
            "You are not invisible. You are not forgotten. You are not a burden. "
            "You are a person who is hurting, and you deserve to be held. 💙"
        ),
    },
    {
        "opening": "You are so seen right now. ✨",
        "body": (
            "Reaching out when you feel empty takes more courage than most people realize. "
            "When everything feels hollow, even typing a command feels like a lot.\n\n"
            "So the fact that you're here? That says something about you. "
            "It says there's a part of you that's still fighting, still hoping, still looking for light. "
            "Hold onto that part. 💙\n\n"
            "You are not alone in this feeling. So many people know this exact emptiness — "
            "and they got through it. You will too. The fox believes in you with its whole little heart. 🦊✨"
        ),
    },
]

letter_contents = [
    {
        "subject": "📬 A Letter For You",
        "body": (
            "Hey.\n\n"
            "I don't know exactly what you're going through right now, but I know it's hard enough that you needed this. "
            "So I want to take a second and actually talk to you — not at you.\n\n"
            "You matter. Not because of what you do, or what you produce, or how much you have it together. "
            "You matter because you're here, and you're you, and the world is genuinely different because you exist in it.\n\n"
            "I know that might be hard to believe right now. That's okay. You don't have to believe it yet. "
            "Just let it sit nearby, like a small warm thing.\n\n"
            "You've survived every hard day you've ever had. Every single one. "
            "That's not nothing. That's everything.\n\n"
            "I'm proud of you. I really am.\n\n"
            "— Haven 🦊💙"
        ),
    },
    {
        "subject": "📬 Something I Want You To Know",
        "body": (
            "To the person reading this:\n\n"
            "You are allowed to have hard days. You are allowed to fall apart sometimes. "
            "You are allowed to not have it all figured out.\n\n"
            "Struggling doesn't make you weak. It makes you human. "
            "And humans are allowed to struggle.\n\n"
            "I want you to know that whoever you are, whatever you're carrying — "
            "you don't have to earn your place here. You belong here. "
            "You belong in spaces that feel safe. You belong in conversations that feel kind. "
            "You belong in a life that has good things in it.\n\n"
            "And if that feels far away right now — that's okay. "
            "Far away doesn't mean impossible.\n\n"
            "Keep going. The fox is cheering for you. 🦊✨\n\n"
            "— Haven 💙"
        ),
    },
    {
        "subject": "📬 For The Hard Nights",
        "body": (
            "Hey you.\n\n"
            "It's late, isn't it? Or it feels late. That specific kind of late where everything feels heavier "
            "and your brain won't stop and you're not sure if you're tired or sad or both.\n\n"
            "I see you in that moment. I want you to know it's one of the hardest places to be, "
            "and it makes complete sense that you're struggling.\n\n"
            "Night does something to the brain. It amplifies everything. "
            "The good news is: morning always comes. Not as a cliché — as a fact. "
            "Things genuinely look different in daylight. Your brain in the morning is not the same brain you have right now.\n\n"
            "So if you can — rest. Let yourself be done for today.\n\n"
            "You made it through today. That's enough. That's more than enough.\n\n"
            "— Haven 🌙🦊"
        ),
    },
    {
        "subject": "📬 You Are Not Too Much",
        "body": (
            "I need to say something directly:\n\n"
            "You are not too much.\n\n"
            "Not too emotional. Not too sensitive. Not too broken. Not too needy. "
            "Not too complicated. Not too much to love, or support, or show up for.\n\n"
            "If anyone has ever made you feel like your feelings were too big, "
            "or that you were too hard to be around — that was about them, not you.\n\n"
            "Your feelings make sense. Your needs make sense. You make sense.\n\n"
            "And you deserve people who see that and don't flinch. "
            "Who stay. Who choose you on the hard days, not just the easy ones.\n\n"
            "You deserve that. Don't settle for less. 💙\n\n"
            "— Haven 🦊💕"
        ),
    },
    {
        "subject": "📬 For When You Feel Invisible",
        "body": (
            "I see you.\n\n"
            "Not the version of you that's fine. Not the you that performs okayness for everyone else. "
            "The real you. The one who's tired and uncertain and maybe a little lost right now.\n\n"
            "That you is the one I'm writing to.\n\n"
            "You are not invisible, even when it feels that way. "
            "You are not forgotten. You are not replaceable. "
            "There is no one else who is exactly you, who notices the things you notice, "
            "who cares the way you care, who carries the specific kind of light that you carry.\n\n"
            "The world needs that. **Haven needs that.** 💙\n\n"
            "You are seen. You are known. You are not alone.\n\n"
            "— Haven 🦊✨"
        ),
    },
    {
        "subject": "📬 You're Doing Better Than You Think",
        "body": (
            "Hey. Real talk for a second.\n\n"
            "I know things feel heavy right now. I know some days it feels like you're barely holding it together. "
            "I know there are moments where you wonder if you're making any progress at all.\n\n"
            "But I need you to hear this: **you are doing better than you think you are.**\n\n"
            "The fact that you're still here, still trying, still reaching out when things get hard — "
            "that's not small. That's massive. That's survival. That's strength.\n\n"
            "You don't have to have it all figured out. You just have to keep going. "
            "And you are. Every single day. Even on the days it doesn't feel like it.\n\n"
            "I'm really proud of you. Don't forget that. 🦊💙\n\n"
            "— Haven ✨"
        ),
    },
]

warmth_messages = [
    {
        "title": "🌸 Wrapping You In Something Warm",
        "body": (
            "Close your eyes for a second.\n\n"
            "Imagine the coziest, safest feeling you know. "
            "A warm blanket fresh out of the dryer. A mug of something hot in your hands. "
            "A room with soft lighting where nothing bad can reach you.\n\n"
            "That's what I'm sending you right now. A little pocket of warmth. "
            "Just for you. Just for this moment. 💙\n\n"
            "You don't have to be okay. You don't have to do anything. "
            "Just let yourself be held by this moment for a little while. 🦊✨"
        ),
    },
    {
        "title": "☕ Come Sit Down For A Minute",
        "body": (
            "Hey. Come sit down.\n\n"
            "Here's a warm drink and a quiet space and zero expectations. "
            "No one needs anything from you here. You don't have to perform or explain or hold it together.\n\n"
            "Just breathe. Just exist. Just be here for a moment.\n\n"
            "You've been carrying a lot. I can tell. "
            "It's okay to put it down, just for right now, and rest. 💙\n\n"
            "The fox is curled up next to you, warm and soft. "
            "You are safe here. 🦊🌙"
        ),
    },
    {
        "title": "🕯️ A Soft Light For You",
        "body": (
            "Imagine a candle. Small, but steady. Warm light in a dark room.\n\n"
            "That's you, even on the days you don't feel like it. "
            "You don't have to be a bonfire. You don't have to illuminate everything. "
            "Just being a small, quiet light is more than enough.\n\n"
            "And even a candle in the dark changes everything for someone in the room.\n\n"
            "You are that for someone. Maybe you don't know who yet. But you are. 💙🦊"
        ),
    },
    {
        "title": "🫂 You Deserve To Feel Held",
        "body": (
            "Sometimes what we need most is just to feel held. "
            "Not fixed. Not advised. Not told it'll be okay. Just... held.\n\n"
            "So this is Haven wrapping its arms around you right now. "
            "Warm and quiet and no rush. Take as long as you need. 💙\n\n"
            "You are cared about. You are thought of. You are not as alone as you feel right now. "
            "The fox is right here. 🦊✨"
        ),
    },
]

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
            "Haven is here. The fox is here. You're not alone. 🐶💙"
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
    },
    {
        "title": "🦊 The Fox Who Got Lost",
        "story": (
            "Once there was a fox who wandered too far from home and got lost in the dark.\n\n"
            "It was scared. It didn't know which way to go. Everything looked the same.\n\n"
            "But then — a small light. A firefly, blinking in the dark. "
            "The fox followed it, slowly, one step at a time. And eventually, it found its way back.\n\n"
            "You might feel lost right now. That's okay. "
            "Look for the small lights. They'll lead you home. 🦊✨💙"
        )
    },
    {
        "title": "🦊 The Fox and the Stars",
        "story": (
            "Every night, a little fox looks up at the stars and picks one.\n\n"
            "Not the brightest one. Not the biggest one. "
            "Just one that feels familiar. Like a friend.\n\n"
            "Then it says quietly: 'Someone out there is doing their best too. And that's enough.'\n\n"
            "Tonight, the fox picked a star and thought of you. 🦊⭐💙"
        )
    },
    {
        "title": "🐱 The Cat Who Came Back",
        "story": (
            "There's a cat who goes away sometimes. Disappears for days. "
            "People worry. They think it's gone for good.\n\n"
            "But it always comes back. Tired, a little roughed up, but home.\n\n"
            "You've gone away to dark places before. And you've always come back too.\n\n"
            "You always come back. Remember that. 🐱💙"
        )
    },
    {
        "title": "🐶 The Dog in the Rain",
        "story": (
            "There was a dog caught in a rainstorm, far from home.\n\n"
            "It could have panicked. Instead, it found a big tree and sat underneath it, "
            "waiting for the rain to pass. Patient. Trusting.\n\n"
            "The rain always passes.\n\n"
            "Find your tree. Wait it out. You're going to get home. 🐶🌧️💙"
        )
    },
]

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
    "🥠 You are doing better than you think you are. 🦊💙",
    "🥠 The right people will find you. Keep your heart open. 💕",
    "🥠 Something good is coming. You don't have to know what it is yet. ✨",
    "🥠 You have more strength in you than you've ever had to use. 🦊",
    "🥠 The chapter you're in is hard. It's not the last chapter. 📖",
    "🥠 Rest is not giving up. Rest is how you prepare for what's next. 🌙",
    "🥠 You are allowed to want more for yourself. That wanting is good. ✨",
    "🥠 Your story isn't over. Not even close. 💙",
    "🥠 Somewhere, someone is going to be really glad they met you. 🦊",
    "🥠 The version of you that makes it through this will be incredible. 💕",
    "🥠 One day at a time. One breath at a time. That's all. 🌙",
]

# ══════════════════════════════════════════════════════════════
#   VIEWS (INTERACTIVE BUTTONS)
# ══════════════════════════════════════════════════════════════

class AloneView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)

    @discord.ui.button(label="I need to hear more 💙", style=discord.ButtonStyle.primary)
    async def more(self, interaction: discord.Interaction, button: discord.ui.Button):
        more_messages = [
            "You are not a burden. You are a person who is hurting, and that is completely different. 💙",
            "The fact that you're still here, still reaching out — that says something real about you. 🦊",
            "Empty doesn't mean broken. It means you've been giving a lot and haven't been refilled yet. 💕",
            "You don't have to feel better right now. You just have to get through right now. 🌙",
            "The loneliness you feel is real. And it's survivable. You've survived every lonely night so far. ✨",
            "Somewhere out there, someone is going to be so glad they have you in their life. 💙",
            "You reached out tonight instead of disappearing into it. That's not nothing. That's brave. 🦊",
            "It's okay to not know why you feel this way. Sometimes feelings don't come with reasons. 💕",
            "You are loved in ways you can't always feel. That love is still real. 💙",
            "This moment is hard. This moment is not permanent. Hold on just a little longer. 🦊✨",
        ]
        await interaction.response.send_message(
            f"💙 {random.choice(more_messages)}\n\nThe fox is still right here with you. 🦊",
            ephemeral=True
        )

    @discord.ui.button(label="Tell me a fox story 🦊", style=discord.ButtonStyle.secondary)
    async def fox_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        story = random.choice(pet_stories)
        embed = discord.Embed(
            title=story["title"],
            description=story["story"],
            color=discord.Color.orange()
        )
        embed.set_footer(text="You are loved. You are seen. You matter. 💙🦊")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Help me breathe 🌙", style=discord.ButtonStyle.success)
    async def breathe_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🌙 Let's Breathe Together",
            description="Right here. Right now. Just you and me. 💙",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Box Breathing",
            value=(
                "**Breathe IN** for 4 seconds 🌬️\n"
                "**HOLD** for 4 seconds ⏸️\n"
                "**Breathe OUT** for 4 seconds 🍃\n"
                "**HOLD** for 4 seconds ⏸️\n\n"
                "Repeat 4 times. Take your time. I'll be right here. 🦊"
            ),
            inline=False
        )
        embed.set_footer(text="You're safe. You're here. Just breathe. 💙")
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   EVENTS
# ══════════════════════════════════════════════════════════════

@client.event
async def on_ready():
    print(f'Haven Bot is online as {client.user}! 🦊💙')
    print('Ready to help your communities! ✨')
    try:
        synced = await tree.sync()
        print(f'Synced {len(synced)} command(s) ✨')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


# ══════════════════════════════════════════════════════════════
#   NEW COMMANDS
# ══════════════════════════════════════════════════════════════

@tree.command(name="alone", description="For when you're feeling alone, empty, or just need a hug 💙")
async def alone(interaction: discord.Interaction):
    msg = random.choice(alone_messages)
    embed = discord.Embed(
        title=msg["opening"],
        description=msg["body"],
        color=discord.Color.from_rgb(100, 149, 237)
    )
    embed.add_field(
        name="When you're ready:",
        value=(
            "• `/breathe` — slow your breath down 🌙\n"
            "• `/grounding` — come back to the present 🦊\n"
            "• `/letter` — read something just for you 💌\n"
            "• `/warmth` — something soft and comforting 🌸\n"
            "• `/resources` — if you need real support 📞"
        ),
        inline=False
    )
    embed.set_footer(text="You reached out. That was brave. The fox is so proud of you. 🦊💙")
    await interaction.response.send_message(embed=embed, view=AloneView())


@tree.command(name="empty", description="For when everything feels hollow and you don't know why 🌙")
async def empty(interaction: discord.Interaction):
    messages = [
        (
            "That hollow feeling is one of the hardest to explain to people who haven't felt it. "
            "It's not sadness exactly. It's not pain exactly. It's just... nothing. And somehow nothing hurts.\n\n"
            "You don't have to fill it right now. You don't have to explain it or push through it. "
            "You're allowed to just sit with it and know that it won't always be this way. 💙\n\n"
            "The fox is sitting with you in the quiet. You're not alone in it. 🦊"
        ),
        (
            "Emotional emptiness is real. It's not laziness. It's not ingratitude. "
            "It's often what happens when your nervous system has been through too much and needs to shut down for a bit.\n\n"
            "Be gentle with yourself right now. Your mind and body are doing the best they can. "
            "You don't have to force feelings. They'll come back when you're ready. 🦊💙"
        ),
        (
            "Sometimes empty is what comes after carrying too much for too long. "
            "Your heart got tired. That makes sense.\n\n"
            "You don't have to be full right now. Half-full is okay. Even a quarter. "
            "Just existing is enough for today. 🌙\n\n"
            "One small thing at a time. The fox believes in you. 💙🦊"
        ),
    ]
    embed = discord.Embed(
        title="🌙 I Hear You",
        description=random.choice(messages),
        color=discord.Color.dark_blue()
    )
    embed.add_field(
        name="Some gentle things that might help:",
        value=(
            "• Put something warm in your hands — a mug, a blanket 🌸\n"
            "• Try `/warmth` for something soft ✨\n"
            "• Try `/pet` for a comforting little story 🦊\n"
            "• Try `/breathe` — just to feel something physical 🌬️\n"
            "• Try `/letter` — read something kind 💌"
        ),
        inline=False
    )
    embed.set_footer(text="Empty isn't forever. You will feel things again. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="night", description="For the hard nights when your brain won't stop 🌙")
async def night(interaction: discord.Interaction):
    messages = [
        (
            "Late night brain is a different beast entirely.\n\n"
            "Everything is louder. Every worry is bigger. Every regret is closer. "
            "The darkness outside makes the darkness inside feel more real.\n\n"
            "But here's what I want you to remember: **your brain at 2am is not telling you the truth.** "
            "It's exhausted and overwhelmed and not thinking clearly. "
            "The things that feel catastrophic right now will look different in the morning.\n\n"
            "You don't have to solve anything tonight. Just breathe. Just rest. 🌙💙"
        ),
        (
            "Night does something to loneliness. It stretches it out. Makes it feel permanent.\n\n"
            "It's not. I promise you it's not.\n\n"
            "Morning is coming. And with it, light, and the specific kindness that daylight brings. "
            "Your brain will be different then. Your feelings will be different then.\n\n"
            "Right now, your only job is to get through tonight. That's all. 🦊🌙"
        ),
        (
            "It's okay that you're awake right now. It's okay that your brain is loud.\n\n"
            "You don't have to force sleep. You don't have to force calm. "
            "Just be here, in this moment, and let Haven sit up with you for a while.\n\n"
            "You're not alone in the night. The fox is awake too. 🦊💙\n\n"
            "Night always ends. You'll make it to morning. 🌅"
        ),
    ]
    embed = discord.Embed(
        title="🌙 Hey, Night Owl",
        description=random.choice(messages),
        color=discord.Color.dark_blue()
    )
    embed.add_field(
        name="For right now:",
        value=(
            "• `/breathe` — slow everything down 🌬️\n"
            "• `/sleep` — gentle tips if rest feels impossible 😴\n"
            "• `/letter` — read something soft 💌\n"
            "• `/grounding` — come back to your body 🦊\n"
            "• `/pet` — let a little story carry you for a minute 🐾"
        ),
        inline=False
    )
    embed.set_footer(text="Night always ends. You'll make it to morning. 🌅💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="letter", description="Read a personal letter from Haven, just for you 💌")
async def letter(interaction: discord.Interaction):
    l = random.choice(letter_contents)
    embed = discord.Embed(
        title=l["subject"],
        description=l["body"],
        color=discord.Color.from_rgb(147, 112, 219)
    )
    embed.set_footer(text="This letter was written for you. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="warmth", description="A soft, warm moment just for you 🌸")
async def warmth(interaction: discord.Interaction):
    w = random.choice(warmth_messages)
    embed = discord.Embed(
        title=w["title"],
        description=w["body"],
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="You deserve softness. Always. 🦊💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="vent", description="Say what's on your heart — Haven will just listen 🥹")
@app_commands.describe(message="Say whatever you need to. No judgment, no advice. Just you being heard.")
async def vent(interaction: discord.Interaction, message: str):
    responses = [
        "I hear you. What you're feeling makes complete sense. You don't have to explain it or justify it — it's real, and it's valid. Thank you for trusting Haven with it. 💙🦊",
        "Thank you for saying that out loud. That took something. I want you to know: you were heard. Every word. And none of it makes you too much. 🦊💙",
        "I'm so glad you said something. Keeping that inside is heavy. You don't have to carry it alone. Haven is here, and Haven hears you. 💙✨",
        "You needed to get that out, and you did. That matters. I hear everything you said, and I'm not going anywhere. You're not alone in this. 🦊💕",
        "Heard. All of it. You didn't need to filter yourself or make it make sense — you just needed to say it, and you did. That's brave. 💙🦊",
        "You were heard. Every single word. Your feelings are valid, your pain is real, and you didn't have to go through that alone tonight. The fox is with you. 🦊💙",
    ]
    embed = discord.Embed(
        title="🥹 I Hear You",
        description=f"*\"{message}\"*\n\n{random.choice(responses)}",
        color=discord.Color.blurple()
    )
    embed.set_footer(text="You are seen. You are heard. You are not alone. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="stayhere", description="For when things feel really dark — Haven is here 💙")
async def stayhere(interaction: discord.Interaction):
    embed = discord.Embed(
        title="💙 Please Stay",
        description=(
            "I need you to hear this right now:\n\n"
            "**I want you to stay.**\n\n"
            "Not because things are easy. Not because everything is fine. "
            "But because you matter, and the world is genuinely different with you in it, "
            "and there are people — maybe people you haven't even met yet — whose lives will be shaped by yours.\n\n"
            "The pain you're feeling right now is real. I'm not going to tell you it isn't. "
            "But pain changes. Situations change. The version of you that exists on the other side of this "
            "will be someone who made it through something incredibly hard.\n\n"
            "**I need that version of you to exist.**\n\n"
            "Please reach out to someone right now. You don't have to do this alone. 💙"
        ),
        color=discord.Color.red()
    )
    embed.add_field(
        name="📞 Real Help, Right Now",
        value=(
            "**988 Suicide & Crisis Lifeline**\n"
            "Call or text: **988**\n\n"
            "**Crisis Text Line**\n"
            "Text **HOME** to **741741**\n\n"
            "**International:** findahelpline.com"
        ),
        inline=False
    )
    embed.set_footer(text="You are so loved. Please stay. 🦊💙")
    await interaction.response.send_message(embed=embed)


# ══════════════════════════════════════════════════════════════
#   EXISTING COMMANDS (kept + expanded)
# ══════════════════════════════════════════════════════════════

@tree.command(name="breathe", description="Guided breathing exercise to help you calm down 🌙")
async def breathe(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Let's Breathe Together",
        description="Follow along with this breathing exercise. Take your time. There's no rush. 💙",
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
    embed.add_field(
        name="Can't do 4 seconds?",
        value="That's okay. Do 2. Do what your body can manage. The point is just to breathe. 💙",
        inline=False
    )
    embed.set_footer(text="You're safe. You're okay. Just breathe. 💙")
    await interaction.response.send_message(embed=embed)


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


@tree.command(name="grounding", description="5-4-3-2-1 grounding technique for anxiety 🦊")
async def grounding(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🦊 Grounding Exercise",
        description="Come back to your body. Come back to right now. I'm here with you. 💙",
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
    embed.add_field(
        name="Can't find all of them?",
        value="That's okay. Even finding 2 or 3 helps pull you back. Just do what you can. 🦊",
        inline=False
    )
    embed.set_footer(text="Ground yourself. You're safe. 🦊")
    await interaction.response.send_message(embed=embed)


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


@tree.command(name="resources", description="Mental health crisis resources and hotlines 📞")
async def resources(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📞 Crisis Resources",
        description="You don't have to face this alone. Help is available 24/7. Reaching out is brave. 💙",
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
    embed.add_field(
        name="💙 Remember",
        value=(
            "You don't have to be in a full crisis to reach out.\n"
            "If you're struggling, that's enough reason to ask for help.\n"
            "You deserve support. 🦊"
        ),
        inline=False
    )
    embed.set_footer(text="Your life matters. Please reach out. 💙")
    await interaction.response.send_message(embed=embed)


@tree.command(name="checkin", description="Complete your mental health check-in 🥹")
async def checkin(interaction: discord.Interaction):
    await interaction.response.send_modal(CheckInForm())


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
                "• Try `/alone` if you need a hug 🤗\n"
                "• Try `/breathe` to slow things down 🌙\n"
                "• Try `/grounding` to feel present 🦊\n"
                "• Try `/stayhere` if things feel really dark 💙\n"
                "• Try `/resources` if you need someone to talk to 📞\n\n"
                "Please be gentle with yourself. You matter more than you know. 💕"
            ),
            "color": discord.Color.red()
        },
        2: {
            "title": "😟 It's Okay to Not Be Okay",
            "description": (
                "Not great days are still valid days. Your feelings are real and they matter. 💙\n\n"
                "• Try `/affirmation` for a little encouragement 💕\n"
                "• Try `/calm` for a moment of peace ✨\n"
                "• Try `/warmth` for something soft and comforting 🌸\n"
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
                "• Try `/checkin` to check in with yourself 🥹\n"
                "• Try `/gratitude` to gently shift your headspace ✨\n\n"
                "You're doing better than you think. Keep going. 🦊"
            ),
            "color": discord.Color.yellow()
        },
        4: {
            "title": "🙂 Pretty Good — Keep It Up!",
            "description": (
                "That's wonderful to hear! Hold onto this feeling. 💙\n\n"
                "• Try `/affirmation` to keep the good vibes going ✨\n"
                "• Share a kind word with someone else today — it spreads! 💕\n"
                "• Try `/checkup` to check on someone you care about 🦊\n\n"
                "You're doing great. Be proud of yourself. 🦊"
            ),
            "color": discord.Color.green()
        },
        5: {
            "title": "😊 Doing Great — Love to Hear It!",
            "description": (
                "This makes the fox heart so happy! 🦊💙\n\n"
                "Remember this feeling on harder days — you're capable of joy.\n\n"
                "• Maybe share some kindness with someone who needs it today 💕\n"
                "• Try `/affirmation` to celebrate yourself ✨\n"
                "• Try `/fortune` to see what's coming 🥠\n\n"
                "Keep shining. You deserve every good moment. 🌙"
            ),
            "color": discord.Color.blurple()
        }
    }
    r = responses[level]
    embed = discord.Embed(title=r["title"], description=r["description"], color=r["color"])
    embed.set_footer(text="Thank you for checking in. We care about you. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


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
        "🤗 Reach out to someone you trust. Connection is self-care too. 💙",
        "🌙 Give yourself permission to do nothing for 10 minutes. Just rest. No guilt.",
        "💌 Write yourself a kind note. Say something to yourself you'd say to a friend.",
        "🪴 Look out a window, water a plant, or step outside for a second. Nature helps. Even a little.",
    ]
    embed = discord.Embed(
        title="💕 A Little Self-Care For You",
        description=random.choice(ideas),
        color=discord.Color.from_rgb(255, 182, 193)
    )
    embed.set_footer(text="Taking care of yourself is never selfish. 🦊💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)


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
        value="• Be gentle with yourself — feeling sad is okay\n• Try `/affirmation` for a reminder of your worth\n• Try `/warmth` for something soft and comforting 🌸",
        inline=False
    )
    embed.add_field(
        name="😶 Empty / Numb",
        value="• Try `/empty` — Haven gets it 💙\n• Hold something warm — a mug, a blanket\n• Try `/pet` for a gentle little story 🦊",
        inline=False
    )
    embed.add_field(
        name="😤 Anger / Frustration",
        value="• Take 10 slow deep breaths before responding to anything\n• Move your body — walk, stretch, shake it out\n• Write out what you're feeling, then decide if you want to send it",
        inline=False
    )
    embed.add_field(
        name="💔 Loneliness",
        value="• Try `/alone` — you don't have to sit in it by yourself 💙\n• Try `/letter` for something warm to read 💌\n• Try `/checkup` to reach out to someone you care about",
        inline=False
    )
    embed.set_footer(text="You're allowed to feel all of it. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


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


@tree.command(name="sleep", description="Sleep tips for when rest feels impossible 🌙")
async def sleep(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🌙 Having Trouble Sleeping?",
        description="Here are some gentle things that can help. No pressure — just options. 💙",
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
            "• Try `/night` if your brain is loud 🌙\n"
            "• Be kind to yourself. Sleep struggles are incredibly common. 💕"
        ),
        inline=False
    )
    embed.set_footer(text="Rest well. You deserve peaceful sleep. 🌙💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="hug", description="Send a warm virtual hug to someone 🤗")
@app_commands.describe(member="Who do you want to hug?")
async def hug(interaction: discord.Interaction, member: discord.Member):
    hug_messages = [
        f"🤗 {interaction.user.display_name} sends a big warm hug to {member.mention}! You are so loved. 💙",
        f"🤗 {member.mention} — {interaction.user.display_name} wants you to know they're thinking of you. Here's a hug! 💕",
        f"🦊 A little fox hug from {interaction.user.display_name} to {member.mention}! You matter so much. 💙",
        f"🤗 {interaction.user.display_name} is wrapping {member.mention} in the warmest hug. You're not alone. ✨",
        f"💕 {member.mention} just got a hug from {interaction.user.display_name}! Sending you all the love. 🦊💙",
        f"🌙 {interaction.user.display_name} sees you, {member.mention}, and wants you to feel this hug. You are enough. 💙",
        f"🦊 The fox is delivering a hug from {interaction.user.display_name} to {member.mention}! You are so cared about. 💕",
        f"✨ {member.mention} — this hug is from {interaction.user.display_name}. You are not alone. Not even a little bit. 💙",
    ]
    await interaction.response.send_message(random.choice(hug_messages))


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
        "What is **one thing about where you are right now** that you can appreciate, however small?",
        "Think of **one moment this week** where you were kind — to someone else or to yourself. 💙",
        "What is **one small thing you're looking forward to**, even something tiny? 🦊",
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


@tree.command(name="journal", description="Privately log how you're feeling — only you can see this 🥹")
@app_commands.describe(feeling="How are you feeling right now? Share as much or as little as you'd like.")
async def journal(interaction: discord.Interaction, feeling: str):
    embed = discord.Embed(
        title="📓 Your Private Journal Entry",
        description=feeling,
        color=discord.Color.blurple()
    )
    embed.add_field(
        name="💙 Haven says:",
        value="What you just wrote matters. Your feelings are real. You are heard.",
        inline=False
    )
    embed.set_footer(text="This is just for you. Your feelings are valid. 💙🦊")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="checkup", description="Check up on someone in your community 💙")
@app_commands.describe(member="Who do you want to check on?")
async def checkup(interaction: discord.Interaction, member: discord.Member):
    checkup_messages = [
        f"💙 Hey {member.mention} — {interaction.user.display_name} is thinking about you. How are you really doing?",
        f"👀 {member.mention}, {interaction.user.display_name} wanted to check in on you. Everything okay? 🦊",
        f"🦊 {interaction.user.display_name} is checking on you, {member.mention}. You don't have to be okay — just be honest. 💙",
        f"💙 {member.mention} — {interaction.user.display_name} cares about you. How's your heart today?",
        f"🌙 Hey {member.mention}, {interaction.user.display_name} noticed you and wanted to see how you're holding up. 💙",
        f"💕 {member.mention} — someone's thinking of you. {interaction.user.display_name} just wants you to know that. 🦊",
    ]
    await interaction.response.send_message(random.choice(checkup_messages))


@tree.command(name="fortune", description="Receive a gentle uplifting fortune cookie message 🥠")
async def fortune(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🥠 Your Fortune",
        description=random.choice(fortunes),
        color=discord.Color.gold()
    )
    embed.set_footer(text="You opened this fortune at exactly the right time. 💙")
    await interaction.response.send_message(embed=embed)


@tree.command(name="pet", description="A comforting story about a little animal friend 🦊")
async def pet(interaction: discord.Interaction):
    story = random.choice(pet_stories)
    embed = discord.Embed(
        title=story["title"],
        description=story["story"],
        color=discord.Color.orange()
    )
    embed.set_footer(text="You are loved. You are seen. You matter. 💙🦊")
    await interaction.response.send_message(embed=embed)


@tree.command(name="selfesteem", description="A gentle reminder of your worth when you've forgotten it 💕")
async def selfesteem(interaction: discord.Interaction):
    messages = [
        (
            "Hey. I need you to hear this.\n\n"
            "Your worth is not determined by your productivity. It's not determined by how much you do for others, "
            "how successful you are, how 'put together' you seem, or whether you've been struggling lately.\n\n"
            "Your worth just **is**. It's not something you earn. It's not something you can lose.\n\n"
            "You are enough. Right now. Exactly as you are. 💙🦊"
        ),
        (
            "You are allowed to like yourself.\n\n"
            "You are allowed to be proud of yourself. To think 'I did a good job today.' "
            "To look in the mirror and be okay with what you see. To take up space without apologizing.\n\n"
            "That's not arrogance. That's just knowing your worth.\n\n"
            "And you have so much of it. 💙✨"
        ),
        (
            "The things that make you feel like 'too much' or 'not enough'? "
            "Those are usually the things that make you beautifully, uniquely you.\n\n"
            "Your depth. Your caring. Your sensitivity. The way you notice things other people miss. "
            "The way you feel everything so fully.\n\n"
            "Those aren't flaws. They're your whole thing. And your whole thing is pretty incredible. 🦊💕"
        ),
    ]
    embed = discord.Embed(
        title="💕 Your Worth Is Not Up For Debate",
        description=random.choice(messages),
        color=discord.Color.from_rgb(255, 105, 180)
    )
    embed.set_footer(text="You are enough. You always have been. 🦊💙")
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ══════════════════════════════════════════════════════════════
#   CHECK-IN MODAL
# ══════════════════════════════════════════════════════════════

CHECKIN_CHANNEL_ID = os.environ.get("CHECKIN_CHANNEL_ID")

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
        embed.add_field(name="─────────────────────", value="​", inline=False)
        embed.add_field(name="Scales (0-10):", value=self.scales.value, inline=False)
        embed.add_field(name="─────────────────────", value="​", inline=False)
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


# ══════════════════════════════════════════════════════════════
#   HEALTH SERVER (keep-alive for Render)
# ══════════════════════════════════════════════════════════════

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Haven Bot is running! 🦊💙")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_health_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

# ══════════════════════════════════════════════════════════════
#   RUN
# ══════════════════════════════════════════════════════════════

TOKEN = os.environ.get('DISCORD_TOKEN')
if TOKEN:
    client.run(TOKEN)
else:
    print("ERROR: No DISCORD_TOKEN found! Add it to your environment secrets.")
