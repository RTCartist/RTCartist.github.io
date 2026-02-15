#!/usr/bin/env python3
"""
Script to fetch publications from Google Scholar and generate publications.yml
Usage: python fetch_publications.py
"""

import yaml
import re
from scholarly import scholarly
import time
from urllib.parse import urlparse

# Your Google Scholar user ID
SCHOLAR_ID = "VywDS3AAAAAJ"

# Your name for highlighting in author lists
YOUR_NAME = "Shengbo Wang"  # Update this to match how your name appears

def highlight_author(authors_str, your_name):
    """Bold your name in the authors string"""
    # Try different variations of the name
    name_variations = [
        your_name,
        your_name.split()[0] + " " + your_name.split()[-1],  # First Last
        your_name.split()[0][0] + ". " + your_name.split()[-1],  # F. Last
    ]
    
    for name_var in name_variations:
        if name_var in authors_str:
            # Use HTML strong tag for Jekyll
            authors_str = authors_str.replace(name_var, f"<strong>{name_var}</strong>")
            break
    
    return authors_str

def extract_year(publication):
    """Extract year from publication data"""
    if 'pub_year' in publication:
        return publication['pub_year']
    # Try to extract from bib entry
    if 'bib' in publication and 'pub_year' in publication['bib']:
        return publication['bib']['pub_year']
    # Try to extract from title or venue
    if 'bib' in publication:
        venue = publication['bib'].get('venue', '')
        year_match = re.search(r'\b(19|20)\d{2}\b', venue)
        if year_match:
            return int(year_match.group())
    return None

def extract_venue_from_url(url):
    """Extract venue name from URL (simplified version)"""
    if not url:
        return ''
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Common journal/conference domains
        if 'nature.com' in domain:
            if 's41467' in url:
                return 'Nature Communications'
            elif 's43588' in url:
                return 'Nature Computational Science'
            return 'Nature'
        elif 'ieeexplore.ieee.org' in domain or 'ieee.org' in domain:
            return 'IEEE'
        elif 'arxiv.org' in domain:
            return 'arXiv'
        elif 'jamanetwork.com' in domain:
            return 'JAMA Network Open'
        elif 'wiley.com' in domain or 'onlinelibrary.wiley.com' in domain:
            if 'adma' in url.lower():
                return 'Advanced Materials'
            elif 'aelm' in url.lower():
                return 'Advanced Electronic Materials'
            return 'Wiley'
        elif 'mdpi.com' in domain:
            return 'MDPI'
        elif 'iopscience.iop.org' in domain:
            return 'IOP Publishing'
    except:
        pass
    
    return ''

def extract_links(publication):
    """Extract relevant links from publication"""
    links = {}
    
    # PDF link
    if 'eprint_url' in publication:
        links['pdf'] = publication['eprint_url']
    elif 'pub_url' in publication:
        links['pdf'] = publication['pub_url']
    
    # ArXiv link
    if 'eprint_url' in publication and 'arxiv' in publication['eprint_url'].lower():
        links['arxiv'] = publication['eprint_url']
    
    # DOI
    if 'bib' in publication and 'doi' in publication['bib']:
        doi = publication['bib']['doi']
        if not doi.startswith('http'):
            doi = f"https://doi.org/{doi}"
        links['doi'] = doi
    
    return links

def fetch_publications():
    """Fetch publications from Google Scholar"""
    print(f"Fetching publications for Scholar ID: {SCHOLAR_ID}")
    
    try:
        # Get the author
        author = scholarly.fill(scholarly.search_author_id(SCHOLAR_ID))
        
        publications_list = []
        
        # Fetch publications
        print(f"Found {len(author.get('publications', []))} publications")
        
        for pub in author.get('publications', []):
            try:
                # Fill in publication details
                filled_pub = scholarly.fill(pub)
                
                bib = filled_pub.get('bib', {})
                title = bib.get('title', 'Untitled')
                
                # Handle authors - can be a list or string
                author_list = bib.get('author', [])
                if isinstance(author_list, str):
                    authors = author_list
                elif isinstance(author_list, list):
                    authors = ', '.join(str(a) for a in author_list if a)
                else:
                    authors = ''
                
                # Get venue - try multiple fields
                venue = bib.get('venue', '') or bib.get('journal', '') or bib.get('publisher', '')
                
                # If venue is still empty, try to extract from URL
                if not venue or venue.strip() == '':
                    venue = extract_venue_from_url(filled_pub.get('eprint_url') or filled_pub.get('pub_url', ''))
                
                # Skip if no title
                if not title or title == 'Untitled':
                    continue
                
                year = extract_year(filled_pub)
                links = extract_links(filled_pub)
                
                # Determine type
                pub_type = "journal"
                venue_lower = venue.lower()
                if any(word in venue_lower for word in ['conference', 'proceedings', 'workshop']):
                    pub_type = "conference"
                elif any(word in venue_lower for word in ['arxiv', 'preprint']):
                    pub_type = "preprint"
                
                # Highlight author name
                authors_highlighted = highlight_author(authors, YOUR_NAME)
                
                pub_entry = {
                    'title': title,
                    'authors': authors_highlighted,
                    'venue': venue,
                    'year': year,
                    'type': pub_type,
                    'links': links if links else None
                }
                
                publications_list.append(pub_entry)
                
                print(f"  - {title[:60]}... ({year})")
                
                # Be polite to Google Scholar
                time.sleep(1)
                
            except Exception as e:
                print(f"  Error processing publication: {e}")
                continue
        
        # Sort by year (newest first)
        publications_list.sort(key=lambda x: x['year'] if x['year'] else 0, reverse=True)
        
        # Group by year
        publications_by_year = {}
        for pub in publications_list:
            year = pub['year'] if pub['year'] else 'Unknown'
            if year not in publications_by_year:
                publications_by_year[year] = []
            publications_by_year[year].append(pub)
        
        # Convert to YAML structure - keep year in each entry for grouping
        yaml_data = {'publications': []}
        for year in sorted(publications_by_year.keys(), reverse=True):
            for pub in publications_by_year[year]:
                # Keep year in entry for template grouping
                yaml_data['publications'].append(pub)
        
        return yaml_data
        
    except Exception as e:
        print(f"Error fetching publications: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have installed: pip install scholarly")
        print("2. Check your internet connection")
        print("3. Google Scholar may rate-limit requests - try again later")
        return None

def save_to_yaml(data, filename='_data/publications.yml'):
    """Save publications data to YAML file"""
    if data is None:
        return
    
    # Ensure authors are strings, not lists
    for pub in data.get('publications', []):
        if 'authors' in pub and isinstance(pub['authors'], list):
            pub['authors'] = ', '.join(str(a) for a in pub['authors'] if a)
    
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\n✓ Saved {len(data['publications'])} publications to {filename}")

if __name__ == "__main__":
    print("=" * 60)
    print("Google Scholar Publications Fetcher")
    print("=" * 60)
    
    data = fetch_publications()
    
    if data:
        save_to_yaml(data)
        print("\n✓ Done! Your publications have been updated.")
        print("\nNote: You may need to manually:")
        print("  - Review and edit the generated YAML file")
        print("  - Add additional links (code, project pages, etc.)")
        print("  - Verify author name highlighting")
    else:
        print("\n✗ Failed to fetch publications. Please check the error messages above.")

