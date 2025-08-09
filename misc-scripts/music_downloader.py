import os

def download_youtube(url, is_playlist=False):
    try:
        if "youtube.com" not in url and "youtu.be" not in url:
            raise ValueError("Invalid YouTube URL.")
        print("\n🎬 Downloading from YouTube...")

        if not is_playlist:
            os.system(f'yt-dlp -x --audio-format mp3 --no-playlist "{url}"')
        else:
            os.system(f'yt-dlp -x --audio-format mp3 "{url}"')
    except Exception as e:
        print(f"❌ Error: {e}")

def download_spotify(url, is_playlist=False):
    try:
        if "spotify.com" not in url:
            raise ValueError("Invalid Spotify URL.")

        if is_playlist and "playlist" not in url:
            raise ValueError("This does not appear to be a playlist link.")
        elif not is_playlist and "track" not in url:
            raise ValueError("This does not appear to be a track link.")

        print("\n🎧 Downloading from Spotify...")
        os.system(f'spotdl "{url}"')
    except Exception as e:
        print(f"❌ Error: {e}")

def download_spotify_liked():
    try:
        print("\n💖 Downloading your Liked Songs from Spotify into 'Liked_Songs_Spotify' folder...")
        output_folder = "Liked_Songs_Spotify"
        save_file = "liked_songs.spotdl"

        # Create folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the liked songs metadata
        print("📄 Saving liked songs metadata...")
        save_command = f'spotdl save liked --save-file {save_file} --user-auth'
        result = os.system(save_command)

        if result != 0:
            raise RuntimeError("Failed to save liked songs metadata.")

        # Move into the folder
        os.chdir(output_folder)

        # Download songs from saved file (skip existing)
        print("⬇️ Downloading songs (skipping already downloaded)...")
        download_command = f'spotdl download ../{save_file} --overwrite skip'
        os.system(download_command)

        # Return to original directory
        os.chdir("..")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🎵 Simple Music Downloader 🎵")
    print("1. YouTube - Download a single song")
    print("2. YouTube - Download full playlist")
    print("3. Spotify - Download a single song")
    print("4. Spotify - Download full playlist")
    print("5. Spotify - Download your liked songs into a folder")
    choice = input("Choose an option (1–5): ").strip()

    if choice == "1":
        url = input("Enter YouTube video link: ")
        download_youtube(url, is_playlist=False)
    elif choice == "2":
        url = input("Enter YouTube playlist link: ")
        download_youtube(url, is_playlist=True)
    elif choice == "3":
        url = input("Enter Spotify track link: ")
        download_spotify(url, is_playlist=False)
    elif choice == "4":
        url = input("Enter Spotify playlist link: ")
        download_spotify(url, is_playlist=True)
    elif choice == "5":
        download_spotify_liked()
    else:
        print("⚠️ Invalid option. Please enter 1–5.")

if __name__ == "__main__":
    main()

