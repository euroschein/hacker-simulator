import os
import sys
import time
import random
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()

state = {
    "player_name": "Runner",
    "credits": 100,
    "health": 100,
    "trace": 0,
    "inventory": ["Basic Decryptor"],
    "location": "Neon District (Slums)",
    "logs": [],
    "story": "Welcome to the Grid. You are a low-level runner trying to make a name for yourself. Your goal is to earn credits and avoid being traced by Netwatch.",
}

def add_log(msg, style="white"):
    timestamp = time.strftime("%H:%M:%S")
    state["logs"].append((f"[{timestamp}]", msg, style))
    if len(state["logs"]) > 10:
        state["logs"].pop(0)

def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    return layout

def generate_header():
    title = Text("🌐 HACKING SIMULATOR 🌐\n", style="bold magenta")
    title.append(f"Location: {state['location']} | Target: Netwatch Mainframe\n", style="cyan")
    title.append("Created by exc7t", style="dim italic")
    return Panel(Align.center(title), style="magenta", box=box.HEAVY)

def generate_left():
    table = Table(title="Status", box=box.ROUNDED, expand=True, border_style="cyan")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    table.add_row("Handle", state["player_name"])
    table.add_row("Credits", f"₡ {state['credits']}")
    
    health_color = "green" if state["health"] > 50 else "yellow" if state["health"] > 20 else "red"
    table.add_row("Health", Text(f"{state['health']}/100", style=health_color))
    
    trace_color = "green" if state["trace"] < 30 else "yellow" if state["trace"] < 70 else "red"
    table.add_row("Trace Level", Text(f"{state['trace']}%", style=trace_color))
    
    table.add_row("Inventory", ", ".join(state["inventory"]) if state["inventory"] else "Empty")
    
    story_text = Text("\n".join([state["story"][i:i+35] for i in range(0, len(state["story"]), 35)]), style="yellow")
    story_panel = Panel(story_text, title="Mission Log", border_style="yellow", height=14)
    
    return Group(table, story_panel)

def generate_right():
    table = Table(title="Terminal Output", box=box.SIMPLE, expand=True, border_style="magenta")
    table.add_column("Time", style="dim", width=8)
    table.add_column("Log", style="white")
    
    display_logs = [""] * 10
    for i, log in enumerate(state["logs"]):
        if i < 10:
            display_logs[9 - i] = log
    
    for log in display_logs:
        if log == "":
            table.add_row("", "")
        else:
            ts, msg, style = log
            table.add_row(ts, Text(msg, style=style))
        
    return Panel(table, border_style="magenta", height=15)

def generate_footer():
    help_text = Text("Commands: scan | hack | upgrade | heal | flee | clear | help | exit", style="dim white", justify="center")
    return Panel(help_text, box=box.SIMPLE)

def render():
    layout = make_layout()
    layout["header"].update(generate_header())
    layout["left"].update(generate_left())
    layout["right"].update(generate_right())
    layout["footer"].update(generate_footer())
    return layout

