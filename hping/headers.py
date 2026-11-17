# hping/headers.py

from typing import Dict, List, Optional


def parse_headers(headers: Optional[List[str]]) -> Dict[str, str]:
    """Parse and validate headers from command line format.

    Args:
        headers: List of headers in "Name: Value" format

    Returns:
        Dictionary of parsed headers
    """
    parsed_headers: Dict[str, str] = {}
    if headers:
        for header in headers:
            if ":" not in header or "\r" in header or "\n" in header:
                print(
                    f"Warning: Invalid header format '{header}'. "
                    f"Expected 'Name: Value'"
                )
                continue
            name, value = header.split(":", 1)
            stripped_name = name.strip()
            if not stripped_name:
                print(
                    f"Warning: Invalid header format '{header}'. "
                    f"Header name cannot be empty"
                )
                continue
            parsed_headers[stripped_name] = value.strip()

    return parsed_headers
