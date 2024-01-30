class TournamentView:
    def __init__(self, tournament_manager):
        self.tournament_manager = tournament_manager

    def manage_tournament(self):
        if not self.tournament_manager.tournaments:
            print("No tournaments available.")
            return

        print("\nAvailable Tournaments:")
        tournament_names = list(self.tournament_manager.tournaments.keys())
        for i, name in enumerate(tournament_names, 1):
            print(f"{i}. {name}")

        choice = input("Select a tournament to manage (enter number): ").strip()
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(tournament_names):
                tournament_name = tournament_names[choice_index]
                tournament = self.tournament_manager.tournaments[tournament_name]
            else:
                print("Invalid selection. Please try again.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        while True:
            print("\n" + "="*60)
            print(f"\nManaging Tournament: {tournament.name}")
            print(f"Venue: {tournament.venue}")
            print(f"Dates: {tournament.start_date} to {tournament.end_date}")
            print(f"Current Round: {tournament.current_round} / {tournament.max_round}")
            print("Players:")
            for player in tournament.players:
                print(f" - {player.name} (Points: {player.points})")

            print("1. View Rankings")
            print("2. Play Next Round")
            print("3. View Player Details")
            print("4. Print Tournament Report")
            print("5. Back to Main Menu")
            choice = input("Choose an option: ")

            if choice == '1':
                tournament.display_rankings()
            elif choice == '2':
                self.tournament_manager.play_next_round(tournament)
            elif choice == '3':
                self.tournament_manager.view_player_details(tournament.name)
            elif choice == '4':
                self.tournament_manager.print_tournament_report(tournament)
            elif choice == '5':
                break
            else:
                print("Invalid option, please try again.")
