from .helpers import display_numbered
from .dailymix import update_single_recipe, load_recipes, save_recipes

def run_update_menu(sp):
    recipes = load_recipes()
    if not recipes:
        print("    No recipes found.")
        return

    if len(recipes) == 1:
        update_single_recipe(sp, recipes[0])
        return

    print("\n  Which recipe(s) would you like to update?")
    display_numbered(recipes, lambda r: r.get("name", "Unnamed Mix"))
    print(f"   {len(recipes) + 1}. Update all Recipes")
    print("   0. Cancel")

    choice = input("  -> ").strip()
    try:
        idx = int(choice)
        if idx == 0:
            return
        elif 1 <= idx <= len(recipes):
            update_single_recipe(sp, recipes[idx - 1])
        elif idx == len(recipes) + 1:
            for r in recipes:
                update_single_recipe(sp, r)
        else:
            print("    Invalid choice.")
    except ValueError:
        print("    Invalid input.")

def view_recipes():
    recipes = load_recipes()
    print("\n  Saved Recipes::")
    print("─────────────────────────────────────")
    for i, r in enumerate(recipes, 1):
        name = r.get("name", "Unnamed Mix")
        layout = r.get("layout", "Unknown")
        url = r.get("playlist_url", "No URL")
        print(f"   {i}. {name}")
        print(f"      Layout: {layout}")
        print(f"      Link: {url}\n")
    print(f"  Total Recipes: {len(recipes)}")

def delete_recipes_menu():
    recipes = load_recipes()
    print("\n   Delete Recipes:")
    display_numbered(recipes, lambda r: r.get("name", "Unnamed Mix"))
    print("   ALL. Delete all Recipes")
    print("   C. Cancel")

    choice = input("\n  Which recipe do you want to delete? -> ").strip().upper()
    
    if choice == 'C':
        print("    Cancelled.")
        return
    
    if choice == 'ALL':
        confirm = input("    Are you sure you want to delete ALL recipes? (y/n): ").strip().lower()
        if confirm == 'y':
            save_recipes([])
            print("    All recipes deleted.")
        else:
            print("    Cancelled.")
        return

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(recipes):
            deleted_name = recipes[idx].get("name", "Unnamed Mix")
            confirm = input(f"    Delete '{deleted_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                recipes.pop(idx)
                save_recipes(recipes)
                print(f"    '{deleted_name}' removed from your recipes.")
            else:
                print("    Cancelled.")
        else:
            print("    Invalid number.")
    except ValueError:
        print("    Invalid input.")
        