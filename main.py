from controllers.manage_tournament import ManageTournament
from views.tournament_view import TournamentView
from resume_tournament.resume_tournament import Resume


def main():
    manager = ManageTournament()
    tview = TournamentView(manager)
    resumetournament = Resume(manager)

    while True:
        print("\n" + "="*60)
        print("\nMenu:")
        print("1. Create a New Tournament")
        print("2. Manage an Existing Tournament")
        print("3. Resume Tournament")
        print("4. List all Ongoing Tournaments")
        print("5. Remove a Tournament")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            manager.create_tournament()
        elif choice == '2':
            tview.manage_tournament()
        elif choice == '3':
            resumetournament.resume_tournament()
        elif choice == '4':
            manager.list_tournaments()
        elif choice == '5':
            manager.remove_tournament()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
