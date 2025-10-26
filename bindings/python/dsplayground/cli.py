import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.columns import Columns
from rich.text import Text
from rich import box
from typing import List
from typing_extensions import Annotated
from collections import defaultdict

from advanced_ds_playground_bindings import UnionFind

app = typer.Typer(help="An Interactive Playground for Advanced Data Structures.")
console = Console()

COLORS = ["cyan", "magenta", "yellow", "green", "blue", "red", "bright_cyan", "bright_magenta"]

def _build_tree_structure(uf: UnionFind):
    """Build a tree structure showing parent-child relationships"""
    parents = uf.parents
    children = defaultdict(list)
    roots = []
    
    for i, p in enumerate(parents):
        if i == p:
            roots.append(i)
        else:
            children[p].append(i)
    
    return roots, children

def _create_tree_visualization(root, children, depth=0, visited=None):
    """Recursively create a rich Tree visualization"""
    if visited is None:
        visited = set()
    
    if root in visited:
        return None
    
    visited.add(root)
    color = COLORS[root % len(COLORS)]
    
    node_children = children.get(root, [])
    size_info = f" [dim](size: {len(node_children) + 1})[/dim]" if node_children else ""
    tree = Tree(f"[bold {color}]Node {root}[/bold {color}]{size_info}", guide_style=color)
    
    for child in sorted(node_children):
        child_tree = _create_tree_visualization(child, children, depth + 1, visited)
        if child_tree:
            tree.add(child_tree)
    
    return tree

def _get_component_info(uf: UnionFind):
    """Get detailed information about each connected component"""
    roots, children = _build_tree_structure(uf)
    components = []
    
    for root in roots:
        members = {root}
        stack = [root]
        
        while stack:
            node = stack.pop()
            for child in children.get(node, []):
                if child not in members:
                    members.add(child)
                    stack.append(child)
        
        components.append({
            'root': root,
            'members': sorted(members),
            'size': len(members)
        })
    
    return sorted(components, key=lambda x: (-x['size'], x['root']))

def _show_union_find_state(uf: UnionFind, last_op: str = "", op_result: str = ""):
    """Renders the state of the UnionFind object with enhanced visuals"""
    
    # Header with operation info
    if op_result:
        op_panel = Panel(
            f"[bold cyan]{last_op}[/bold cyan]\n[yellow]→ {op_result}[/yellow]",
            title="[bold magenta]Operation[/bold magenta]",
            border_style="magenta",
            box=box.ROUNDED
        )
        console.print(op_panel)
    
    # Main statistics
    stats_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    stats_table.add_column(style="bold cyan", justify="right")
    stats_table.add_column(style="bold yellow")
    
    stats_table.add_row("Total Elements:", f"{len(uf.parents)}")
    stats_table.add_row("Disjoint Sets:", f"{uf.count}")
    stats_table.add_row("Largest Component:", f"{max(_get_component_info(uf), key=lambda x: x['size'])['size']}")
    
    # Component details
    components = _get_component_info(uf)
    comp_table = Table(
        title="[bold green]Connected Components[/bold green]",
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        border_style="green"
    )
    comp_table.add_column("Root", style="bold cyan", justify="center")
    comp_table.add_column("Size", style="bold yellow", justify="center")
    comp_table.add_column("Members", style="white")
    
    for comp in components:
        color = COLORS[comp['root'] % len(COLORS)]
        members_str = ", ".join([f"[{color}]{m}[/{color}]" for m in comp['members']])
        comp_table.add_row(
            str(comp['root']),
            str(comp['size']),
            members_str
        )
    
    # Parent array visualization
    parent_table = Table(
        title="[bold blue]Parent Array[/bold blue]",
        show_header=True,
        header_style="bold blue",
        box=box.ROUNDED,
        border_style="blue"
    )
    parent_table.add_column("Index", justify="center")
    parent_table.add_column("Parent", justify="center")
    parent_table.add_column("Status", justify="center")
    
    parents = uf.parents
    for i, p in enumerate(parents):
        color = COLORS[p % len(COLORS)]
        if i == p:
            status = "[bold yellow]ROOT[/bold yellow]"
            style = "bold yellow"
        else:
            status = "node"
            style = f"{color}"
        
        parent_table.add_row(
            f"[{color}]{i}[/{color}]",
            f"[{color}]{p}[/{color}]",
            status,
            style=style
        )
    
    # Tree visualisations
    roots, children = _build_tree_structure(uf)
    trees = []
    
    for root in sorted(roots):
        tree_viz = _create_tree_visualization(root, children)
        if tree_viz:
            trees.append(Panel(
                tree_viz,
                title=f"[bold]Set #{root}[/bold]",
                border_style=COLORS[root % len(COLORS)],
                box=box.ROUNDED
            ))
    
    # Layout
    console.print()
    console.print(Panel(
        stats_table,
        title="[bold yellow]Statistics[/bold yellow]",
        border_style="yellow",
        box=box.DOUBLE
    ))
    
    console.print(comp_table)
    console.print(parent_table)
    
    if trees:
        console.print("\n[bold white]Forest Structure:[/bold white]")
        if len(trees) <= 3:
            console.print(Columns(trees, equal=True, expand=True))
        else:
            for tree in trees:
                console.print(tree)
    
    console.print("\n" + "─" * console.width)

