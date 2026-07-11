import sys
import json
import re

def bump_version(new_version):
    # 1. Update manifest.json
    manifest_path = "custom_components/jourferier/manifest.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    manifest["version"] = new_version
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n") # Ensure trailing newline
    print(f"Updated {manifest_path} to {new_version}")

    # 2. Update const.py
    const_path = "custom_components/jourferier/const.py"
    with open(const_path, "r", encoding="utf-8") as f:
        const_content = f.read()
    
    # We want to replace VERSION = "1.0.6" with VERSION = "new_version"
    updated_const, count = re.subn(
        r'(VERSION\s*=\s*")([^"]+)(")',
        rf'\g<1>{new_version}\g<3>',
        const_content
    )
    if count == 0:
        print("Warning: VERSION constant not found in const.py")
    else:
        with open(const_path, "w", encoding="utf-8") as f:
            f.write(updated_const)
        print(f"Updated {const_path} to {new_version}")

    # 3. Update README.md
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
        
    # Replace | **Version**       | `1.0.5`                            |
    updated_readme, count = re.subn(
        r'(\|\s*\*\*Version\*\*\s*\|\s*`)[^`]+(`\s*\|)',
        rf'\g<1>{new_version}\g<2>',
        readme_content
    )
    if count == 0:
        print("Warning: Version table row not found in README.md")
    else:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_readme)
        print(f"Updated {readme_path} to {new_version}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 bump_version.py <new_version>")
        sys.exit(1)
    bump_version(sys.argv[1])
