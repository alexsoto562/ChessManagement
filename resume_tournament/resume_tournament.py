import json
from models.player import Player
from models.tournament import Tournament
from models.match import Match


class Resume:
    def __init__(self, manager):
        self.manager = manager

    def resume_tournament(self):
        file_name = input("Enter the file name of the tournament to resume: ").strip()
        file_path = file_name

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            players = [Player(p['name'], p['email'], p['chess_id'], p['birthday']) for p in data['player_details']]
            for player, details in zip(players, data['player_details']):
                player.points = details['points']

            tournament = Tournament(
                data['tournament_name'],
                data['venue'],
                data['start_date'],
                data['end_date'],
                players,
                data['max_round']
                )

            tournament.current_round = data['current_round']
            tournament.is_round_setup_done = data['is_round_setup_done']

            tournament.history = []

            for round_data in data['round_data']:
                round_matches = []
                for match_data in round_data:
                    player1 = next((p for p in players if p.chess_id == match_data['player1']['chess_id']), None)
                    player2 = next((p for p in players if p.chess_id == match_data['player2']['chess_id']), None)
                    if player1 and player2:
                        match = Match(player1, player2)
                        match.played = match_data['played']
                        match.result = match_data['result']
                        round_matches.append(match)
                tournament.history.append(round_matches)

            self.manager.tournaments[data['tournament_name']] = tournament
            print(f"Tournament '{data['tournament_name']}' has been resumed successfully.")

        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file '{file_path}'.")
        except Exception as e:
            print(f"Failed to resume tournament: {e}")
