# Personal Research Portfolio

A clean, academic-style Jekyll site for showcasing research in neuromorphic computing and efficient AI systems.

## Quick Start

### Local Development

1. **Install Ruby** (if not already installed)
   ```bash
   # macOS (using Homebrew)
   brew install ruby
   
   # Ubuntu/Debian
   sudo apt-get install ruby-full build-essential
   ```

2. **Install Jekyll and dependencies**
   ```bash
   gem install bundler jekyll
   cd portfolio-site
   bundle install
   ```

3. **Run locally**
   ```bash
   bundle exec jekyll serve
   ```
   Visit `http://localhost:4000` in your browser.

### Deploy to GitHub Pages

1. **Create a new repository** on GitHub named `yourusername.github.io`

2. **Push your site**
   ```bash
   cd portfolio-site
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Select "Deploy from a branch"
   - Choose `main` branch, `/ (root)` folder
   - Your site will be live at `https://yourusername.github.io`

## Customization

### Site Configuration (`_config.yml`)

```yaml
title: "Your Name"
description: "Your research tagline"
author: "Your Name"
email: your.email@example.com
url: "https://yourusername.github.io"
```

### Adding Content

**New Blog Post:**
Create a file in `_posts/` with the format `YYYY-MM-DD-title.md`:

```markdown
---
layout: post
title: "Your Post Title"
date: 2025-02-15
tags: [research, announcement]
---

Your content here...
```

**New Research Project:**
Create a file in `_research/` (or add to `research.html` directly):

```markdown
---
layout: research-item
title: "Project Title"
description: "Brief description"
tags: [tag1, tag2]
---

Detailed project description...
```

### Styling

All CSS is embedded in `_layouts/default.html` for simplicity. Key CSS variables:

```css
:root {
  --color-primary: #1e3a5f;    /* Main accent color */
  --color-accent: #c4a052;      /* Secondary accent */
  --font-display: 'Crimson Pro'; /* Headings */
  --font-body: 'IBM Plex Sans';  /* Body text */
}
```

### Adding Your Photo

Replace the placeholder in `index.html`:
```html
<img src="/assets/images/profile.jpg" alt="Your Name" style="width: 100%; height: 100%; object-fit: cover; border-radius: 12px;">
```

## File Structure

```
portfolio-site/
├── _config.yml          # Site configuration
├── _layouts/
│   ├── default.html     # Main layout with CSS
│   ├── post.html        # Blog post layout
│   └── research-item.html
├── _includes/
│   ├── header.html      # Navigation
│   └── footer.html      # Footer links
├── _posts/              # Blog posts
├── _research/           # Research project pages (optional)
├── assets/
│   └── images/          # Your images
├── index.html           # Home page
├── research.html        # Research overview
├── publications.html    # Publications list
├── news.html            # Blog/news index
├── contact.html         # Contact info
├── Gemfile              # Ruby dependencies
└── README.md
```

## Tips

- **Images**: Optimize images before uploading (compress, resize to ~800px width)
- **SEO**: The `jekyll-seo-tag` plugin handles meta tags automatically
- **Performance**: The embedded CSS approach keeps everything fast and simple
- **Updates**: Edit `publications.html` directly, or create a `_data/publications.yml` for easier management

## License

MIT License - feel free to use and modify for your own portfolio.
