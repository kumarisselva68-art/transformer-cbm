# -*- coding: utf-8 -*-
"""
Master assembler for Version 3.0 specification:
Combines document preamble, Sections 1-8, Sections 9-15, and Sections 16-24
into documentation/transformer_cbm_spec.typ.
"""

import os
from build_v3_document import generate_v3
from build_v3_sections_1_to_8 import get_sections_1_to_8
from build_v3_sections_9_to_15 import get_sections_9_to_15
from build_v3_sections_16_to_24 import get_sections_16_to_24

def assemble():
    output_path = os.path.join("documentation", "transformer_cbm_spec.typ")
    
    parts = []
    print("1. Generating preamble and cover page...")
    parts.append(generate_v3())
    
    print("2. Generating Sections 1-8...")
    parts.append(get_sections_1_to_8())
    
    print("3. Generating Sections 9-15...")
    parts.append(get_sections_9_to_15())
    
    print("4. Generating Sections 16-24...")
    parts.append(get_sections_16_to_24())
    
    full_content = "\n".join(parts)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_content)
        
    print(f"Successfully assembled {output_path} ({len(full_content)} bytes, {len(full_content.splitlines())} lines).")

if __name__ == "__main__":
    assemble()
