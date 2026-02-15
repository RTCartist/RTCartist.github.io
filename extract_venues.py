#!/usr/bin/env python3
"""
Script to extract journal/conference names from PDF URLs and update publications.yml
"""

import yaml
import re
from urllib.parse import urlparse

# Mapping of domain patterns to journal/conference names
VENUE_MAPPING = {
    'nature.com': 'Nature',
    'springer.com': 'Springer',
    'ieee.org': 'IEEE',
    'ieeexplore.ieee.org': 'IEEE',
    'arxiv.org': 'arXiv',
    'jamanetwork.com': 'JAMA Network Open',
    'mdpi.com': 'MDPI',
    'wiley.com': 'Wiley',
    'advanced.onlinelibrary.wiley.com': 'Advanced Materials',
    'iopscience.iop.org': 'IOP Publishing',
    'pmc.ncbi.nlm.nih.gov': 'PMC',
    'scholar.google.com': 'Google Scholar',
    'repository.cam.ac.uk': 'Cambridge Repository',
    'researchsquare.com': 'Research Square',
    'ui.adsabs.harvard.edu': 'arXiv',
}

# More specific patterns
SPECIFIC_VENUES = {
    r'jamanetwork\.com.*jamanetworkopen': 'JAMA Network Open',
    r'advanced\.onlinelibrary\.wiley\.com.*adma': 'Advanced Materials',
    r'advanced\.onlinelibrary\.wiley\.com.*aelm': 'Advanced Electronic Materials',
    r'advanced\.onlinelibrary\.wiley\.com.*adsr': 'Advanced Science',
    r'mdpi\.com.*2079-6374': 'Biosensors',
    r'ieeexplore\.ieee\.org': 'IEEE',
    r'iopscience\.iop\.org.*2634-4386': 'Neuromorphic Computing and Engineering',
    r'iopscience\.iop\.org.*1361-6463': 'Journal of Physics D: Applied Physics',
    r'nature\.com.*s41467': 'Nature Communications',
    r'nature\.com.*s43588': 'Nature Computational Science',
}

def extract_venue_from_url(url):
    """Extract venue name from URL"""
    if not url:
        return None
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Check specific patterns first
        for pattern, venue in SPECIFIC_VENUES.items():
            if re.search(pattern, url, re.IGNORECASE):
                return venue
        
        # Check domain mapping
        for domain_pattern, venue in VENUE_MAPPING.items():
            if domain_pattern in domain:
                return venue
        
        # Try to extract from path
        path = parsed.path.lower()
        if 'journal' in path:
            # Try to extract journal name from path
            parts = [p for p in path.split('/') if p and p not in ['journals', 'journal', 'articles', 'article']]
            if parts:
                # Capitalize first letter of each word
                journal = ' '.join(word.capitalize() for word in parts[0].replace('-', ' ').split())
                return journal
        
        return None
    except Exception as e:
        print(f"  Error parsing URL {url}: {e}")
        return None

def update_venues(filename='_data/publications.yml'):
    """Update venue information in publications.yml"""
    print(f"Reading {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data or 'publications' not in data:
        print("No publications found in file")
        return
    
    print(f"Found {len(data['publications'])} publications")
    print("Extracting venue information from URLs...")
    
    updated_count = 0
    for pub in data['publications']:
        # Skip if venue already exists
        if pub.get('venue') and pub['venue'].strip() != '':
            continue
        
        # Try to extract from PDF link
        venue = None
        if pub.get('links') and pub['links']:
            if pub['links'].get('pdf'):
                venue = extract_venue_from_url(pub['links']['pdf'])
            elif pub['links'].get('arxiv'):
                venue = 'arXiv preprint'
            elif pub['links'].get('doi'):
                venue = extract_venue_from_url(pub['links']['doi'])
        
        if venue:
            pub['venue'] = venue
            updated_count += 1
            print(f"  Updated: {pub['title'][:50]}... -> {venue}")
    
    if updated_count > 0:
        print(f"\nUpdated {updated_count} publications")
        print(f"Writing updated data to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print("Done! Venue information has been updated.")
    else:
        print("No venues needed updating (all already have venue information or no URLs found).")

if __name__ == "__main__":
    update_venues()

