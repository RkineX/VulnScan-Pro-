from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.console import Console
from time import sleep

class ScanDashboard:
    def __init__(self, scanner):
        self.scanner = scanner
        self.console = Console()
        self.layout = Layout()
        self.progress = 0.0
        
        # Configure layout
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=7)
        )
        
    def update_display(self):
        """Refresh dashboard components"""
        self.layout["header"].update(
            Panel("[bold blue]VulnScan Pro - Real-time Network Intelligence", style="white on blue")
        )
        
        main_table = Table.grid(padding=1)
        main_table.add_row(self._build_stats_panel(), self._build_ports_panel())
        
        self.layout["main"].update(main_table)
        self.layout["footer"].update(self._build_progress_panel())

    def _build_stats_panel(self):
        stats_table = Table(title="Scan Statistics", expand=True)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="magenta")
        
        stats_table.add_row("Target", self.scanner.target)
        stats_table.add_row("Ports Scanned", str(self.scanner.ports_scanned))
        stats_table.add_row("Open Ports", str(len(self.scanner.open_ports)))
        stats_table.add_row("Critical CVEs", str(self.scanner.critical_vulns))
        
        return Panel(stats_table, title="Statistics")

    def _build_ports_panel(self):
        ports_table = Table(title="Open Ports", expand=True)
        ports_table.add_column("Port", style="green")
        ports_table.add_column("Service")
        ports_table.add_column("Version")
        ports_table.add_column("CVEs", style="red")
        
        for port in self.scanner.open_ports[:5]:
            ports_table.add_row(
                str(port['port']),
                port['service'],
                port.get('version', ''),
                ", ".join([cve['id'] for cve in port['cves']])
            )
            
        return Panel(ports_table, title="Top Vulnerable Ports")

    def _build_progress_panel(self):
        progress_bar = (
            f"[progress.description]{self.progress*100:.0f}% Complete[/]\n"
            f"[progress.bar]{'█' * int(40 * self.progress)}{' ' * (40 - int(40 * self.progress))}[/]"
        )
        return Panel(progress_bar, title="Scan Progress")

    def run(self):
        with Live(self.layout, refresh_per_second=4, screen=True):
            while not self.scanner.complete:
                self.progress = self.scanner.scan_progress
                self.update_display()
                sleep(0.1)
