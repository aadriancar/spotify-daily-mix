from .dailymix import authenticate, load_recipes, create_recipe
from .menus import run_update_menu, view_recipes, delete_recipes_menu

def main():
    """Daily Mix Main Menu"""
    sp = authenticate()

    while True:
        try:
            recipes = load_recipes()
            has_config = len(recipes) > 0

            print()
            print("        Spotify Daily Mix Builder        ")
            print()
            
            print("  1. Create a new Daily Mix recipe")
            
            if has_config:
                print("  2. Run daily update")
                print("  3. View saved recipes")
                print("  4. Delete a recipe")
            
            print("  5. Exit")

            choice = input("\n  → ").strip()

            if choice == "1":
                create_recipe(sp)
            elif choice == "2" and has_config:
                run_update_menu(sp)
            elif choice == "3" and has_config:
                view_recipes()
            elif choice == "4" and has_config:
                delete_recipes_menu()
            elif choice == "5":
                print("  Exiting...")
                break
            else:
                print("  Invalid choice.")
        except KeyboardInterrupt:
            print("\n\n  Playlist generation cancelled! Returning to the main menu...")
            continue

# TODO: Add a way to automatically run the update function daily, perhaps with a simple scheduler or by instructing users to set up a cron job that runs the 'dailymix' command with an 'update' argument.
if __name__ == "__main__":
    main()
        