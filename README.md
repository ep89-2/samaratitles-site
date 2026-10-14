# samaratitles.com

The Samara Titles website: a home page for Tumbledew, plus the Support and Privacy Policy pages that the App Store listing links to.

- `docs/` is the published site. GitHub Pages serves it from the `main` branch, `/docs` folder, at https://samaratitles.com.
- `page-copy.md` holds the words for every page. The Support and Privacy pages are generated from it.
- `build.py` regenerates `docs/` after the copy changes: `pip install markdown && python3 build.py`.

Nunito Sans is self-hosted (`docs/assets/fonts/`, SIL Open Font License, see `OFL.txt`), so the site loads nothing from other companies.
