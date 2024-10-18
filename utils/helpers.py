import asyncio

async def loading_animation(message, steps):
    animations = [
        "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        "⣾⣽⣻⢿⡿⣟⣯⣷",
        "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
    ]
    animation = animations[hash(str(steps)) % len(animations)]
    for step in steps:
        for char in animation:
            await message.edit(content=f"{step} {char}")
            await asyncio.sleep(0.1)
