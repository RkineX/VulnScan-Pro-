import json
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Scan Report - {{ timestamp }}</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .vuln-critical { color: #dc3545; font-weight: bold; }
        .vuln-high { color: #fd7e14; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
        tr:hover { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <h1>Network Scan Report</h1>
    <p>Generated: {{ timestamp }}</p>
    
    {% for host in hosts %}
    <h2>Host: {{ host.target }}</h2>
    <table>
        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Version</th>
            <th>CVEs</th>
        </tr>
        {% for port in host.ports %}
        <tr>
            <td>{{ port.port }}</td>
            <td>{{ port.service }}</td>
            <td>{{ port.version }}</td>
            <td>
                {% for cve in port.cves %}
                <span class="vuln-{{ cve.risk }}">{{ cve.id }}</span>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </table>
    {% endfor %}
</body>
</html>
"""

class ReportGenerator:
    def __init__(self, scan_data):
        self.scan_data = scan_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.env = Environment(loader=FileSystemLoader('templates'))

    def generate_report(self, format='html'):
        if format == 'html':
            return self._generate_html()
        elif format == 'json':
            return self._generate_json()
        else:
            return self._generate_text()

    def _generate_html(self):
        template = self.env.from_string(HTML_TEMPLATE)
        return template.render(
            timestamp=self.timestamp,
            hosts=self.scan_data.values()
        )

    def _generate_json(self):
        return json.dumps({
            "metadata": {
                "generated_at": self.timestamp,
                "scan_duration": self.scan_data.get('duration')
            },
            "results": self.scan_data
        }, indent=2)

    def _generate_text(self):
        report = [f"VulnScan Report ({self.timestamp})\n"]
        for host in self.scan_data.values():
            report.append(f"\nHost: {host['target']}")
            report.append("Port\tService\tVersion\tCVEs")
            for port in host['ports']:
                report.append(
                    f"{port['port']}\t{port['service']}\t"
                    f"{port.get('version', '')}\t"
                    f"{', '.join([cve['id'] for cve in port['cves']])}"
                )
        return "\n".join(report)
