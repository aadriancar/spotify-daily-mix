def create_env_file():
    """
    Setup function to create a .env file with Spotify API credentials.
    
    I wanted to make it as easy as possible for users to get started. So, instead of making the user go into the dailymix.py file
    and copy/paste their credentials there, I thought it would be easiest to let them do it through their CLI, letting this function
    handle the setup.
    """
    print()
    print("       Spotify Daily Mix Setup       ")
    print()

    client_id = input("Enter your Client ID: ").strip()
    client_secret = input("Enter your Client secret: ").strip()

    env_content = (
        f"SPOTIPY_CLIENT_ID={client_id}\n"
        f"SPOTIPY_CLIENT_SECRET={client_secret}\n"
        f"SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback\n"
    )

    with open(".env", "w") as env_file:
        env_file.write(env_content)
        
    print("\n  Your credentials have been saved.")
    print("   You can now run 'dailymix' to start building your playlists!\n")
