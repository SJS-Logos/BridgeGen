#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# ------------------------------------------------------------
# Step 1 — Parse abstract interface class from C++ header
# ------------------------------------------------------------
import re

def extract_braced_block(text, start_index):
    """
    Returns the substring between matching braces starting at text[start_index],
    handling nested braces correctly.

    Parameters:
        text (str): The full text to scan.
        start_index (int): Index of the opening '{' character.

    Returns:
        (block_text, end_index): 
            block_text is the string between braces (excluding the braces).
            end_index is the index *after* the matching '}'.
    
    Raises:
        ValueError: if braces are unbalanced or start_index is invalid.
    """
    if start_index < 0 or start_index >= len(text) or text[start_index] != '{':
        raise ValueError("start_index must point to an opening brace '{'")

    brace_count = 1
    i = start_index + 1
    while i < len(text) and brace_count > 0:
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
        i += 1

    if brace_count != 0:
        raise ValueError("Unbalanced braces in input text")

    return text[start_index + 1 : i - 1], i


def parse_interface(header_text):
    """
    Finds the first C++ abstract interface class (not enum/struct/union) in header_text
    and returns its name and body text (without braces).
    """
    # Regex to find a non-enum/struct/union class declaration
    class_match = re.search(r'(?<!enum\s)\bclass\s(\w+).*\s*{', header_text)
    if not class_match:
        raise ValueError("No abstract class found")

    class_name = class_match.group(1)
    start_index = class_match.end() - 1  # points to '{'

    class_body, _ = extract_braced_block(header_text, start_index)

    # Match pure virtual methods
    method_pattern = re.compile(
        r'virtual\s+([\w:<>&\s*\[\]]+?)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*=\s*0\s*;',
        re.MULTILINE
    )

    methods = []
    for m in method_pattern.finditer(class_body):
        return_type, name, args, const = m.groups()
        methods.append({
            "return_type": return_type.strip(),
            "name": name.strip(),
            "args": args.strip(),
            "const": bool(const)
        })

    if not methods:
        raise ValueError(f"No abstract class found (no pure virtual methods) looking in {class_body}")

    return class_name, methods


# ------------------------------------------------------------
# Step 2 — Generate hourglass header and source files
# ------------------------------------------------------------

TPL_HEADER = """#pragma once
#include <memory>
#include "../{orig_header}"

namespace detail {{

// Hidden bridge (not part of public ABI)
class {interface_name}Bridge {{
public:
    explicit {interface_name}Bridge(std::unique_ptr<{interface_name}>&& impl)
        : impl_(std::move(impl)) {{}}

{bridge_methods}

private:
    std::unique_ptr<{interface_name}> impl_;
}};

}} // namespace detail

// Proxy implementing {interface_name}
class {interface_name}Proxy : public {interface_name} {{
public:
    explicit {interface_name}Proxy(std::unique_ptr<detail::{interface_name}Bridge>&& bridge)
        : bridge_(std::move(bridge)) {{}}

{proxy_methods}

private:
    std::unique_ptr<detail::{interface_name}Bridge> bridge_;
}};

// Inline factory (header-only)
inline std::unique_ptr<{interface_name}> CreateStable{interface_name}(std::unique_ptr<{interface_name}>&& impl) {{
    auto bridge = std::make_unique<detail::{interface_name}Bridge>(std::move(impl));
    return std::make_unique<{interface_name}Proxy>(std::move(bridge));
}}
"""

# ------------------------------------------------------------
# Step 3 — Render methods
# ------------------------------------------------------------
def parse_interface(header_text):
    """Extract the first abstract class and its virtual methods."""
    # Ignore enums, structs, and unions
    match = re.search(
        r'(?<!enum\s)(?<!struct\s)(?<!union\s)\bclass\s+(\w+)\s*\{([\s\S]*?)\};',
        header_text
    )
    if not match:
        raise ValueError("No abstract class found")

    name = match.group(1)
    body = match.group(2)

    # Find all virtual pure methods
    virtuals = re.findall(r'virtual\s+([^;]+?)\s*=\s*0\s*;', body)
    if not virtuals:
        raise ValueError("No virtual methods found")

    return name, virtuals



def generate_forwarders(interface_name, virtuals):
    """Generate bridge and proxy forwarding functions, with arguments and const."""
    bridge_methods = []
    proxy_methods = []

    for v in virtuals:
        v = v.strip()

        # Match return type, name, args, const qualifier
        m = re.match(r'(.+?)\s+([A-Za-z_]\w*)\s*\(([^)]*)\)(\s*const)?', v)
        if not m:
            continue

        ret_type = m.group(1).strip()
        func_name = m.group(2)
        args = m.group(3).strip()
        constness = m.group(4) or ""

        # Collect argument names for forwarding
        arg_names = []
        if args and args != 'void':
            for part in args.split(','):
                nm = re.search(r'(\w+)(\s*(?:=\s*[^,]+)?)?$', part.strip())
                if nm:
                    arg_names.append(nm.group(1))
        call_args = ", ".join(arg_names)

        # Bridge method (forwards to impl_)
        call_stmt = f"impl_->{func_name}({call_args});" if ret_type == "void" else f"return impl_->{func_name}({call_args});"
        bridge_methods.append(f"    {ret_type} {func_name}({args}){constness} {{ {call_stmt} }}")

        # Proxy method (forwards to bridge_)
        proxy_call_stmt = f"bridge_->{func_name}({call_args});" if ret_type == "void" else f"return bridge_->{func_name}({call_args});"
        proxy_methods.append(f"    inline {ret_type} {func_name}({args}){constness} override {{ {proxy_call_stmt} }}")

    return "\n".join(bridge_methods), "\n".join(proxy_methods)


def generate_files(header_path):
    header_path = Path(header_path)
    orig_header = header_path.name
    header_text = header_path.read_text(encoding="utf-8")

    interface_name, virtuals = parse_interface(header_text)
    bridge_methods, proxy_methods = generate_forwarders(interface_name, virtuals)


    h_out = TPL_HEADER.format(
        orig_header=orig_header,
        interface_name=interface_name,
        bridge_methods=bridge_methods,
        proxy_methods=proxy_methods,
    )

    out_file = header_path.parent / "Stable" /f"{interface_name}.h"
    print(out_file)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(h_out, encoding="utf-8")
    print(f"✅ Generated generated/{out_file.name} from {orig_header}")

# ------------------------------------------------------------
# Step 5 — Command line entry
# ------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bridgegen.py <interface-header>")
        sys.exit(1)

    generate_files(sys.argv[1])
