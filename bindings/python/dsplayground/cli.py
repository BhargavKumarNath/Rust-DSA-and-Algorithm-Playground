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

from advanced_ds_playground_bindings import (
    UnionFind,
    FenwickTree,
    prefix_function,  
    find_all,         
    SparseTable,      
    Treap            
)

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

# -------------------------------------------
# FENWICK TREE
# -------------------------------------------
def _show_fenwick_tree_state(ft: FenwickTree, last_op: str = " "):
    """Renders the state of the FenwickTree object with clear explanations"""
    
    # Header with operation info
    header_table = Table(title="FenwickTree State", show_header=True, header_style="bold magenta", box=box.ROUNDED)
    header_table.add_column("", style="bold cyan")
    header_table.add_column("", style="yellow")
    header_table.add_row("Last Operation", f"{last_op}")
    header_table.add_row("Size (n)", f"{len(ft)}")
    console.print(header_table)
    
    n = len(ft)
    
    # Show actual reconstructed values
    values_table = Table(
        title="[bold green]Array Values (0-indexed)[/bold green]",
        show_header=True,
        header_style="bold green",
        box=box.ROUNDED,
        border_style="green"
    )
    values_table.add_column("Index", style="dim", justify="center")
    values_table.add_column("Value", style="bold white", justify="center")
    values_table.add_column("Prefix Sum [0..i]", style="cyan", justify="center")
    
    # Calculate actual values from prefix sums
    prev_sum = 0
    for i in range(n):
        prefix_sum = ft.query(i)
        actual_value = prefix_sum - prev_sum
        values_table.add_row(str(i), str(actual_value), str(prefix_sum))
        prev_sum = prefix_sum
    
    console.print(values_table)
    
    internal_tree = ft.internal_tree
    tree_table = Table(
        title="[bold blue]Internal Tree Structure (1-indexed)[/bold blue]",
        show_header=True,
        header_style="bold blue",
        box=box.ROUNDED,
        border_style="blue"
    )
    tree_table.add_column("Index", style="dim", justify="center")
    tree_table.add_column("Internal Value", style="yellow", justify="center")
    tree_table.add_column("Range Covered", style="dim", justify="center")
    
    for i in range(1, len(internal_tree)):
        # Calculate the range this index is responsible for
        # In Fenwick tree, index i covers range [i - LSB(i) + 1, i]
        lsb = i & -i
        range_start = i - lsb + 1
        range_str = f"[{range_start-1}..{i-1}]" if range_start != i else f"[{i-1}]"
        
        tree_table.add_row(
            str(i),
            str(internal_tree[i]),
            range_str
        )
    
    console.print(tree_table)
    console.print()
    console.print("[dim] Tip: The 'Array Values' table shows the actual data.")
    console.print("[dim] The 'Internal Tree' shows how Fenwick Tree stores it internally.[/dim]")
    console.print("-" * console.width)

