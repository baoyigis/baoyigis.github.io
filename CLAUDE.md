# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## About the Owner

**Name**: 鲍毅 (Yi Bao)

**Position**: Assistant Professor at Nanjing University (Institute of Space Earth Science)

**Research Interests**:
- Urban spatiotemporal big data mining and sustainable development
- High-resolution urban built environment research
- Interaction mechanisms between built environment and human activities
- Geographic intelligence (LLM and GeoAI applications)

**Contact**: baoyi AT nju.edu.cn

**Note**: Please remember the owner's name is **鲍毅** (Bao Yi), not "Yi Bao" in isolation. When referring to the owner, use the full name "Yi Bao" or Chinese name "鲍毅".

## Project Overview

This is an academic website built with [Jekyll](https://jekyllrb.com/) using the [al-folio](https://github.com/alshedivat/al-folio) theme. It is deployed to GitHub Pages and automatically builds on every push to the `main` branch.

## Essential Commands

### Local Development

```bash
# Using Docker (recommended)
docker compose pull    # Pull latest image
docker compose up     # Start development server (http://localhost:8080)

# Using Docker with slim image
docker compose -f docker-compose-slim.yml up

# Using Ruby/Bundler directly (requires Ruby, Bundler, Python)
bundle install
pip install jupyter
bundle exec jekyll serve   # Serve at http://localhost:4000
```

### Building & Deployment

```bash
# Build the site (generates _site/ directory)
bundle exec jekyll build

# Build for production with optimized CSS
bundle exec jekyll build
purgecss -c purgecss.config.js   # Remove unused CSS

# Deploy to GitHub Pages (via script)
bin/deploy

# GitHub Actions automatically deploys on push to main branch
# Manual deployment: Actions -> Deploy -> Run workflow
```

### Code Quality

```bash
# Format code with Prettier (includes Liquid plugin)
npm install
npx prettier --write .   # Format all files
npx prettier --check .   # Check formatting

# Run CI build
bin/cibuild
```

### Updating Citations

```bash
# Update Google Scholar citations (requires PAT)
bin/update_scholar_citations.py
```

## Architecture

### Jekyll Theme Structure

This is a **Jekyll static site generator** project with the following architecture:

- **Collections**: Content types (`news`, `projects`, `books`, `posts`)
- **Layouts**: Page templates in [`_layouts/`](_layouts/) (Liquid templates)
- **Includes**: Reusable components in [`_includes/`](_includes/)
- **Data Files**: Configuration data in [`_data/`](_data/) (YAML files)
- **Plugins**: Ruby gems in [`_plugins/`](_plugins/) for custom functionality

### Key Directories

```
├── _bibliography/     # BibTeX files for publications
├── _books/            # Book review pages
├── _data/             # YAML data files (cv.yml, socials.yml, etc.)
├── _includes/         # Reusable Liquid components
├── _layouts/          # Page layout templates
├── _news/             # News items (displayed on about page)
├── _pages/            # Site pages (about.md, projects.md, etc.)
├── _plugins/          # Custom Jekyll plugins
├── _posts/            # Blog posts (format: YYYY-MM-DD-title.md)
├── _projects/         # Project portfolio items
├── _sass/             # SASS/SCSS stylesheets
├── assets/            # Static assets (images, PDFs, JS, CSS)
└── bin/               # Shell scripts (deploy, cibuild, etc.)
```

### Configuration Flow

1. **[`_config.yml`](_config.yml)**: Main Jekyll configuration (site settings, plugins, collections)
2. **[`_data/`](_data/)**: Content data (social links, CV, repositories, venues)
3. **Front matter**: YAML in each page/post controls layout and metadata
4. **Jekyll Scholar**: Processes BibTeX bibliography from [`_bibliography/papers.bib`](_bibliography/)

### Layout System

Pages use layouts defined in front matter:

- `about`: Profile page with news section
- `bib`: Publications page (from BibTeX)
- `cv`: Curriculum vitae page
- `distill`: Academic blog post style (distill.pub)
- `page`: Standard page with sidebar
- `post`: Blog post
- `profiles`: Multi-person profiles page

### Collections & Content Types

- **News**: Items in [`_news/`](_news/) displayed on about page (via [`_includes/news.liquid`](_includes/news.liquid))
- **Projects**: Portfolio items in [`_projects/`](_projects/) with categories
- **Posts**: Blog posts in [`_posts/`](_posts/) with `YYYY-MM-DD-title.md` naming
- **Books**: Book reviews in [`_books/`](_books/)
- **Publications**: Auto-generated from [`_bibliography/papers.bib`](_bibliography/)

### Key Custom Plugins

Located in [`_plugins/`](_plugins/):

- **`google-scholar-citations.rb`**: Fetches Google Scholar citation counts
- **`inspirehep-citations.rb`**: Fetches InspireHEP citations
- **`external-posts.rb`**: Imports posts from external RSS feeds
- **`cache-bust.rb`**: Cache busting for assets

## Common Customizations

### Modifying Site Content

- **Personal info**: [`_config.yml`](_config.yml) (title, name, url, etc.)
- **Social links**: [`_data/socials.yml`](_data/socials.yml)
- **CV**: [`_data/cv.yml`](_data/cv.yml) OR [`assets/json/resume.json`](assets/json/resume.json)
- **Publications**: [`_bibliography/papers.bib`](_bibliography/)
- **News**: Add files to [`_news/`](_news/)
- **Projects**: Add files to [`_projects/`](_projects/)
- **Blog posts**: Add files to [`_posts/`](_posts/)

### Adding New Pages

Create new Markdown files in [`_pages/`](_pages/):

```yaml
---
layout: page
title: Page Title
permalink: /page-url/
---
```

### Theme Customization

- **Colors**: [`_sass/_themes.scss`](_sass/_themes.scss)
- **Fonts**: [`_sass/_variables.scss`](_sass/_variables.scss)
- **Styles**: [`_sass/_base.scss`](_sass/_base.scss), [`_sass/_layout.scss`](_sass/_layout.scss)

### BibTeX Publication Entry

Add to [`_bibliography/papers.bib`](_bibliography/):

```bibtex
@article{key2024,
  author = {Bao, Yi and Others},
  title = {Paper Title},
  journal = {Journal Name},
  year = {2024},
  pdf = {assets/pdf/paper.pdf},
  arxiv = {1234.56789},
  selected = true
}
```

Supported custom fields: `abstract`, `altmetric`, `arxiv`, `bibtex_show`, `blog`, `code`, `doi`, `html`, `pdf`, `poster`, `slides`, `supp`, `video`, `website`.

## Deployment

- **GitHub Actions**: Automatically deploys on push to `main` branch
- **Output branch**: `gh-pages` (auto-generated, do not edit)
- **Workflow**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
- **Production URL**: Configured in [`_config.yml`](_config.yml) (`url` and `baseurl`)

## Important Notes

- All edits to the `main` branch only; `gh-pages` is auto-generated
- Changes to [`_config.yml`](_config.yml) require rebuilding the site
- Liquid templates use `.liquid` extension (not `.html`)
- Blog posts require `YYYY-MM-DD-title.md` filename format
- BibTeX entries support custom fields for buttons/badges
- ImageMagick is used for responsive image generation (WebP format)
