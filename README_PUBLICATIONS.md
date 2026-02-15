# Fetching Publications from Google Scholar

This guide explains how to automatically fetch your publications from Google Scholar and display them on your website.

## Setup

1. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update the script with your information:**
   - Open `fetch_publications.py`
   - Update `YOUR_NAME` variable to match how your name appears in publications (line 13)
   - The `SCHOLAR_ID` is already set to your Google Scholar ID

## Usage

Run the script to fetch publications:

```bash
python fetch_publications.py
```

The script will:
- Fetch all publications from your Google Scholar profile
- Extract titles, authors, venues, years, and links
- Highlight your name in author lists
- Save everything to `_data/publications.yml`

## Manual Editing

After running the script, you can manually edit `_data/publications.yml` to:
- Add additional links (code repositories, project pages, videos, etc.)
- Fix any formatting issues
- Add publications not on Google Scholar
- Reorder or remove publications

## Troubleshooting

**Rate Limiting:** Google Scholar may rate-limit requests. If you get errors:
- Wait a few minutes and try again
- The script includes delays between requests to be polite

**Missing Data:** Some publications may have incomplete information:
- Manually add missing links or details in the YAML file
- Check that your Google Scholar profile is complete

**Author Highlighting:** If your name isn't being highlighted:
- Update the `YOUR_NAME` variable in the script
- Manually edit the YAML file to add `<strong>` tags around your name

## YAML Structure

Each publication entry looks like:
```yaml
- title: "Paper Title"
  authors: "Author One, <strong>Your Name</strong>, Author Two"
  venue: "Conference/Journal Name"
  year: 2024
  type: "conference"  # or "journal", "preprint"
  links:
    pdf: "https://..."
    arxiv: "https://..."
    doi: "https://..."
    code: "https://..."
```

## Updating Your Site

After updating the publications file:
1. Commit and push to GitHub
2. GitHub Pages will automatically rebuild your site
3. Your publications will appear on the `/publications/` page

