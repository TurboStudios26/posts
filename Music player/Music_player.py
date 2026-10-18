"""
Project name: Music player
Version: 3.0.0
Author: Tbm Tahmid
Date: 11/3/2026
"""

import os
import random
import time
import threading
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# Global variable for input thread
current_command = None

def get_input():
    global current_command
    while True:
        cmd = input("> ").strip()
        current_command = cmd

def yt_downloader(folder):
    """YouTube video/audio downloader function using yt-dlp"""
    try:
        import yt_dlp
    except ImportError:
        print("\nError: 'yt-dlp' library is not installed.")
        print("Please run 'pip install yt-dlp' in your terminal/command prompt.")
        input("\nPress Enter to go back...")
        return

    while True:
        print("\n==================================")
        print("    YouTube Audio Downloader      ")
        print("==================================")
        print("Enter YouTube URL (or search query)")
        print("Type 'B' to Go Back to Music Player menu")
        
        link = input("\nLink/Query > ").strip()

        if link.upper() == 'B':
            print("Returning to Music Player...")
            break

        if not link:
            print("Please enter a valid link or query!")
            continue

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'no_warnings': True,
        }

        print("\n[Downloading...] Please wait...")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print("\n✓ Download completed successfully! File saved to Music folder.")
        except Exception as e:
            print(f"\n❌ Download failed: {e}")

def play_music(folder, playlist):
    global current_command
    
    # Input thread start
    input_thread = threading.Thread(target=get_input, daemon=True)
    if not input_thread.is_alive():
        input_thread.start()

    for song in playlist:
        file_path = os.path.join(folder, song)

        if not os.path.exists(file_path):
            print(f"File not found: {song}") 
            continue
        
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        print(f"\nNow playing: {song}")
        print("Commands: [P]ause, [R]esume, [S]top, [N]ext")

        stopped = False
        current_command = None  # Previous command reset

        while pygame.mixer.music.get_busy():
            if current_command:
                cmd = current_command.upper()
                current_command = None  # Reset command

                if cmd == 'P':
                    pygame.mixer.music.pause()
                    print("Music paused.")
                elif cmd == 'R':
                    pygame.mixer.music.unpause()
                    print("Music resumed.")
                elif cmd == 'S':
                    pygame.mixer.music.stop()
                    print("Music stopped.")
                    stopped = True
                    break
                elif cmd == 'N':
                    pygame.mixer.music.stop()
                    print("Skipping to next song...")
                    break
                else:
                    print("Invalid command. Use [P]ause, [R]esume, [S]top, or [N]ext.")
            
            time.sleep(0.2)
        
        if stopped:
            break

def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("Audio initialization failed:", e)
        return
    
    folder = "Music" #Give your music folder location here

    if not os.path.isdir(folder):
        print(f'Folder "{folder}" not found. Creating folder...')
        os.makedirs(folder, exist_ok=True)

    while True:
        mp3_files = [file for file in os.listdir(folder) if file.endswith('.mp3')]

        print("\n***** Music Player v3 *****")
        print("My song list:")

        if not mp3_files:
            print("  (No .mp3 files found in your Music folder)")
        else:
            for index, song in enumerate(mp3_files, start=1):
                print(f"  {index}. {song}")
            
        print("\nOptions:")
        print(" - Enter song number to play specific song")
        print(" - Enter 'P' to Play All songs")
        print(" - Enter 'S' to Shuffle Play All songs")
        print(" - Enter 'D' to open Downloader interface")
        print(" - Enter 'Q' to Quit")

        choice_input = input("\nEnter your choice: ").strip().upper()
    
        if choice_input == 'Q':
            print("Bye!")
            break
        elif choice_input == 'D':
            yt_downloader(folder)
        elif choice_input == 'P':
            if mp3_files:
                play_music(folder, mp3_files)
            else:
                print("No songs to play!")
        elif choice_input == 'S':
            if mp3_files:
                shuffled_list = mp3_files.copy()
                random.shuffle(shuffled_list)
                play_music(folder, shuffled_list)
            else:
                print("No songs to play!")
        elif choice_input.isdigit():
            choice = int(choice_input) - 1
            if 0 <= choice < len(mp3_files):
                play_music(folder, [mp3_files[choice]])
            else:
                print("Invalid choice. Please select a valid song number.")
        else:
            print("Invalid input. Please enter a number, 'P', 'S', 'D', or 'Q'.")

if __name__ == "__main__":
    main()