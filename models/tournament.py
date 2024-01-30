import random
from .match import Match


class Tournament:
    def __init__(self, name, venue, start_date, end_date, players, max_round):
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.max_round = max_round
        self.current_round = 0
        self.history = []
        self.is_round_setup_done = False

    def setup_round(self):
        if not self.history or self.current_round == 0:
            self.shuffle_players()
        else:
            self.sort_players_by_points()
        round_matches = []
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                match = Match(self.players[i], self.players[i + 1])
                round_matches.append(match)
        self.history.append(round_matches)
        self.is_round_setup_done = True

    def shuffle_players(self):
        random.shuffle(self.players)

    def sort_players_by_points(self):
        self.players.sort(key=lambda player: player.points, reverse=True)

    def play_round(self):
        if self.current_round >= self.max_round:
            print("Maximum rounds reached. No new round will be played.")
            return False

        if not self.is_round_setup_done:
            self.setup_round()
            self.is_round_setup_done = True

        all_matches_played = all(match.is_played() for match in self.history[self.current_round])

        if all_matches_played:
            self.current_round += 1
            self.is_round_setup_done = False
            print(f"Successfully completed round {self.current_round}.")
            return True
        else:
            print("Round not fully played yet.")
            return False

    def display_playerinfo(self):
        print("Rankings:")
        for player in sorted(self.players, key=lambda x: x.points, reverse=True):
            print(player)

    def display_rankings(self):
        print("Rankings:")
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)
        for player in sorted_players:
            print(f"Name: {player.name}, Points: {player.points}")
