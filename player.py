from rich.console import Console
from rich.panel import Panel
import subprocess
import os

console = Console()

SONG_FOLDER = "songs"

songs = [file for file in os.listdir(SONG_FOLDER) if file.endswith(".mp3")]

if not songs:
    console.print("[red]No songs found in /songs folder[/red]")
    exit()

current_song = songs[0]

console.print(
    Panel.fit(
        f"🎧 Now Playing:\n\n[cyan]{current_song}[/cyan]\n\nPress CTRL+C to quit",
        title="pastel-player"
    )
)

try:
    subprocess.run(
        ["mpv", f"{SONG_FOLDER}/{current_song}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
except KeyboardInterrupt:
    console.print("\n[yellow]Stopped playback[/yellow]")
