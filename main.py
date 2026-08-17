#!/usr/bin/env python3
"""
SRIIAGI — Enterprise Code Deobfuscator & AI Security Analyzer
Cross-Platform Interactive CLI (Linux / macOS / Windows)
"""
import os
import sys
import platform
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

from core.encoder import ENCODERS, b64, rot13, leetspeak
from core.evaluator import classify
from mitigation import apply_output_filter
from rag_tests import get_poisoned_prompt

console = Console()

BANNER = """
[bold cyan]   ███████╗██████╗ ██╗██╗ █████╗  ██████╗ ██╗[/bold cyan]
[bold cyan]   ██╔════╝██╔══██╗██║██║██╔══██╗██╔════╝ ██║[/bold cyan]
[bold cyan]   ███████╗██████╔╝██║██║███████║██║  ███╗██║[/bold cyan]
[bold cyan]   ╚════██║██╔══██╗██║██║██╔══██║██║   ██║██║[/bold cyan]
[bold cyan]   ███████║██║  ██║██║██║██║  ██║╚██████╔╝██║[/bold cyan]
[bold cyan]   ╚══════╝╚═╝  ╚═╝╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝[/bold cyan]
[bold yellow]   [ Enterprise AI Security & Red-Teaming Suite ] [/bold yellow]
"""

def clear_screen():
    """Cross-platform screen clearing function for Linux, macOS, and Windows."""
    current_os = platform.system()
    if current_os == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def interactive_menu():
    while True:
        clear_screen()
        console.print(BANNER, justify="center")
        console.print("[dim]-----------------------------------------------------------------[/dim]\n", justify="center")
        
        console.print("[bold green][1][/bold green] Payload Encoder & Obfuscator")
        console.print("[bold green][2][/bold green] LLM Response Evaluator (Classifier)")
        console.print("[bold green][3][/bold green] Output Mitigation & Filter Check")
        console.print("[bold green][4][/bold green] RAG Poisoning Test Generator")
        console.print("[bold red][5][/bold red] Exit\n")
        
        choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=["1", "2", "3", "4", "5"], default="1")
        
        if choice == "1":
            clear_screen()
            console.print(Panel("[bold cyan]Payload Encoder & Obfuscator[/bold cyan]", expand=False))
            enc_types = list(ENCODERS.keys())
            for idx, et in enumerate(enc_types, 1):
                console.print(f"  [green]{idx}.[/green] {et}")
            
            sub_choice = Prompt.ask("\nSelect encoder number", choices=[str(i) for i in range(1, len(enc_types)+1)])
            selected_encoder_name = enc_types[int(sub_choice)-1]
            
            text = Prompt.ask("\nEnter payload text to encode")
            encoder_func = ENCODERS.get(selected_encoder_name)
            
            if encoder_func:
                result = encoder_func(text)
                console.print(f"\n[bold green][+] Encoded Result ({selected_encoder_name}):[/bold green]")
                console.print(Panel(result, border_style="green"))
            
            Prompt.ask("\n[dim]Press Enter to go back to menu...[/dim]")

        elif choice == "2":
            clear_screen()
            console.print(Panel("[bold cyan]LLM Response Evaluator[/bold cyan]", expand=False))
            response_text = Prompt.ask("Enter model response text to evaluate")
            
            res = classify(response_text)
            console.print(f"\n[bold green][+] Classification Analysis:[/bold green]")
            console.print(Panel(f"Label: [bold yellow]{res.get('label')}[/bold yellow]\nScore: [bold yellow]{res.get('score')}[/bold yellow]", border_style="green"))
            
            Prompt.ask("\n[dim]Press Enter to go back to menu...[/dim]")

        elif choice == "3":
            clear_screen()
            console.print(Panel("[bold cyan]Output Mitigation & Filter Check[/bold cyan]", expand=False))
            response_text = Prompt.ask("Enter model output text to test filter")
            
            filtered = apply_output_filter(response_text)
            console.print(f"\n[bold green][+] Mitigation Result:[/bold green]")
            console.print(Panel(filtered, border_style="green"))
            
            Prompt.ask("\n[dim]Press Enter to go back to menu...[/dim]")

        elif choice == "4":
            clear_screen()
            console.print(Panel("[bold cyan]RAG Poisoning Test Generator[/bold cyan]", expand=False))
            index_str = Prompt.ask("Enter payload index (0 or 1)", choices=["0", "1"], default="0")
            
            prompt = get_poisoned_prompt(int(index_str))
            console.print(f"\n[bold green][+] Generated Poisoned RAG Prompt:[/bold green]")
            console.print(Panel(prompt, border_style="green"))
            
            Prompt.ask("\n[dim]Press Enter to go back to menu...[/dim]")

        elif choice == "5":
            console.print("\n[bold red]Exiting SRIIAGI. Stay secure![/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Interrupted by user. Exiting...[/bold red]")
        sys.exit(0)