import discord
import scrython

from sqlalchemy import text
from sqlalchemy.orm import Session

from table2ascii import table2ascii as t2a, PresetStyle

from ..sql import sql_get_deck_cards

from ..db.queries.deck import get_deck_wins, get_deck
from ..util import colors_to_str_rep

class DeckSummaryEmbed(discord.Embed):

    def __init__(self, title, db_engine, emojis, deck_id):
        super(DeckSummaryEmbed, self).__init__(title=title)

        found_deck = False
        wins = None
        with Session(db_engine) as session:
            try:
                res = session.execute(get_deck(deck_id))
                deck_meta = res.fetchone()

                if deck_meta is not None:
                    found_deck = True
                    comm, color_identity, desc = deck_meta
                    win_res = session.execute(get_deck_wins(deck_id))
                    wins = win_res.fetchone()

            except Exception as e:
                print("error in deck summary query.")
                print(f"error: {e}")

        if found_deck:
            wins = 0 if wins is None else wins[1]
            win_str = "win" if wins == 1 else "wins"

            color_str = colors_to_str_rep(color_identity, emojis)
            self.add_field(name=f"{color_str} - {comm}", value=f"{wins} {win_str}\n{desc}")

            # TODO - Keep this URI in the DB, and return it in the query above.
            #        saves a possible fuck up with the scryfall api call.
            card = scrython.cards.Named(fuzzy=comm)
            self.set_thumbnail(url=card.image_uris()['art_crop'])

        else:
            self.add_field(name=f"Error retrieving deck.", value=f"Deck ID {deck_id} not found.")


class DeckCardsEmbed(discord.Embed):
    def __init__(self, title, card_data):
        super(DeckCardsEmbed, self).__init__(title=title)
        table = t2a(
            body=card_data,
            style=PresetStyle.plain
        )
        self.add_field(name="Cards", value=table)


def generate_card_list_embeds(db_engine, emojis, deck_id):
    cards_per_embed = 25

    card_table_data = []
    with Session(db_engine) as session:
        try:
            res = session.execute(text(sql_get_deck_cards), {'iddeck': deck_id})
            for card in res.fetchall():
                count, name, mana_cost, type_line, sf_uri = card
                card_table_data.append(
                    [count, f"{name}"]
                )
        except Exception as e:
            print("error in card retirevial sql")
            print(f"error: {e}")

    if len(card_table_data) == 0:
        return []

    embeds = []
    if len(card_table_data) > cards_per_embed:
        for c in range(int(len(card_table_data)/cards_per_embed)):
            c_idx = c*cards_per_embed
            partial_list = card_table_data[c_idx:c_idx+cards_per_embed]
            embeds.append(DeckCardsEmbed("Cards", partial_list))
    else:
        embeds.append(DeckCardsEmbed("Cards", card_table_data))

    return embeds
