# genpark-agent-computer-interface-aci-command-normalizer-skill

Normalizes raw autonomous agent shell, editor, and navigation commands into token-efficient Agent-Computer Interface (ACI) execution primitives.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities
- **Command Disambiguation**: Translates complex bash pipes (`cat -n | head -n`, `sed -n '1,50p'`, `grep -rn`) into deterministic ACI primitives.
- **Token Efficiency**: Prevents LLM context blowup caused by dumping full command output or malformed shell arguments.
- **Boundary Clamping**: Validates requested file windows against real document lengths to prevent out-of-bounds exceptions.
- **Zero Dependencies**: Pure Python standard library implementation with microsecond parsing performance.

## Architecture

```
[Raw Agent CLI Command String]
              │
              ▼
┌──────────────────────────────────────────────┐
│  ACICommandNormalizer                        │
│  ├─ Regex Pipeline Matcher (cat/sed/grep)    │
│  ├─ Primitive Classifier (open/search/run)   │
│  └─ Window Boundary Clamping Engine          │
└──────────────────────────────────────────────┘
              │
              ▼
[Structured ACI Primitive with Clean Args]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `normalize_raw_command`: Translates arbitrary shell commands into standardized ACI primitives.
- `validate_aci_bounds`: Validates and clamps line range arguments for file opening.

## Quickstart

```python
from client import ACICommandNormalizer

# Normalize messy pipe command
raw = "cat -n src/server.py | head -n 35"
res = ACICommandNormalizer.parse_raw_action(raw)

print(res["primitive"])           # "open"
print(res["normalized_command"])  # "open src/server.py 1:35"
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
