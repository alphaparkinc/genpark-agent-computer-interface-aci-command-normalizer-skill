"""MCP server for Agent-Computer Interface (ACI) Command Normalizer."""
import sys
import json
from client import ACICommandNormalizer


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "normalize_raw_command",
                    "description": "Parses arbitrary shell/file commands (cat, sed, grep) into structured ACI execution primitives",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "raw_command": {"type": "string", "description": "Arbitrary agent CLI command string"}
                        },
                        "required": ["raw_command"],
                    },
                },
                {
                    "name": "validate_aci_bounds",
                    "description": "Validates and clamps line window boundaries for ACI open/scroll actions",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "primitive": {"type": "string"},
                            "start_line": {"type": "integer"},
                            "end_line": {"type": "integer"},
                            "total_file_lines": {"type": "integer"},
                        },
                        "required": ["primitive"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "normalize_raw_command":
            res = ACICommandNormalizer.parse_raw_action(args.get("raw_command", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "validate_aci_bounds":
            res = ACICommandNormalizer.validate_aci_bounds(
                args.get("primitive", ""),
                start_line=args.get("start_line"),
                end_line=args.get("end_line"),
                total_file_lines=args.get("total_file_lines"),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
