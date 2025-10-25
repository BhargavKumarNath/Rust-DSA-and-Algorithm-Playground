import typer
from rich.console import Console
from rich.table import Table
from typing import List
from typing_extensions import Annotated

from advanced_ds_playground_bindings import UnionFind

app = typer.Typer(help="An Interactive Playground for Advanced Data Structures.")
console = Console()

def _show_union_find_state(uf: UnionFind, last_op: str = ""):
    """Renders the state of the UnionFind object in a rich table"""
    table = Table(title="UnionFind State", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="dim")
    table.add_column("Value")

    table.add_row("Last Operation", f"[cyan]{last_op}[/cyan]")
    table.add_row("Disjoint Sets (Count)", f"[bold green]{uf.count}[/bold green]")

    # Display the parent array
    parent_table = Table(show_header=True, header_style="bold blue")
    parent_table.add_column("Index")
    parent_table.add_column("Parent")

    parents = uf.parents
    for i, p in enumerate(parents):
        style = "bold yellow" if i == p else ""
        parent_table.add_row(str(i), str(p), style=style)
    
    console.print(table)
    console.print(parent_table)
    console.print("-" * 30)

@app.command()
def unionfind(
    size: Annotated[int, typer.Option(help="Number of elements in the set.")],
    operations: Annotated[List[str], typer.Argument(help='A sequence of operations, e.g., "union 1 2"')]
):
    """
    Visualizes the Union-Find data structure.
    
    Operations:
    - union p q
    - connected p q
    - find p
    """
    console.print(f"[bold]Initializing UnionFind with {size} elements.[/bold]")
    try:
        uf = UnionFind(size)
        _show_union_find_state(uf, f"init({size})")

        for op in operations:
            parts = op.lower().split()
            if not parts:
                continue
            
            cmd = parts[0]
            if cmd == "unionfind":
                continue
                
            args = [int(p) for p in parts[1:]]

            if cmd == "union" and len(args) == 2:
                p, q = args
                merged = uf.union(p, q)
                console.print(f"Performed: [bold]union({p}, {q})[/bold] -> Merged: {merged}")
                _show_union_find_state(uf, f"union({p}, {q})")
            elif cmd == "connected" and len(args) == 2:
                p, q = args
                is_connected = uf.connected(p, q)
                console.print(f"Performed: [bold]connected({p}, {q})[/bold] -> Result: [bold]{is_connected}[/bold]")
            elif cmd == "find" and len(args) == 1:
                p = args[0]
                root = uf.find(p)
                console.print(f"Performed: [bold]find({p})[/bold] -> Root: [bold]{root}[/bold]")
            else:
                console.print(f"[bold red]Error: Unknown or invalid operation '{op}'[/bold red]") 

    except IndexError as e:
        console.print(f"[bold red]Error: {e}. An index was out of bounds for size {size}.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
