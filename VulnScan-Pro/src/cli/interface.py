import argparse
from rich.console import Console
from rich.table import Table
from ..scanner.core_engine import VulnScanner

console = Console()

class VulnScanCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="VulnScan Pro - Next-Gen Vulnerability Scanner")
        self._setup_arguments()
        self.scanner = VulnScanner()
    
    def _setup_arguments(self):
        self.parser.add_argument('target', help="Target IP or hostname")
        self.parser.add_argument('-p', '--ports', default='1-1024',
                               help="Port range to scan")
        self.parser.add_argument('-o', '--output', choices=['text', 'json', 'html'],
                               default='text', help="Report format")
        self.parser.add_argument('--risk', choices=['low', 'medium', 'high', 'critical'],
                               help="Filter by risk level")

    def run(self):
        args = self.parser.parse_args()
        results = self.scanner.async_scan(args.target, args.ports)
        self._display_results(results, args.output, args.risk)

    def _display_results(self, results: Dict, format: str, risk_filter: str):
        """Display results in specified format"""
        table = Table(title="Scan Results")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="magenta")
        table.add_column("Version", style="green")
        table.add_column("CVEs", style="red")
        
        for port in results['open_ports']:
            if self._passes_filter(port['cves'], risk_filter):
                table.add_row(
                    str(port['port']),
                    port['service'],
                    port.get('version', ''),
                    ", ".join([cve['id'] for cve in port['cves']])
        
        console.print(table)

    def _passes_filter(self, cves: List, risk: str) -> bool:
        """Apply risk level filter"""
        # Implementation of risk filtering
        pass