def process_command(cmd):
    cmd = cmd.lower().strip()
    
    if not cmd:
        return
        
    add_log(f"> {cmd}", "dim white")
    
    if cmd in ["help", "?"]:
        state["story"] = (
            "COMMANDS:\n"
            "- scan: Look for nodes (+10% Trace)\n"
            "- hack: Breach a node (+25% Trace)\n"
            "- upgrade: Buy ICE Breaker (100c)\n"
            "- heal: Buy Med-Stim (150c, +50 HP)\n"
            "- flee: Reduce Trace by 30%\n"
            "- clear: Clear terminal logs\n"
            "- exit: Quit the game"
        )
        add_log("Displayed help menu.", "cyan")
        
    elif cmd == "scan":
        state["trace"] += 10
        if random.random() < 0.7:
            state["story"] = "You scan the local grid and find an unsecured node. Target acquired. Type 'hack' to breach it."
            add_log("Found vulnerable node!", "green")
            if "Node IP" not in state["inventory"]:
                state["inventory"].append("Node IP")
        else:
            state["story"] = "You scan the grid, but find only heavily encrypted traffic. Try again."
            add_log("No unsecured nodes found.", "yellow")
            
    elif cmd == "hack":
        state["trace"] += 25
        if "Node IP" in state["inventory"]:
            success_chance = 0.5
            if "ICE Breaker" in state["inventory"]:
                success_chance += 0.3
                
            if random.random() < success_chance:
                loot = random.randint(50, 150)
                state["credits"] += loot
                state["inventory"].remove("Node IP")
                state["story"] = f"Success! You bypassed the firewall and stole {loot} credits. Use 'scan' to find another target."
                add_log(f"Hacked node. +{loot}c", "green")
            else:
                state["health"] -= 20
                state["inventory"].remove("Node IP")
                state["story"] = "Hack failed! The ICE fried your deck. You lost 20 HP and the target."
                add_log("Hack failed. Took damage.", "red")
        else:
            add_log("No target to hack. Use 'scan' first.", "yellow")
            state["story"] = "You try to hack, but you don't have an active target. Use 'scan' to find a Node IP first."
            
    elif cmd == "upgrade":
        if state["credits"] >= 100:
            state["credits"] -= 100
            if "ICE Breaker" not in state["inventory"]:
                state["inventory"].append("ICE Breaker")
                state["story"] = "You purchased an ICE Breaker. Hacking success rate increased by 30%."
                add_log("Upgraded deck.", "cyan")
            else:
                state["story"] = "You already have an ICE Breaker. It doesn't stack."
                add_log("Already upgraded.", "yellow")
        else:
            add_log("Not enough credits.", "red")
            state["story"] = "You need at least 100 credits to buy an ICE Breaker. Go hack some nodes first."

    elif cmd == "heal":
        if state["health"] >= 100:
            state["story"] = "Your health is already full. You don't need a Med-Stim right now."
            add_log("Health already full.", "yellow")
        elif state["credits"] >= 150:
            state["credits"] -= 150
            state["health"] = min(100, state["health"] + 50)
            state["story"] = "You injected a Med-Stim. Restored 50 HP."
            add_log("Healed 50 HP. -150c", "green")
        else:
            add_log("Not enough credits for Med-Stim.", "red")
            state["story"] = "A Med-Stim costs 150 credits. You don't have enough. Go hack more nodes."
            
    elif cmd == "flee":
        state["trace"] = max(0, state["trace"] - 30)
        state["story"] = "You disconnected from the grid and wiped your tracks. Trace level reduced by 30%."
        add_log("Trace reduced.", "cyan")
        
    elif cmd == "clear":
        os.system("clear" if os.name == "posix" else "cls")
        
    elif cmd == "exit":
        sys.exit(0)
        
    else:
        add_log(f"Command not found: {cmd}", "red")
        state["story"] = "Unknown command. The grid does not understand you. Type 'help' to see available commands."

    if state["trace"] >= 100:
        os.system("clear" if os.name == "posix" else "cls")
        console.print(Panel(Text("\nSYSTEM TRACED.\n\nYou have been captured by Netwatch.\nGAME OVER.", style="bold red", justify="center"), border_style="red", box=box.DOUBLE))
        time.sleep(3)
        sys.exit(0)
        
    if state["health"] <= 0:
        os.system("clear" if os.name == "posix" else "cls")
        console.print(Panel(Text("\nFLATLINED.\n\nYour brain fried from the ICE.\nGAME OVER.", style="bold red", justify="center"), border_style="red", box=box.DOUBLE))
        time.sleep(3)
        sys.exit(0)

def main():
    os.system("clear" if os.name == "posix" else "cls")
    
    console.print("[bold magenta]🌐 INITIALIZING NEON GRID 🌐[/bold magenta]")
    time.sleep(0.5)
    name = console.input("[cyan]Enter your Hacker Handle: [/cyan]").strip()
    if name:
        state["player_name"] = name
        
    os.system("clear" if os.name == "posix" else "cls")
    add_log("Booting Cyberdeck...", "green")
    time.sleep(0.5)
    add_log(f"Welcome to the grid, {state['player_name']}.", "cyan")
    add_log("Type 'help' for commands.", "yellow")
    
    while True:
        os.system("clear" if os.name == "posix" else "cls")
        console.print(render())
        
        cmd = console.input("[bold green]root@neon » [/bold green]")
        process_command(cmd)

if __name__ == "__main__":
    main()
