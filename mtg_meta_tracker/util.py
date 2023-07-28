from discord.utils import get

def colors_to_str_rep(colors, emojis):
    color_rep = ""
    for c in colors:
        if c not in "{}":
            mana_em_name = f"mana{c.lower()}"
            color_rep += str(get(emojis, name=mana_em_name))
    return color_rep


def maybe_field(field, obj):
    if field in obj:
        return obj[field]
    else:
        return None

def maybe_float(val):
    if val is None:
        return None
    try:
        num = float(val)
    except ValueError:
        num = None
    return num

"""
Handles the nulling, too.

Just the stuff I'm saving, for now. 
"""
def parse_scryfalljson(card):
    # Stuff from the 'whole card' - Needs to be grabbed before possibly swapping to the primary face.
    oracle_id    = card['oracle_id']
    scryfall_uri = card['scryfall_uri']
    color_id_str = "".join(card['color_identity'])
    cmc = maybe_float(card['cmc'])

    if 'card_faces' in card and len(card['card_faces']) > 1:
        card = card['card_faces'][0]

    # Stuff on just the 'primary' face
    power   = maybe_field('power', card)
    num_pow = maybe_float(power)
    tough   = maybe_field('toughness', card)
    num_tou = maybe_float(power)

    return {"oracle_id": oracle_id,
            "scryfall_uri": scryfall_uri,
            "cmc": cmc,
            "color_identity": color_id_str,
            "loyalty": maybe_field('loyalty', card),
            "mana_cost": maybe_field('mana_cost', card),
            "name": card['name'],
            "oracle_text": card['oracle_text'],
            "power": power,
            "power_numeric": num_pow,
            "toughness": tough,
            "toughness_numeric": num_tou,
            "typeline": card['type_line']}
