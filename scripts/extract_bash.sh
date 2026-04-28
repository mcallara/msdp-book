#!/usr/bin/env bash
# Extract all `{code-cell} bash` blocks from a MyST markdown file
# into a runnable bash script. Lines that begin with `:tags:` (the
# MyST cell tag directive) are commented out in the output.
#
# Usage: extract_bash.sh <input.md> [output.sh]
#        If output is omitted, the script is written to stdout.
# Example: ./scripts/extract_bash.sh ch1/ch12.md scripts/ch12.sh

set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <input.md> [output.sh]" >&2
    exit 1
fi

input=$1
output=${2:-/dev/stdout}

if [[ ! -f $input ]]; then
    echo "Error: input file '$input' not found" >&2
    exit 1
fi

awk '
    BEGIN { in_cell = 0 }

    # Opening fence of a bash code-cell
    /^[[:space:]]*```\{code-cell\}[[:space:]]+bash[[:space:]]*$/ {
        in_cell = 1
        next
    }

    # Closing fence
    in_cell && /^[[:space:]]*```[[:space:]]*$/ {
        in_cell = 0
        print ""
        next
    }

    in_cell {
        # Comment out MyST cell option directives like `:tags: [...]`,
        # `:tag: [...]`, `:linenos:`, etc. These are lines of the form
        # `:word:` (optionally followed by a value) appearing inside a cell.
        if ($0 ~ /^[[:space:]]*:[A-Za-z_-]+:/) {
            print "# " $0
        } else {
            print
        }
    }
' "$input" > "$output"