@app.command()
def fenwicktree(
    init_values: Annotated[str, typer.Option(help='Initial values as a comma-separated string, e.g., "1,2,3,4".')] = "",
    size: Annotated[int, typer.Option(help="Size of the tree if no initial values.")] = 10,
    operations: Annotated[List[str], typer.Argument(help='A sequence of operations, e.g., "add 2 5"')] = None
):
    """
    Visualizes the Fenwick Tree (Binary Indexed Tree).
    
    Operations:
    - add idx delta
    - query idx
    - range_sum start end
    """
    try:
        if init_values:
            values = [int(v.strip()) for v in init_values.split(',')]
            ft = FenwickTree(values)
            console.print(f"[bold]Initializing FenwickTree with values: {values}[/bold]")
            _show_fenwick_tree_state(ft, f"init({values})")
        else:
            ft = FenwickTree(size)
            console.print(f"[bold]Initializing FenwickTree with size {size}[/bold]")
            _show_fenwick_tree_state(ft, f"init(size={size})")

        if not operations:
            return

        for op in operations:
            parts = op.lower().split()
            cmd = parts[0]
            args = [int(p) for p in parts[1:]]

            if cmd == "add" and len(args) == 2:
                idx, delta = args
                ft.add(idx, delta)
                _show_fenwick_tree_state(ft, f"add({idx}, {delta})")
            elif cmd == "query" and len(args) == 1:
                idx = args[0]
                result = ft.query(idx)
                console.print(f"Performed: [bold]query({idx})[/bold] -> Prefix Sum: [bold green]{result}[/bold green]")
            elif cmd == "range_sum" and len(args) == 2:
                start, end = args
                result = ft.range_sum(start, end)
                console.print(f"Performed: [bold]range_sum({start}, {end})[/bold] -> Sum: [bold green]{result}[/bold green]")
            else:
                console.print(f"[bold red]Error: Unknown or invalid operation '{op}'[/bold red]")

    except (IndexError, ValueError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

# -------------------------------------------
# KMP (Knuth-Morris-Pratt)
# -------------------------------------------

@app.command()
def kmp_prefix(
    pattern: Annotated[str, typer.Argument(help="The pattern string to analyze.")]
):
    """
    Calculates and displays the KMP prefix function (pi table).
    """
    if not pattern:
        console.print("[bold red]Error: Pattern cannot be empty.[/bold red]")
        raise typer.Exit(code=1)
        
    pi = prefix_function(pattern)
    
    table = Table(title=f"KMP Prefix Function for: [yellow]'{pattern}'[/yellow]", box=box.ROUNDED)
    table.add_column("Index (i)", style="dim", justify="center")
    table.add_column("Pattern (P[i])", style="bold white", justify="center")
    table.add_column("Pi Table (pi[i])", style="bold cyan", justify="center")
    table.add_column("Matching Prefix/Suffix", style="green") 
    
    for i, (char, val) in enumerate(zip(pattern, pi)):
        match_str = "[dim]-[/dim]"
        if val > 0:
            
            match_str = f"[green]'{pattern[:val]}'[/green]"
            
        table.add_row(str(i), str(char), str(val), match_str) 
        
    console.print(table)
    console.print("[dim] `pi[i]` = length of the longest proper prefix of `P[0..i]` that is also a suffix of `P[0..i]`.[/dim]")

@app.command()
def kmp_find(
    text: Annotated[str, typer.Argument(help="The text string to search in.")],
    pattern: Annotated[str, typer.Argument(help="The pattern string to search for.")]
):
    """
    Finds all occurrences of a pattern in text using KMP.
    """
    if not pattern:
        console.print("[bold red]Error: Pattern cannot be empty.[/bold red]")
        raise typer.Exit(code=1)
    if not text:
        console.print("[bold red]Error: Text cannot be empty.[/bold red]")
        raise typer.Exit(code=1)
        
    indices = find_all(text, pattern)
    pi = prefix_function(pattern) 
    
    console.print(f"Searching for [yellow]'{pattern}'[/yellow] in [cyan]'{text}'[/cyan]")
    
    pi_table = Table(title=f"Pattern's Pi Table", box=box.MINIMAL, padding=(0, 1))
    pi_table.add_column("Pattern", style="white")
    pi_table.add_column("Pi Value", style="cyan")
    for char, val in zip(pattern, pi):
        pi_table.add_row(char, str(val))
    console.print(Panel(
        pi_table,
        title="[dim]KMP Preprocessing[/dim]",
        border_style="blue",
        box=box.ROUNDED,
        expand=False
    ))
    
    if not indices:
        console.print(Panel("[bold green]No occurrences found.[/bold green]", border_style="green", box=box.ROUNDED))
        return
        
    console.print(Panel(
        f"Found [bold green]{len(indices)}[/bold green] occurrence(s) at 0-based indices: [bold yellow]{indices}[/bold yellow]",
        border_style="green",
        box=box.ROUNDED
    ))
    
    rich_text = Text(text)
    for idx in indices:
        rich_text.stylize("bold white on red", idx, idx + len(pattern))
        
    console.print("\n[bold]Visual representation:[/bold]")
    console.print(rich_text) 
    console.print()

# -------------------------------------------
# SPARSE TABLE
# -------------------------------------------

def _show_sparse_table_state(arr: List[int], last_op: str = ""):
    """Renders the state of the SparseTable object."""
    header_table = Table(title="SparseTable State (for Min)", show_header=True, header_style="bold magenta", box=box.ROUNDED)
    header_table.add_column("", style="bold cyan")
    header_table.add_column("", style="yellow")
    if last_op:
        header_table.add_row("Last Operation", f"{last_op}")
    header_table.add_row("Size (n)", f"{len(arr)}")
    console.print(header_table)
    
    arr_table = Table(
        title="[bold green]Original Array (0-indexed)[/bold green]",
        box=box.ROUNDED,
        border_style="green"
    )
    arr_table.add_column("Index", style="dim", justify="center")
    for i in range(len(arr)):
        arr_table.add_column(str(i), style="bold white", justify="center")
    
    arr_table.add_row("Value", *[str(v) for v in arr])
    console.print(arr_table)
    console.print("[dim] Sparse Table is immutable. State shows the array it was built from.[/dim]")
    console.print("-" * console.width)

@app.command()
def sparsetable(
    init_values: Annotated[str, typer.Option(help='Initial values as a comma-separated string, e.g., "5,2,4,7,1,3".')],
    operations: Annotated[List[str], typer.Argument(help='A sequence of query operations, e.g., "query 1 4"')] = None
):
    """
    Visualizes the Sparse Table (for Range Minimum Query).
    
    Operations:
    - query l r
    """
    if not init_values:
        console.print("[bold red]Error: Initial values are required for Sparse Table.[/bold red]")
        raise typer.Exit(code=1)
        
    try:
        values = [int(v.strip()) for v in init_values.split(',')]
        st = SparseTable(values)
        console.print(f"[bold]Initializing SparseTable with values: {values}[/bold]")
        _show_sparse_table_state(values, f"init({values})")
        
        if not operations:
            return

        for op in operations:
            parts = op.lower().split()
            cmd = parts[0]
            args = [int(p) for p in parts[1:]]
            
            if cmd == "query" and len(args) == 2:
                l, r = args
                result = st.query(l, r)
                if result is not None:
                    console.print(f"Performed: [bold]query({l}, {r})[/bold] -> Min: [bold green]{result}[/bold green]")
                else:
                    console.print(f"Performed: [bold]query({l}, {r})[/bold] -> [red]Invalid range (l > r or out of bounds)[/red]")
            else:
                console.print(f"[bold red]Error: Unknown or invalid operation '{op}'[/bold red]")
                
    except (IndexError, ValueError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error: {e}[/bold red]")

# -------------------------------------------
# TREAP
# -------------------------------------------

def _build_treap_viz(node) -> Tree:
    """Recursively builds a rich.Tree from a PyTreapNode."""
    if not node:
        return Tree("[dim]empty[/dim]")
    
    color = COLORS[abs(node.key) % len(COLORS)]
    
    label = (
        f"[{color} bold]Key: {node.key}[/{color} bold] "
        f"[dim](Prio: ...{node.priority % 10000:04d})[/dim] "
        f"[green](Count: {node.count}, Size: {node.size})[/green]"
    )
    tree = Tree(label, guide_style=color)
    
    if node.left or node.right:
        left_child = _build_treap_viz(node.left) if node.left else Tree("L: [dim]null[/dim]")
        right_child = _build_treap_viz(node.right) if node.right else Tree("R: [dim]null[/dim]")
        tree.add(left_child)
        tree.add(right_child)
    else:
        tree.guide_style = "dim" 
    
    return tree

def _show_treap_state(t: Treap, last_op: str = "", op_result: str = ""):
    """Renders the state of the Treap object."""
    header_table = Table(title="Treap State", show_header=True, header_style="bold magenta", box=box.ROUNDED)
    header_table.add_column("", style="bold cyan")
    header_table.add_column("", style="yellow")
    header_table.add_row("Last Operation", f"{last_op}")
    if op_result:
        header_table.add_row("Result", op_result)
    header_table.add_row("Size (len)", f"{len(t)}")
    console.print(header_table)
    
    root_node = t.root
    if root_node:
        viz_tree = _build_treap_viz(root_node)
        console.print(Panel(
            viz_tree,
            title="[bold blue]Treap Structure (BST by Key, Heap by Priority)[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        ))
    else:
        console.print(Panel(
            "[dim]Treap is empty[/dim]",
            title="[bold blue]Treap Structure[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        ))

    contents = t.inorder_vec()
    
    content_table = Table(
        title="[bold green]Current Contents (In-Order)[/bold green]",
        box=box.ROUNDED,
        border_style="green"
    )
    content_table.add_column("Values", style="bold white")
    
    if not contents:
        content_table.add_row("[dim](empty)[/dim]")
    else:
        content_table.add_row(f"{contents}")
    
    console.print(content_table)
    console.print("-" * console.width) 

@app.command()
def treap(
    operations: Annotated[List[str], typer.Argument(help='A sequence of operations, e.g., "insert 5" "remove 3"')] = None
):
    """
    Visualizes the Treap (Randomized BST).
    
    Operations:
    - insert key
    - remove key
    - contains key
    """
    console.print()
    console.print(Panel.fit(
        f"[bold magenta]Treap (Randomized BST)[/bold magenta]\n"
        f"[dim]Initializing new empty Treap[/dim]",
        border_style="magenta",
        box=box.DOUBLE_EDGE
    ))

    try:
        t = Treap()
        _show_treap_state(t, "init()")
        
        if not operations:
            return

        for op in operations:
            parts = op.lower().split()
            if not parts:
                continue
            
            cmd = parts[0]
            args = [int(p) for p in parts[1:]]

            if cmd == "insert" and len(args) == 1:
                key = args[0]
                t.insert(key)
                _show_treap_state(t, f"insert({key})")
            elif cmd == "remove" and len(args) == 1:
                key = args[0]
                t.remove(key)
                _show_treap_state(t, f"remove({key})")
            elif cmd == "contains" and len(args) == 1:
                key = args[0]
                result = key in t 
                is_found = result
                op_str = f"contains({key})"
                result_str = f"[{'green' if is_found else 'red'}] {'✓ Found' if is_found else '✗ Not Found'}[/{'green' if is_found else 'red'}]"
                _show_treap_state(t, op_str, result_str) 
            else:
                console.print(f"[bold red]Error: Unknown or invalid operation '{op}'[/bold red]")
                
    except (IndexError, ValueError) as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error: {e}[/bold red]")