"""Example usage for Agent-Computer Interface (ACI) Command Normalizer."""
from client import ACICommandNormalizer

if __name__ == "__main__":
    # 1. Normalize cat + head pipe to ACI open primitive
    cmd1 = "cat -n src/api.py | head -n 40"
    res1 = ACICommandNormalizer.parse_raw_action(cmd1)
    print("Command 1 Normalization:")
    print("  Primitive:", res1["primitive"])
    print("  Path:", res1["path"])
    print("  Normalized:", res1["normalized_command"])

    # 2. Normalize sed line range to ACI open
    cmd2 = "sed -n '50,90p' lib/utils.py"
    res2 = ACICommandNormalizer.parse_raw_action(cmd2)
    print("\nCommand 2 Normalization:")
    print("  Primitive:", res2["primitive"])
    print("  Normalized:", res2["normalized_command"])

    # 3. Normalize grep to search_dir primitive
    cmd3 = "grep -rn 'AUTH_TOKEN' ./config"
    res3 = ACICommandNormalizer.parse_raw_action(cmd3)
    print("\nCommand 3 Normalization:")
    print("  Primitive:", res3["primitive"])
    print("  Query:", res3["query"])
    print("  Normalized:", res3["normalized_command"])
