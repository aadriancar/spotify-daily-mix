"""
This is the main logic file for the Daily Mix project.
It contains the core functions needed, such as authentication, recipe management, and playlist updating.
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import random
from dotenv import load_dotenv

from .helpers import fetch_pages, display_numbered, pick_indices

load_dotenv() # Load environment variables from .env file if it exists

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Set up the specific scopes for the Spotify API
SCOPES = " ".join([
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-library-read",
    "user-read-private",
])

def authenticate():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES,
        cache_path=".spotify_cache"
    ))

def load_recipes():
    if not os.path.exists("daily_mix_config.json"):
        return []
    try:
        with open("daily_mix_config.json", "r") as f:
            recipe_data = json.load(f)
            if isinstance(recipe_data, dict):
                recipe_data["name"] = recipe_data.get("name", "My Daily Mix")
                return [recipe_data]
            return recipe_data
    except Exception:
        return []

def save_recipes(recipes):
    with open("daily_mix_config.json", "w") as f:
        json.dump(recipes, f, indent=4)
        
def choose_layout():
    """
    Allows for custom layouts through a simple string input.
    Ever since I started using the original Daily Drive playlist, I've always wanted to choose
    how many podcasts and songs I wanted and where in the playlist. This does it!
    """
    print("\n  Let us create a new Daily Mix recipe! First, we need to decide on the structure of your playlist.")
    print("  Type a layout string using P (Podcast) and S (Song). Example: PSPSSSP")
    
    layout = input("\n  Layout: ").strip().upper()
    layout = ''.join([c for c in layout if c in ['P', 'S']])
    if not layout:
        print("    Invalid layout.")
        return
    return layout
        
def select_podcasts(sp, index, total):
    """
    Lets the user select up to 5 podcasts per slot.
    """
    print(f"\n  Setting up Podcast Slot #{index} of {total}...")
    print("  You can pick up to 5 podcasts for this slot, of which the most recent episode among them will be automatically selected.")
    
    chosen_podcasts = []
    while len(chosen_podcasts) < 5:
        query = input(f"\n  Search for podcast {len(chosen_podcasts)+1}/5 (or press Enter to finish this slot): ").strip()
        if not query:
            if not chosen_podcasts:
                print("    You must pick at least one podcast for this slot.")
                continue
            break
            
        results = sp.search(q=query, type="show", limit=10)["shows"]["items"]
        if not results:
            print("    No podcasts found.")
            continue
            
        display_numbered(results, lambda s: f"{s.get('name', 'Unknown Show')}  [{s.get('total_episodes', '?')} episodes]")
        
        chosen = pick_indices(results, "  Pick a show number (or press Enter to restart search): ")
        if not chosen:
            print("    Search cancelled.")
            continue
            
        chosen_podcasts.append(chosen[0]["uri"])
        print(f"    Added '{chosen[0]['name']}'. Currently {len(chosen_podcasts)}/5 podcasts in this slot.")
            
    return chosen_podcasts

def collect_podcast_slots(sp, layout):
    podcasts = []
    num_p = layout.count('P')
    for i in range(num_p):
        slot_options = select_podcasts(sp, i+1, num_p)
        podcasts.append(slot_options)
    return podcasts

def collect_song_slots(sp, layout):
    """
    Lets the user fill song slots with either specific songs or songs randomly chosen from their playlists.
    
    Originally for the randomly chosen songs from playlists, I wanted to allow the user to paste their wanted playlist URL in,
    but due to Spotify's new API limitations, I sadly no longer could. Thus, I encourage the user to add songs to a playlist
    first, then run dailymix.
    """
    songs = []
    num_s = layout.count('S')
    if num_s > 0:
        print(f"\n  Your layout requires {num_s} song(s) total.")
        print("  You can configure these in sections.")
        
        configured_s = 0
        while configured_s < num_s:
            remaining = num_s - configured_s
            print(f"\n  You have {remaining} song slot(s) left to configure.")
            
            while True:
                try:
                    chunk_input = input(f"  How many slots do you want to configure right now? (1-{remaining}): ").strip()
                    if not chunk_input: continue
                    chunk_size = int(chunk_input)
                    if 1 <= chunk_size <= remaining:
                        break
                    else:
                        print(f"    Please enter a number between 1 and {remaining}.")
                except ValueError:
                    print("    Invalid input.")
            
            print(f"  For these {chunk_size} slot(s), how should we fill them?")
            print("   1. Pick specific static songs")
            print("   2. Randomly sample from an existing playlist of yours")
            choice = input("  -> ").strip()

            if choice == "2":
                playlist_id = pick_user_playlist(sp)
                if not playlist_id: 
                    print("    No playlist selected, let's try configuring this block again.")
                    continue
                songs.append({"type": "playlist", "id": playlist_id, "count": chunk_size})
                print(f"    Will shuffle {chunk_size} song(s) from this playlist daily.")
            else:
                track_uris = select_songs(sp, chunk_size)
                if len(track_uris) < chunk_size:
                     print(f"    You didn't select enough songs. Saving {len(track_uris)} instead of {chunk_size}.")
                songs.append({"type": "specific", "uris": track_uris, "count": len(track_uris)})
                print(f"    Saved {len(track_uris)} static song(s).")
                chunk_size = len(track_uris)
                
            configured_s += chunk_size

    return songs

def select_songs(sp, needed_count):
    """
    Follows from collect_song_slots. Specific song selector.
    """
    track_uris = []
    while len(track_uris) < needed_count:
        print(f"\n  Need {needed_count - len(track_uris)} more song(s) for this block.")
        query = input("  Search for a song (or press Enter to stop/finish): ").strip()
        if not query:
            break

        results = sp.search(q=query, type="track", limit=10)["tracks"]["items"]
        if not results:
            print("  No songs found.")
            continue

        display_numbered(results, lambda t: f"{t['name']}  —  {t['artists'][0]['name']}")
        
        chosen = pick_indices(results, "  Pick song number(s) (or press Enter to restart search): ")
        if not chosen:
            print("    Search cancelled.")
            continue

        track_uris.extend([t["uri"] for t in chosen])
        
    return track_uris[:needed_count]

def pick_user_playlist(sp):
    """
    Follows from collect_song_slots. Random songs from playlist selector.
    """
    print("\n  Fetching your playlists...")
    
    user_id = sp.current_user()["id"]
    all_playlists = fetch_pages(sp, sp.current_user_playlists)
    
    owned_playlists = [p for p in all_playlists if p.get('owner', {}).get('id') == user_id]
    
    if owned_playlists:
        display_numbered(owned_playlists, lambda p: p.get('name', 'Unknown Playlist'))
    else:
        print("  (No owned playlists found in your library.)")
        return ""

    while True:
        choice = input("\n  Pick a number (or press Enter to cancel): ").strip()
        if not choice:
            return ""

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(owned_playlists):
                return owned_playlists[idx]["id"]
            else:
                print("    Invalid number.")
        except ValueError:
            print("    Invalid input.")

def update_podcasts(sp, recipe):
    resolved_ps = []
    if recipe.get("podcasts"):
        print("    Updating to most recent podcast episodes...")
        for slot_index, slot_podcasts in enumerate(recipe["podcasts"]):
            latest_episode_uri = None
            latest_date_string = ""
            for show_uri in slot_podcasts:
                eps = sp.show_episodes(show_uri, limit=1)["items"]
                if eps:
                    ep = eps[0]
                    if ep['release_date'] > latest_date_string:
                        latest_date_string = ep['release_date']
                        latest_episode_uri = ep['uri']
            resolved_ps.append(latest_episode_uri)
    return resolved_ps

def update_songs(sp, recipe):
    resolved_ss = []
    if recipe.get("songs"):
        print("    Updating songs...")
        for rule in recipe["songs"]:
            if rule["type"] == "playlist":
                print(f"      -> Sampling {rule['count']} song(s) from playlist...")
                playlist_items = []
                offset = 0
                while True:
                    result = sp.playlist_items(rule['id'], limit=50, offset=offset)
                    if not result or not result.get("items"):
                        break
                    playlist_items.extend(result["items"])
                    if not result.get("next"):
                        break
                    offset += 50
                valid_songs = [
                    it["item"]["uri"] for it in playlist_items
                    if it.get("item") and it["item"].get("uri")
                ]
                sample_size = min(rule["count"], len(valid_songs))
                sampled = random.sample(valid_songs, sample_size) if valid_songs else []
                resolved_ss.extend(sampled)
            elif rule["type"] == "specific":
                print(f"       -> Loading {rule['count']} static song(s)...")
                resolved_ss.extend(rule["uris"])
    return resolved_ss

def replace_playlist_items(sp, playlist_id, uris):
    if not uris:
        return
    sp._put(f"playlists/{playlist_id}/items", payload={"uris": uris[:100]})
    for i in range(100, len(uris), 100):
        sp._post(f"playlists/{playlist_id}/items", payload={"uris": uris[i:i+100]})

def update_single_recipe(sp, recipe):
    """
    Playlist updater based on user's saved recipes.
    
    TODO: Find a way to automate this.
    """
    print(f"\n  Updating '{recipe.get('name', 'Daily Mix')}' based on your recipe...")
    layout = recipe["layout"]
    
    updated_ps = update_podcasts(sp, recipe)
    updated_ss = update_songs(sp, recipe)

    final_uris = []
    p_idx, s_idx = 0, 0
    for char in layout:
        if char == 'P':
            if p_idx < len(updated_ps) and updated_ps[p_idx]:
                final_uris.append(updated_ps[p_idx])
            p_idx += 1
        elif char == 'S':
            if s_idx < len(updated_ss):
                final_uris.append(updated_ss[s_idx])
            s_idx += 1

    print("    Applying structure to your playlist...")
    replace_playlist_items(sp, recipe["playlist_id"], final_uris)
    
    print(f"    '{recipe.get('name', 'Daily Mix')}' updated successfully!")
    print(f"    Link: {recipe['playlist_url']}")

def create_recipe(sp):
    """
    Main function to generate the Daily Mix playlist.
    """
    layout = choose_layout()
    podcasts = collect_podcast_slots(sp, layout)
    songs = collect_song_slots(sp, layout)

    playlist_name = input("\n  Name for this Daily Mix playlist: ").strip() or "My Daily Mix"
    
    playlist_data = {
        "name": playlist_name,
        "public": False,
        "description": f"Daily Mix Playlist w/ layout: {layout}"
    }

    playlist = sp._post("me/playlists", payload=playlist_data)

    recipe = {
        "name": playlist_name,
        "playlist_id": playlist["id"],
        "playlist_url": playlist["external_urls"]["spotify"],
        "layout": layout,
        "podcasts": podcasts,
        "songs": songs
    }

    recipes = load_recipes()
    recipes.append(recipe)
    save_recipes(recipes)

    print(f"\n  Recipe saved!")
    print(f"    Generating '{playlist_name}' for the first time...")
    update_single_recipe(sp, recipe)
