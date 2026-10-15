"""Agent-Computer Interface (ACI) Command Normalizer.
100% Python Standard Library.
"""

from typing import Dict, Any, List, Optional
import re
import shlex


class ACICommandNormalizer:
    """Translates messy, arbitrary agent shell & file commands into structured,
    deterministic Agent-Computer Interface (ACI) execution primitives (open, scroll, edit, run)."""

    ACI_PRIMITIVES = {"open", "scroll_down", "scroll_up", "goto_line", "search_dir", "edit_lines", "run"}

    @classmethod
    def parse_raw_action(cls, raw_command: str) -> Dict[str, Any]:
        """Maps freeform commands like `cat -n file.py | head -n 30` or `sed -i`
        into standard ACI primitives with normalized arguments."""
        cmd = raw_command.strip()

        # 1. Inspect file view / pagination patterns
        # e.g., cat file | head -n 50, or sed -n '1,50p'
        cat_match = re.search(r"\bcat\s+(?:-[a-zA-Z]+\s+)?([^\s|;]+)", cmd)
        head_match = re.search(r"\bhead\s+-n\s*(\d+)", cmd)
        sed_match = re.search(r"\bsed\s+-n\s*['\"](\d+),(\d+)p['\"]\s+([^\s]+)", cmd)

        if sed_match:
            start_l = int(sed_match.group(1))
            end_l = int(sed_match.group(2))
            filepath = sed_match.group(3)
            return {
                "primitive": "open",
                "path": filepath,
                "start_line": start_l,
                "end_line": end_l,
                "normalized_command": f"open {filepath} {start_l}:{end_l}",
            }

        if cat_match:
            filepath = cat_match.group(1)
            line_count = int(head_match.group(1)) if head_match else 50
            return {
                "primitive": "open",
                "path": filepath,
                "start_line": 1,
                "end_line": line_count,
                "normalized_command": f"open {filepath} 1:{line_count}",
            }

        # 2. Search pattern: grep -rn "term" path or find . -name
        grep_match = re.search(r"\bgrep\s+-[a-zA-Z]*r[a-zA-Z]*\s+['\"]?([^'\"|\s]+)['\"]?\s*([^\s|;]*)", cmd)
        if grep_match:
            term = grep_match.group(1)
            dir_target = grep_match.group(2) or "."
            return {
                "primitive": "search_dir",
                "query": term,
                "path": dir_target,
                "normalized_command": f"search_dir {dir_target} '{term}'",
            }

        # 3. Direct ACI command matching
        parts = cmd.split()
        if parts and parts[0] in cls.ACI_PRIMITIVES:
            return {
                "primitive": parts[0],
                "arguments": parts[1:],
                "normalized_command": cmd,
            }

        # 4. Fallback: treat as raw shell execution
        return {
            "primitive": "run",
            "command": cmd,
            "normalized_command": f"run {cmd}",
        }

    @classmethod
    def validate_aci_bounds(
        cls,
        primitive: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        total_file_lines: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Validates that ACI pagination arguments respect valid document boundaries."""
        if primitive == "open":
            start = start_line if start_line is not None else 1
            end = end_line if end_line is not None else (start + 50)

            if start < 1:
                start = 1
            if total_file_lines and end > total_file_lines:
                end = total_file_lines
            if end < start:
                end = start

            return {
                "valid": True,
                "clamped_start_line": start,
                "clamped_end_line": end,
                "window_size": end - start + 1,
            }

        return {"valid": True, "notice": f"Primitive '{primitive}' does not require line bounds."}
