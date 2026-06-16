import sys
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

if len(sys.argv) < 2:
    console.print("[bold red]ERR:[/bold red] No Braindance datastream provided.")
    console.print("Usage: python3 bd_tuner.py <file.bd>")
    sys.exit(1)

console.clear()
console.print(Panel.fit("[bold cyan]MILITECH NEURAL TUNER v2.4.1[/bold cyan]", border_style="cyan"))
time.sleep(1.5)

with console.status("[bold green]Syncing with Braindance datastream (david_last_moments.bd)...[/bold green]", spinner="bouncingBar"):
    time.sleep(2.5)

console.print("[bold yellow]WARNING: Severe data corruption detected. Playback may be unstable.[/bold yellow]")
time.sleep(1.5)
console.clear()

console.print("[bold cyan]>>> NEURAL ID: DAVID MARTINEZ[/bold cyan]")
console.print("[bold cyan]>>> CYBER SKELETON: ENGAGED[/bold cyan]")
time.sleep(1)

# The stuttering here hints at the network timing covert channel
for i in range(1, 6):
    delay = random.choice([0.15, 0.65]) # Matches our timing channel delays!
    console.print(f"[bold blue]>>> SANDEVISTAN ACTIVATION: {i*20}% ...[/bold blue]")
    time.sleep(delay)

console.clear()
time.sleep(0.5)

console.print(Panel("[bold red]CRITICAL WARNING: ARASAKA ICE DETECTED\nENTITY IDENTIFIED: ADAM SMASHER[/bold red]", border_style="red"))
time.sleep(1.5)

for _ in range(20):
    if random.random() > 0.5:
        console.print("[bold red]ERR: FRAME DROPPED - TIME DILATION ANOMALY[/bold red]")
    else:
        console.print("[bold white]SYS: KINETIC IMPACT DETECTED[/bold white]")
    time.sleep(0.04)

console.clear()
console.print(Text(" NEURAL LINK SEVERED. FLATLINE. ", style="bold white on red", justify="center"))
print("\n")
