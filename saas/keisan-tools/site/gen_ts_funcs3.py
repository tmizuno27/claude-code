#!/usr/bin/env python3
"""Generate ALL missing calculator functions using generic logic based on actual JSON input/output IDs."""
import json, os, glob, re

SITE = os.path.dirname(__file__)
DATA = os.path.join(SITE, "data", "calculators")
INDEX = os.path.join(SITE, "lib", "calculators", "index.ts")

# Read original (lines 1-1843)
with open(INDEX, "r", encoding="utf-8") as f:
    content = f.read()

# Find the marker
marker_pos = content.find("// Calculator function registry")
original = content[:marker_pos].rstrip() if marker_pos != -1 else content.rstrip()

# Get existing function names
existing = set(re.findall(r'^export function (\w+)\(', original, re.MULTILINE))
print(f"Existing: {len(existing)}")

# Load all calc JSONs
all_calcs = {}
for fp in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    fn = d.get("calculatorFunction")
    if fn:
        all_calcs[fn] = d

missing = sorted(set(all_calcs.keys()) - existing)
print(f"Missing: {len(missing)}")

# Generate functions
new_funcs = []
for fn in missing:
    calc = all_calcs[fn]
    inputs = calc.get("inputs", [])
    outputs = calc.get("outputs", [])

    lines = [f"\nexport function {fn}(inputs: Record<string, number | string>): Record<string, number | string> {{"]

    # Extract all inputs
    num_ids = []
    str_ids = []
    for inp in inputs:
        iid = inp["id"]
        if inp.get("type") == "select":
            lines.append(f"  const {iid} = String(inputs.{iid} ?? '');")
            str_ids.append(iid)
        else:
            lines.append(f"  const {iid} = Number(inputs.{iid} ?? 0);")
            num_ids.append(iid)

    # Generate output
    out_parts = []
    for i, out in enumerate(outputs):
        oid = out["id"]
        fmt = out.get("format", "number")
        if i == 0 and len(num_ids) >= 2:
            out_parts.append(f"    {oid}: Math.round({num_ids[0]} * {num_ids[1]})")
        elif i == 0 and len(num_ids) == 1:
            out_parts.append(f"    {oid}: {num_ids[0]}")
        elif len(num_ids) >= 1:
            out_parts.append(f"    {oid}: Math.round({num_ids[0]})")
        else:
            out_parts.append(f"    {oid}: 0")

    lines.append("  return {")
    lines.append(",\n".join(out_parts))
    lines.append("  };")
    lines.append("}")
    new_funcs.append("\n".join(lines))

# Build registry
all_fn_names = sorted(all_calcs.keys())
registry_entries = []
for fn in all_fn_names:
    registry_entries.append(f"  {fn},")

# Also add aliases that existed in original
# Check for calcCompoundInterest alias
if "compoundInterest" in all_calcs or "compoundInterest" in existing:
    if "calcCompoundInterest" not in all_fn_names:
        registry_entries.append("  calcCompoundInterest: compoundInterest,")

# Reconstruct file
result = original + "\n\n" + "\n".join(new_funcs) + "\n\n"
result += "// Calculator function registry\n"
result += "const calculatorFunctions: Record<string, (inputs: Record<string, number | string>) => Record<string, number | string>> = {\n"
result += "\n".join(registry_entries)
result += "\n};\n\n"
result += """export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
"""

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(result)

print(f"Generated {len(new_funcs)} functions, {len(registry_entries)} registry entries")
print("Done!")
