from discord.utils import get

def colors_to_str_rep(colors, emojis):
    color_rep = ""
    for c in colors:
        mana_em_name = f"mana{c.lower()}"
        color_rep += str(get(emojis, name=mana_em_name))
    return color_rep
