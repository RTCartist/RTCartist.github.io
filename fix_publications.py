#!/usr/bin/env python3
"""
Script to fix the broken authors field in publications.yml
The authors field appears to be split into individual characters instead of strings.
"""

import yaml
import re

def reconstruct_authors_from_chars(char_list):
    """Reconstruct author names from a list of individual characters"""
    if not char_list:
        return ""
    
    # The pattern is: ['C', 'h', 'e', 'n', 'y', 'u', '', 'T', 'a', 'n', 'g', '', 'a', 'n', 'd', '', ...]
    # Empty strings represent spaces, and we need to detect word boundaries
    result = []
    current_word = []
    
    for i, item in enumerate(char_list):
        char = str(item).strip()
        
        # Skip commas that might be in the list
        if char == ',' or char == '':
            # Empty string or comma indicates a potential word boundary
            if current_word:
                # Finish current word
                word = ''.join(current_word)
                result.append(word)
                current_word = []
            # If it's an empty string, add a space marker
            if char == '' and i < len(char_list) - 1:
                # Check if next char starts a new word (capital letter)
                next_idx = i + 1
                while next_idx < len(char_list) and str(char_list[next_idx]).strip() == '':
                    next_idx += 1
                if next_idx < len(char_list):
                    next_char = str(char_list[next_idx]).strip()
                    if next_char and next_char[0].isupper():
                        # This is likely a new name, so add space
                        if result and not result[-1].endswith(','):
                            result.append(' ')
        elif char and char.isalnum():
            current_word.append(char)
        elif char:
            # Punctuation or other characters
            if current_word:
                result.append(''.join(current_word))
                current_word = []
            # Handle special cases like "and" which might be split
            if char in [',', '.', '&']:
                result.append(char)
    
    # Add the last word
    if current_word:
        result.append(''.join(current_word))
    
    # Join everything
    authors_str = ''.join(result)
    
    # Clean up: fix "and" patterns and add proper commas
    # Pattern: "Name1and Name2" -> "Name1, Name2"
    # Pattern: "Name1 and Name2" -> "Name1, Name2" (sometimes)
    authors_str = re.sub(r'([a-z])([A-Z])', r'\1, \2', authors_str)  # Add comma between lowercase and uppercase
    authors_str = re.sub(r'([a-z])\s+and\s+([A-Z])', r'\1, \2', authors_str)  # Replace " and " with ", "
    authors_str = re.sub(r'([a-z])and\s+([A-Z])', r'\1, \2', authors_str)  # Replace "and " with ", "
    authors_str = re.sub(r'\s+', ' ', authors_str)  # Multiple spaces to single
    authors_str = re.sub(r'\s*,\s*', ', ', authors_str)  # Space after comma
    
    return authors_str.strip()

def highlight_author_name(authors_str, name="Shengbo Wang"):
    """Highlight the author's name in the authors string"""
    if not authors_str or not name:
        return authors_str
    
    # Try different variations of the name
    name_variations = [
        name,
        name.split()[0] + " " + name.split()[-1],  # First Last
        name.split()[0][0] + ". " + name.split()[-1],  # F. Last
    ]
    
    for name_var in name_variations:
        if name_var in authors_str and f"<strong>{name_var}</strong>" not in authors_str:
            authors_str = authors_str.replace(name_var, f"<strong>{name_var}</strong>")
            break
    
    return authors_str

def fix_publications_file(filename='_data/publications.yml'):
    """Fix the publications YAML file"""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data or 'publications' not in data:
        print("No publications found in file")
        return
    
    print(f"Found {len(data['publications'])} publications")
    print("Fixing authors fields...")
    
    fixed_count = 0
    for pub in data['publications']:
        if 'authors' in pub:
            original = pub['authors']
            needs_fix = False
            # If authors is a list of single characters, it's broken
            if isinstance(original, list):
                # Check if it's a list of single characters (the broken format)
                if len(original) > 0:
                    # Check if most items are single characters
                    char_count = sum(1 for c in original if isinstance(c, str) and len(c.strip()) == 1 and c.strip().isalnum())
                    if char_count > len(original) * 0.5:  # More than 50% are single chars
                        # Reconstruct the string
                        reconstructed = reconstruct_authors_from_chars(original)
                        pub['authors'] = reconstructed
                        fixed_count += 1
                        print(f"  Fixed: {pub['title'][:50]}...")
                    else:
                        # It's a proper list of author names
                        pub['authors'] = ', '.join(str(a).strip() for a in original if str(a).strip())
                        fixed_count += 1
                        print(f"  Fixed (list): {pub['title'][:50]}...")
            elif isinstance(original, str):
                # Check if it needs formatting (missing commas between names)
                # Pattern: "Name1and Name2" or "Name1Name2" (no spaces/commas)
                if re.search(r'([a-z])([A-Z])', original) or 'and' in original.lower():
                    # Fix formatting: add commas between names
                    fixed = re.sub(r'([a-z])([A-Z])', r'\1, \2', original)
                    fixed = re.sub(r'([a-z])\s+and\s+([A-Z])', r'\1, \2', fixed, flags=re.IGNORECASE)
                    fixed = re.sub(r'([a-z])and\s+([A-Z])', r'\1, \2', fixed, flags=re.IGNORECASE)
                    fixed = re.sub(r'\s+', ' ', fixed)  # Normalize spaces
                    fixed = re.sub(r'\s*,\s*', ', ', fixed)  # Normalize commas
                    pub['authors'] = fixed.strip()
                    needs_fix = True
                    fixed_count += 1
                    print(f"  Fixed formatting: {pub['title'][:50]}...")
            
            # Always check and add name highlighting if needed
            if isinstance(pub['authors'], str):
                highlighted = highlight_author_name(pub['authors'])
                if highlighted != pub['authors']:
                    pub['authors'] = highlighted
                    if not needs_fix:
                        fixed_count += 1
                        print(f"  Added highlighting: {pub['title'][:50]}...")
    
    if fixed_count > 0:
        print(f"\nFixed {fixed_count} publications")
        print(f"Writing fixed data to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print("Done! Please review the file and manually fix any remaining issues.")
    else:
        print("No issues found or unable to auto-fix. The authors may need manual correction.")

if __name__ == "__main__":
    fix_publications_file()

