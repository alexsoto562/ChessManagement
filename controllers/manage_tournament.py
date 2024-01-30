import os
import json
from models.tournament import Tournament
from models.player import Player


class ManageTournament:
    def __init__(self):
        self.all_players = []
        self.tournaments = {}
        self.load_all_clubs()

    def load_all_clubs(self):
        base_path = (r"C:\python_hello_word\Open classroom\ProjectThreeJsonUpdate"
                     r"\ChessManagement\project_three_complete\data\clubs")
        club_files = ["cornville.json", "springfield.json"]
        for club_file in club_files:
            club_path = os.path.join(base_path, club_file)
            club_name, club_players = self.load_club(club_path)
            self.all_players.extend(club_players)

    def load_club(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            players = [Player(player['name'], player['email'], player['chess_id'], player['birthday'])
                       for player in data['players']]
            return data["name"], players

    def create_tournament(self):
        tournament_name = input("Enter the name of the new tournament: ").strip()
        venue = input("Enter the venue for the tournament: ").strip()
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()

        if tournament_name in self.tournaments:
            print(f"Tournament '{tournament_name}' already exists.")
            return

        num_players = 0
        while num_players % 2 != 0 or num_players <= 0:
            num_players = int(input("Enter the number of players to select (must be an even number): "))
        selected_players = self.select_players(num_players)

        max_rounds = int(input("Enter the maximum number of rounds: "))

        new_tournament = Tournament(tournament_name, venue, start_date, end_date, selected_players, max_rounds)
        self.tournaments[tournament_name] = new_tournament
        print(f"Tournament '{tournament_name}' has been created at {venue} from {start_date} to {end_date}.")

    def play_next_round(self, tournament):
        print(f"Attempting to play round {tournament.current_round + 1} of {tournament.max_round}.")
        if tournament.current_round >= tournament.max_round:
            print("Maximum number of rounds reached. The tournament has concluded.")
            self.declare_winner(tournament)
            self.save_tournament_state(tournament)
            return
        if not tournament.is_round_setup_done:
            tournament.setup_round()
        current_round_matches = tournament.history[tournament.current_round]
        for i, match in enumerate(current_round_matches, start=1):
            if not match.is_played():
                print(f"Match {i}: {match.player1.name} vs {match.player2.name}")
                result = input("Enter winner (1 for player1, 2 for player2, 0 for draw): ").strip()
                if result == "1":
                    match.play_match("player1")
                elif result == "2":
                    match.play_match("player2")
                elif result == "0":
                    match.play_match("draw")
        if all(match.is_played() for match in current_round_matches):
            tournament.current_round += 1
            tournament.is_round_setup_done = False
            print(f"Round {tournament.current_round} completed.")
            self.save_tournament_state(tournament)
            if tournament.current_round == tournament.max_round:
                self.declare_winner(tournament)
        else:
            print("Some matches were not completed, round cannot be completed.")

    def declare_winner(self, tournament):
        sorted_players = sorted(tournament.players, key=lambda x: x.points, reverse=True)
        winner = sorted_players[0]
        print(f"The winner of the tournament is: {winner.name} with {winner.points} points.")

    def view_player_details(self, tournament_name):
        tournament = self.tournaments.get(tournament_name)
        if not tournament:
            print(f"No tournament found with the name '{tournament_name}'.")
            return

        print(f"Player details for {tournament.name}:")
        for player in tournament.players:
            print(player)

    def select_players(self, num_players):
        selected_players = []
        while len(selected_players) < num_players:
            search_term = input("Enter a name or chess ID to search, or just press enter to list all players: ")
            display_list = self.search_players(search_term) if search_term else self.all_players

            for i, player in enumerate(display_list, 1):
                print(f"{i}: {player.name} ({player.chess_id})")

            player_index = int(input(f"Select player {len(selected_players) + 1} (enter number): ")) - 1
            if 0 <= player_index < len(display_list):
                selected_player = display_list[player_index]
                if selected_player not in selected_players:
                    selected_players.append(selected_player)
                    self.display_selected_players(selected_players)
                else:
                    print("Player already selected. Please choose a different player.")
            else:
                print("Invalid player number. Please try again.")
        return selected_players

    def display_selected_players(self, selected_players):
        print("\nCurrently selected players:")
        for i, player in enumerate(selected_players, 1):
            print(f"{i}: {player.name} ({player.chess_id})")
        print()

    def print_tournament_report(self, tournament):
        print(f"\nTournament Report for: {tournament.name}")
        print(f"Dates: {tournament.start_date} to {tournament.end_date}")
        print(f"Venue: {tournament.venue}")
        print(f"Current Round: {tournament.current_round}/{tournament.max_round}")

        print("\nPlayers (sorted by points):")
        sorted_players = sorted(tournament.players, key=lambda x: x.points, reverse=True)
        for player in sorted_players:
            print(f" - {player.name} (Points: {player.points})")

        print("\nRounds and Matches:")
        for round_num, round_matches in enumerate(tournament.history, start=1):
            print(f"Round {round_num}:")
            for match in round_matches:
                match_info = f"{match.player1.name} vs {match.player2.name}"
                if match.played:
                    result = f"Result: {match.result}"
                else:
                    result = "Not played yet"
                print(f" - Match: {match_info}, {result}")

    def list_tournaments(self):
        if not self.tournaments:
            print("There are no ongoing tournaments.")
            return

        print("Ongoing Tournaments:")
        for tournament_name in self.tournaments.keys():
            print(tournament_name)

    def remove_tournament(self):
        if not self.tournaments:
            print("There are no ongoing tournaments to remove.")
            return

        tournament_name = input("Enter the name of the tournament to remove: ").strip()
        if tournament_name in self.tournaments:
            del self.tournaments[tournament_name]
            print(f"Tournament '{tournament_name}' has been removed.")
        else:
            print(f"No tournament found with the name '{tournament_name}'.")

    def search_players(self, search_term):
        lower_search_term = search_term.lower()
        return [player for player in self.all_players
                if lower_search_term in player.name.lower()
                or lower_search_term in player.chess_id.lower()]

    def save_tournament_state(self, tournament):
        round_number = tournament.current_round
        file_name = f"{tournament.name.replace(' ', '_')}_round_{round_number}.json"
        tournament_info = {
            'tournament_name': tournament.name,
            'venue': tournament.venue,
            'start_date': tournament.start_date,
            'end_date': tournament.end_date,
            'current_round': tournament.current_round,
            'max_round': tournament.max_round,
            'is_round_setup_done': tournament.is_round_setup_done,
            'player_details': [],
            'player_leaderboard': [],
            'round_data': []
        }

        for player in tournament.players:
            player_info = {
                'name': player.name,
                'email': player.email,
                'chess_id': player.chess_id,
                'birthday': player.birthday,
                'points': player.points
            }
            tournament_info['player_details'].append(player_info)

        for round_matches in tournament.history:
            round_data = []
            for match in round_matches:
                match_info = {
                    'player1': {
                        'name': match.player1.name,
                        'chess_id': match.player1.chess_id,
                        'points': match.player1.points
                    },
                    'player2': {
                        'name': match.player2.name,
                        'chess_id': match.player2.chess_id,
                        'points': match.player2.points
                    },
                    'played': match.played,
                    'result': match.result
                }
                round_data.append(match_info)
            tournament_info['round_data'].append(round_data)

        try:
            with open(file_name, 'w') as file:
                json.dump(tournament_info, file, indent=4)
            print(f"Tournament state saved in {file_name}")
        except Exception as e:
            print(f"Failed to save tournament state: {e}")
