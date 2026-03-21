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
        # Check for template literal start: long_description: `...
        match = re.match(r"^(\s*)long_description: `(.*)$", line)
        if match:
            indent = match.group(1)
            rest = match.group(2)
            in_template = True
            template_lines = [rest]
            continue

        # Also fix the console.log template literal on line ~931
        # console.log(`更新対象: ${API_DATA.length} API`);
        if "`" in line and "long_description" not in line:
            # Replace simple template literals like `text ${expr} text`
            # Pattern: `...${expr}...`
            new_line = line
            # Find template literals with ${} expressions
            tl_pattern = re.compile(r"`([^`]*)`")
            matches = list(tl_pattern.finditer(new_line))
            if matches:
                for m in reversed(matches):
                    inner = m.group(1)
                    if "${" in inner:
                        # Split by ${...} and rebuild with concatenation
                        parts = re.split(r"\$\{([^}]+)\}", inner)
                        # parts alternates: string, expr, string, expr, ...
                        pieces = []
                        for i, part in enumerate(parts):
                            if i % 2 == 0:
                                # string part
                                if part:
                                    escaped = part.replace("\\", "\\\\").replace('"', '\\"')
                                    pieces.append('"' + escaped + '"')
                            else:
                                # expression part
                                pieces.append(part)
                        concat = " + ".join(p for p in pieces if p)
                        new_line = new_line[:m.start()] + concat + new_line[m.end():]
                    else:
                        # Simple template literal without expressions - just replace backticks with quotes
                        escaped = inner.replace("\\", "\\\\").replace('"', '\\"')
                        new_line = new_line[:m.start()] + '"' + escaped + '"' + new_line[m.end():]
            result.append(new_line)
        else:
            result.append(line)
    else:
        stripped = line.rstrip()
        # Check if this line is the closing backtick of the template literal
        # The closing is a bare ` at end that is NOT part of a ``` code fence
        if stripped.endswith("`"):
            before = stripped[:-1]
            # If before ends with `` then this is ``` (code fence), not closing
            if before.endswith("``"):
                template_lines.append(line)
                continue
            # Also check \`\` pattern
            if before.endswith("\\`\\`"):
                template_lines.append(line)
                continue
            # This is the real closing backtick
            template_lines.append(before)
            # Join all collected lines into one string
            full_text = "\n".join(template_lines)
            # In the original template literals, \` represents a literal backtick
            # Replace \` with just `
            full_text = full_text.replace("\\`", "`")
            # Now escape for a double-quoted JS string
            # First escape backslashes (but be careful not to double-escape)
            full_text = full_text.replace("\\", "\\\\")
            # Escape double quotes
            full_text = full_text.replace('"', '\\"')
            # Convert real newlines to \n
            full_text = full_text.replace("\n", "\\n")
            result.append(indent + 'long_description: "' + full_text + '"')
            in_template = False
            template_lines = []
        else:
            template_lines.append(line)

output = "\n".join(result)

with open(INPUT, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Done. {len(lines)} lines input, {len(result)} lines output.")
# Verify no backtick template literals remain
backtick_count = output.count("long_description: `")
print(f"Remaining template literal long_descriptions: {backtick_count}")
# Count remaining backticks (should only be in comments or none)
