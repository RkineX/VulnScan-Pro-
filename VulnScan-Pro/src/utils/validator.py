import re
import ipaddress
from typing import Union

class InputValidator:
    @staticmethod
    def validate_target(target: str) -> bool:
        """Validate IP/hostname input"""
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return bool(re.match(
                r"^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])"
                r"(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$",
                target
            ))

    @staticmethod
    def validate_port(port: Union[int, str]) -> bool:
        """Validate single port number"""
        try:
            return 1 <= int(port) <= 65535
        except ValueError:
            return False

    @staticmethod
    def validate_port_range(port_range: str) -> bool:
        """Validate port range format"""
        if '-' in port_range:
            parts = port_range.split('-')
            return len(parts) == 2 and all(InputValidator.validate_port(p) for p in parts)
        return InputValidator.validate_port(port_range)

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize potentially dangerous input"""
        return re.sub(r"[^a-zA-Z0-9\.\-\/:]", "", input_str)

    @staticmethod
    def validate_risk_level(level: str) -> bool:
        """Validate risk level filter"""
        return level.lower() in {'low', 'medium', 'high', 'critical'}
