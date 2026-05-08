from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.live import Live
from rich.align import Align
from rich.text import Text

import os
import subprocess
import threading
import keyboard
import random
import time

console = Console()

SUPPORTED_FORMATS = [".mp3", ".wav"]

# scan home directory for audio files
HOME = os.path.expanduser("~")

songs = []

for root, dirs, files in os.walk(HOME):
    for file in files:
        if any(file.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
            songs.append(os.path.join(root, file))

if not songs:
    console.print("[bold red]No audio files found on your system.[/bold red]")
    exit()

current_index = 0
player_process = None
random_mode = False


def play_song(index):
    global player_process

    if player_process:
        player_process.terminate()

    song = songs[index]

    player_process = subprocess.Popen(
        ["mpv", "--no-video", "--quiet", song],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def next_song():
    global current_index

    if random_mode:
        current_index = random.randint(0, len(songs) - 1)
    else:
        current_index = (current_index + 1) % len(songs)

    play_song(current_index)


def previous_song():
    global current_index

    current_index = (current_index - 1) % len(songs)

    play_song(current_index)


def toggle_random():
    global random_mode
    random_mode = not random_mode


def generate_ui():
    layout = Layout()

    layout.split_column(
        Layout(name="top", size=18),
        Layout(name="bottom")
    )

    song_name = os.path.basename(songs[current_index])

    circle = f"""
       ✨      🎧      ✨

          pastel-player

         Now Playing

        {song_name[:22]}

       ◁      ❚❚      ▷

    random: {"ON" if random_mode else "OFF"}

       press q to quit
    """

    player_panel = Panel(
        Align.center(circle),
        border_style="bright_magenta",
        title="[bold pink]pastel-player[/bold pink]",
        padding=(1, 4),
    )

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("#", style="cyan", width=4)
    table.add_column("Song", style="white")

    start = max(0, current_index - 5)
    end = min(len(songs), start + 10)

    for i in range(start, end):
        name = os.path.basename(songs[i])

        if i == current_index:
            table.add_row("▶", f"[bold cyan]{name}[/bold cyan]")
        else:
            table.add_row(str(i + 1), name)

    playlist_panel = Panel(
        table,
        border_style="bright_magenta",
        title="[bold pink]playlist[/bold pink]",
    )

    controls = """
[n] next
[p] previous
[r] random
[q] quit
"""

    controls_panel = Panel(
        controls,
        border_style="magenta",
        title="[bold pink]controls[/bold pink]"
    )

    layout["top"].split_row(
        Layout(player_panel),
        Layout(playlist_panel)
    )

    layout["bottom"].update(controls_panel)

    return layout


def keyboard_listener():
    while True:
        if keyboard.is_pressed("n"):
            next_song()
            time.sleep(0.2)

        elif keyboard.is_pressed("p"):
            previous_song()
            time.sleep(0.2)

        elif keyboard.is_pressed("r"):
            toggle_random()
            time.sleep(0.2)

        elif keyboard.is_pressed("q"):
            if player_process:
                player_process.terminate()

            os._exit(0)


play_song(current_index)

threading.Thread(target=keyboard_listener, daemon=True).start()

with Live(generate_ui(), refresh_per_second=4, screen=True) as live:
    while True:
        live.update(generate_ui())
        time.sleep(0.1)