@app.command()
def unionfind(
    size: Annotated[int, typer.Option(help="Number of elements in the set.")],
    operations: Annotated[List[str], typer.Argument(help='A sequence of operations, e.g., "union 1 2"')]
):
    """
    Visualizes the Union-Find data structure with beautiful, detailed output.
    
    Operations:
    - union p q     : Unite the sets containing p and q
    - connected p q : Check if p and q are in the same set
    - find p        : Find the root of the set containing p
    """
    # Initial banner
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]Union-Find Data Structure[/bold cyan]\n"
        f"[dim]Initializing with {size} elements[/dim]",
        border_style="bright_blue",
        box=box.DOUBLE_EDGE
    ))
    
    try:
        uf = UnionFind(size)
        _show_union_find_state(uf, f"Initialization", f"Created {size} singleton sets")

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
                result = f"Sets merged ✓ (now {uf.count} disjoint sets)" if merged else "Already connected (no change)"
                _show_union_find_state(uf, f"union({p}, {q})", result)
                
            elif cmd == "connected" and len(args) == 2:
                p, q = args
                is_connected = uf.connected(p, q)
                result_icon = "✓" if is_connected else "✗"
                console.print(Panel(
                    f"[bold]connected({p}, {q})[/bold]\n"
                    f"[{'green' if is_connected else 'red'}]{result_icon} {'Yes, they are connected!' if is_connected else 'No, they are in different sets.'}[/{'green' if is_connected else 'red'}]",
                    border_style="green" if is_connected else "red",
                    box=box.ROUNDED
                ))
                
            elif cmd == "find" and len(args) == 1:
                p = args[0]
                root = uf.find(p)
                color = COLORS[root % len(COLORS)]
                console.print(Panel(
                    f"[bold]find({p})[/bold]\n"
                    f"[{color}]Root: {root}[/{color}]",
                    border_style=color,
                    box=box.ROUNDED
                ))
            else:
                console.print(Panel(
                    f"[bold red]Unknown or invalid operation: '{op}'[/bold red]\n"
                    f"[dim]Valid operations: union p q, connected p q, find p[/dim]",
                    border_style="red",
                    box=box.ROUNDED
                ))

    except IndexError as e:
        console.print(Panel(
            f"[bold red]Index Error![/bold red]\n"
            f"{e}\n"
            f"[dim]Valid indices: 0 to {size-1}[/dim]",
            border_style="red",
            box=box.DOUBLE
        ))
    except Exception as e:
        console.print(Panel(
            f"[bold red]Unexpected Error![/bold red]\n"
            f"{e}",
            border_style="red",
            box=box.DOUBLE
        ))