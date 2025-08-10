import json
import os
from pathlib import Path
from bg_core import registry

def main():
    print("\nAmbient Profile Creator (Safe Mode)")

    name = input("Sound name (e.g., rain, wind, fireplace): ").strip().lower()
    if not name:
        print("❌ Name cannot be empty.")
        return

    try:
        level = float(input("Final volume level (e.g., 0.2): ").strip())
    except ValueError:
        print("❌ Invalid level.")
        return

    # Get allowed operators from registry
    allowed_ops = sorted(registry._OPS.keys())
    print("\nAvailable operators:")
    for i, op in enumerate(allowed_ops, start=1):
        print(f"{i}) {op}")

    ops = []
    while True:
        choice = input("\nSelect operator number (or Enter to finish): ").strip()
        if not choice:
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(allowed_ops)):
            print("❌ Invalid choice. Try again.")
            continue

        op_name = allowed_ops[int(choice) - 1]
        params = input(f"Enter params for {op_name} (e.g., gain=0.5 or lo=300,hi=2500,gain=1.2): ").strip()
        if params:
            ops.append(f"{op_name}:{params}")
        else:
            ops.append(op_name)  # allow operator with no params

    # Save profile JSON
    profiles_dir = Path("profiles")
    profiles_dir.mkdir(exist_ok=True)
    out_path = profiles_dir / f"{name}.json"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"level": level, "ops": ops}, f, indent=4)

    print(f"\n✅ Profile created: {out_path}")
    print("You can run it, for example:")
    print(f"python app.py bg --name {name} --minutes 5 --seed 42 --out out/{name}")

if __name__ == "__main__":
    main()
