# Leagues
### Structure
A league has:
* A set of participating players. These are players who can be added to games for that league. 
* A format.
* A description/notes.
* A boolean for using points or not? 

### Commands/Embeds/Etc
* CreateLeague: \<League Name> \<League ID> \<Format> \<Note>
  * P: Must have CreateLeague permission.
  * E:
    * Adds new league to the league table.
    * Adds the league ID to the ModifyLeague list for the invoking player.
* Add Player to League: \<League ID> \<Player ID>
  * P: League ID is in invoking players ModifyLeague list.
  * E:
    * Adds (Player ID, League ID) to the league-player table.
    * Does NOT add that to the Permissions table, so the player can't, by default, add game records. 
* Add Game Record to League: \<League ID>
  * P: Invoking player has League ID in their ModifyLeague list. 
  * E:
    * Sends Embed that exposes the game record modification screen.
    * Which has options for interacting with the game record.
    * I think anyone could mess with it at that point, but w.e. we start here.
* View League Leaderboard: \<League ID>
  * P: Anyone. 
  * E:
    * Show the thing.  

# Permissions/Admin
### Commands
* Add Player: <Player Name> 
  * Adds a Discord user to the database as a Player. 
  * Associates the User with something we can track on the discord side? Like their full username or something. Something to check against? Idk. 
  * Gives them default permissions: Ability to make decks, create leagues. 
  * Goal: Only works if invoking player has Global permissions.
* Grant Permission
  * CreateGame \<League ID> \<Player Name>
    * Goal: Only works if the league ID is in the invoking players ModifyLeague list.
  * CreateLeagues \<Player Name>
    * Goal: Only works if invoking player has Global permission.
  * ModifyLeague \<League ID> \<Player Name>
    * Goal: Only works if League ID is in invoking players ModifyLeague list.
  * CreateDecks \<Player Name>
    * Goal: Only works if invoking player has Global permission.
  * ModifyDeck \<Deck ID> \<Player Name>
    * Goal: Only works if Deck ID is in invoking players ModifyDeck list. Or if invoking has global?
  * Global \<Player Name>
    * Goal: Only works if invoking player has Global permission.
* Revoke Permission

### Permission Object/Table
This is a proxy for the structure of a permissions list for a given user.

* CreateGames
  * List of League IDs.
  * The leagues this player can create games in.
  * One-to-Many Table
    * PK: (player_id, league_id)
    * Can use this to make the list.
* CreateLeagues
  * Boolean
  * if they can create leagues in the app.
  * One-to-Constant
* ModifyLeague
  * List of League IDs.
  * The leagues this player can modify. This will also allow them to grant permissions for that league.
  * One-to-Many Table
    * PK: (player_id, league_id)
* CreateDecks
  * Boolean 
  * If they can create a deck.
  * One-to-Constant
    * Just a bool for now?
* ModifyDeck
  * List of DeckIDs
  * The decks the player can add/remove cards from.
  * When a player creates a deck, they always get permission to edit it.
  * And they gain the ability to grant permissions for that one.
  * One-to-Many Table
    * PK: (player_id, deck_id)
* GrantGlobalPermissions
  * Boolean
  * If they can change permissions for things like creating decks.

To make these things that can be tracked by a table, we need to make the tables. 
# Decks
### To Do
* Include Format as an input for deck creation
* Match this against the Format thing during adding league games
  * To only show matching decks for each player.