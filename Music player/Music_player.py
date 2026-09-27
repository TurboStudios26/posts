"""
Project name: Music player
Version: 2.0.0
Author: Tbm Tahmid (base taken from Bro Code. This is an edited version)
Date: 11/3/2026
"""

import os
import random
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def play_music(folder, playlist):
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
        while pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() != -1:
            command = input("> ").upper()

            if command == 'P':
                pygame.mixer.music.pause()
                print("Music paused.")
            elif command == 'R':
                pygame.mixer.music.unpause()
                print("Music resumed.")
            elif command == 'S':
                pygame.mixer.music.stop()
                print("Music stopped.")
                stopped = True
                break
            elif command == 'N':
                pygame.mixer.music.stop()
                print("Skipping to next song...")
                break
            else:
                print("Invalid command. Use [P]ause, [R]esume, [S]top, or [N]ext.")
        
        if stopped:
            break

def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("Audio initialization failed:", e)
        return
    
    folder = "folder"  #Give your Music folde address here

    if not os.path.isdir(folder):
        print(f'Folder "{folder}" not found.')
        return

    mp3_files = [file for file in os.listdir(folder) if file.endswith('.mp3')]
    
    if not mp3_files:
        print(f'No .mp3 files found in "{folder}".')
        return

    while True:
        print("\n***** Music Player *****")
        print("My song list:")

        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")
            
        print("\nOptions:")
        print(" - Enter song number to play specific song")
        print(" - Enter 'P' to Play All songs")
        print(" - Enter 'S' to Shuffle Play All songs")
        print(" - Enter 'Q' to Quit")

        choice_input = input("\nEnter your choice: ").strip().upper()
    
        if choice_input == 'Q':
            print("Bye!")
            break
        elif choice_input == 'P':
            play_music(folder, mp3_files)
        elif choice_input == 'S':
            shuffled_list = mp3_files.copy()
            random.shuffle(shuffled_list)
            play_music(folder, shuffled_list)
        elif choice_input.isdigit():
            choice = int(choice_input) - 1
            if 0 <= choice < len(mp3_files):
                play_music(folder, [mp3_files[choice]])
            else:
                print("Invalid choice. Please select a valid song number.")
        else:
            print("Invalid input. Please enter a number, 'P', 'S', or 'Q'.")

if __name__ == "__main__":
    main()
