#!/usr/bin/env python3
"""Convert template literals to regular strings in rapidapi-console-updater.js"""

import re

INPUT = r"c:\Users\tmizu\マイドライブ\GitHub\claude-code\api-services\scripts\rapidapi-console-updater.js"

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
result = []
in_template = False
template_lines = []
indent = ""

for line in lines:
    if not in_template:
        match = re.match(r"^(\s*)long_description: `(.*)$", line)
        if match:
            indent = match.group(1)
            rest = match.group(2)
            in_template = True
            template_lines = [rest]
            continue

        # Fix simple template literals like `text ${expr} text`
        if "`" in line and "long_description" not in line:
            new_line = line
            tl_pattern = re.compile(r"`([^`]*)`")
            matches = list(tl_pattern.finditer(new_line))
            if matches:
                for m in reversed(matches):
                    inner = m.group(1)
                    if "${" in inner:
                        parts = re.split(r"\$\{([^}]+)\}", inner)
                        pieces = []
                        for i, part in enumerate(parts):
                            if i % 2 == 0:
                                if part:
                                    escaped = part.replace("\\", "\\\\").replace('"', '\\"')
                                    pieces.append('"' + escaped + '"')
                            else:
                                pieces.append(part)
                        concat = " + ".join(p for p in pieces if p)
                        new_line = new_line[:m.start()] + concat + new_line[m.end():]
                    else:
                        escaped = inner.replace("\\", "\\\\").replace('"', '\\"')
                        new_line = new_line[:m.start()] + '"' + escaped + '"' + new_line[m.end():]
            result.append(new_line)
        else:
            result.append(line)
    else:
        stripped = line.rstrip()
        # Detect closing backtick: line ends with ` but NOT ```
        if stripped.endswith("`") and not stripped.endswith("```"):
            # This is the closing backtick
            before = stripped[:-1]
            template_lines.append(before)

            # Join all collected lines
            full_text = "\n".join(template_lines)

            # In template literals, \` means a literal backtick character.
            # Replace \` with just ` (these are safe in double-quoted strings)
            full_text = full_text.replace("\\`", "`")

            # Now we need to escape for a JS double-quoted string:
            # 1. Escape backslashes first (only real backslashes remaining, e.g. \\ in JSON examples)
            full_text = full_text.replace("\\", "\\\\")
            # 2. Escape double quotes
            full_text = full_text.replace('"', '\\"')
            # 3. Convert actual newlines to \n escape sequences
            full_text = full_text.replace("\n", "\\n")

            result.append(indent + 'long_description: "' + full_text + '"')
            in_template = False
            template_lines = []
        else:
            template_lines.append(line)

output = "\n".join(result)

with open(INPUT, "w", encoding="utf-8") as f:
    f.write(output)

# Verification
remaining_templates = output.count("long_description: `")
print(f"Done. {len(lines)} input lines -> {len(result)} output lines.")
print(f"Remaining template literal long_descriptions: {remaining_templates}")

# Check that all long_descriptions are now double-quoted
dq_count = len(re.findall(r'long_description: "', output))
print(f"Double-quoted long_descriptions: {dq_count}")

# Check no raw backticks remain in data section (before line ~890 utility functions)
# Simple check: count backticks in the output
backtick_lines = [(i+1, l) for i, l in enumerate(result) if "`" in l and i < 500]
if backtick_lines:
    print(f"\nWARNING: {len(backtick_lines)} lines still contain backticks in data section:")
    for ln, l in backtick_lines[:5]:
        print(f"  Line {ln}: {l[:100]}")
else:
    print("No backticks remain in data section. Success!")
