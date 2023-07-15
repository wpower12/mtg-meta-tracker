import discord
import scrython
from table2ascii import table2ascii as t2a, PresetStyle

from ..sql import sql_get_deck, sql_get_deck_cards, sql_get_wins
from ..util import colors_to_str_rep

class DeckSummaryEmbed(discord.Embed):

    def __init__(self, title, cnx, emojis, deck_id):
        super(DeckSummaryEmbed, self).__init__(title=title)

        cur = cnx.cursor()
        cur.execute(sql_get_deck, (deck_id,))
        deck_meta = cur.fetchone()
        comm, color_identity, desc = deck_meta

        cur.execute(sql_get_wins, (deck_id,))
        wins = cur.fetchone()
        if wins is None:
            wins = 0
        else:
            wins = wins[0]

        if wins == 1:
            win_str = "win"
        else:
            win_str = "wins"

        color_str = colors_to_str_rep(color_identity, emojis)
        self.add_field(name=f"{color_str} - {comm}", value=f"{wins} {win_str}\n{desc}")

        card = scrython.cards.Named(fuzzy=comm)
        for k in card.image_uris():
            print(k)
        # print(card.image_uris())
        self.set_thumbnail(url=card.image_uris()['art_crop'])

class DeckCardsEmbed(discord.Embed):
    def __init__(self, title, card_data):
        super(DeckCardsEmbed, self).__init__(title=title)
        print(card_data)
        table = t2a(
            body=card_data,
            style=PresetStyle.plain
        )
        self.add_field(name="Cards", value=table)


def generate_card_list_embeds(cnx, emojis, deck_id):
    cards_per_embed = 25
    cur = cnx.cursor()
    cur.execute(sql_get_deck_cards, (deck_id,))
    card_table_data = []
    for card in cur.fetchall():
        count, name, mana_cost, type_line, sf_uri = card
        card_table_data.append(
            # [count, f"[{name}]({sf_uri})"]
            [count, f"{name}"]
        )

    embeds = []
    if len(card_table_data) > cards_per_embed:
        for c in range(int(len(card_table_data)/cards_per_embed)):
            c_idx = c*cards_per_embed
            partial_list = card_table_data[c_idx:c_idx+cards_per_embed]
            embeds.append(DeckCardsEmbed("Cards", partial_list))
    else:
        embeds.append(DeckCardsEmbed("Cards", card_table_data))
    return embeds
