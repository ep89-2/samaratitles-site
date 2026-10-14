"""Builds the site into docs/, which GitHub Pages publishes.
Support and Privacy text comes from page-copy.md, so edit the words there.
Run: python3 build.py   (needs: pip install markdown)"""
import re
from pathlib import Path
import markdown

ROOT = Path(__file__).parent
HERE = ROOT / "docs"
COPY = (ROOT / "page-copy.md").read_text()

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/tumbledew-icon.png">
<link rel="preload" href="assets/fonts/nunito-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css">
</head><body>
<header class="site-header"><div class="wrap">
  <a class="logo" href="index.html"><img src="assets/samara-logo-white.png" alt="Samara Titles"></a>
  <nav><a href="support.html"{s}>Support</a><a href="privacy.html"{p}>Privacy</a></nav>
</div></header>
"""
FOOT = """<footer class="site-footer"><div class="wrap">
  <div><a href="support.html">Support</a><a href="privacy.html">Privacy Policy</a></div>
  <div>&copy; 2026 Samara Titles</div>
</div></footer>
</body></html>
"""


def seo(name):
    part = COPY.split(f"## Page {name}")[1]
    return re.search(r"\*\*SEO description:\*\* (.+)", part).group(1).strip()


def head(title, cur="", desc=""):
    return HEAD.format(title=title, desc=desc, s=' aria-current="page"' if cur == "s" else "",
                       p=' aria-current="page"' if cur == "p" else "")


def section(name):
    """The blockquoted body of one page in the copy file, unquoted."""
    part = COPY.split(f"## Page {name}")[1].split("\n---\n")[0]
    lines = [l[2:] if l.startswith("> ") else ("" if l == ">" else None)
             for l in part.splitlines()]
    return "\n".join(l for l in lines if l is not None)


def doc_html(md):
    html = markdown.markdown(md)
    html = html.replace('href="/privacy"', 'href="privacy.html"')
    # Questions in bold on their own line become small headings.
    html = re.sub(r"<p><strong>([^<]+\?)</strong>\n?", r"<h3>\1</h3><p>", html)
    html = re.sub(r"<p><strong>(I bought[^<]+)</strong>\n?", r"<h3>\1</h3><p>", html)
    html = re.sub(r"\[([A-Z][A-Z ,.'/]+[A-Z.]*)\]", r'<span class="ph">[\1]</span>', html)
    return html


def build_doc(fname, name, title, cur, short_version_box=False):
    html = doc_html(section(name))
    page_head = head(title, cur, seo(name))
    if short_version_box:
        html = re.sub(r"(<h2>The short version</h2>\s*)(<ul>.*?</ul>)",
                      r'\1<div class="callout">\2</div>', html, flags=re.S)
    (HERE / fname).write_text(page_head + f'<main class="doc"><div class="wrap">{html}</div></main>\n' + FOOT)


INDEX = head("Tumbledew for iPhone · Samara Titles", "", seo("1")) + """
<main>
<section class="sky hero">
  <div class="wrap">
    <div>
      <img class="app-icon" src="assets/tumbledew-icon.png" alt="Tumbledew app icon">
      <h1>Tumbledew</h1>
      <p class="tagline">Roll. Flip gravity. Dodge the rain.</p>
      <p>Dewey is a small cut-paper alien caught in a downpour. Roll left and right along the grass, flip gravity to run along the clouds instead, and catch the power-ups drifting across the sky.</p>
      <span class="button">Coming soon to the App Store</span>
      <p class="fine">Free on iPhone · Optional one-time ad-free upgrade</p>
    </div>
    <img class="shot" src="assets/1-menu.jpg" alt="Tumbledew main menu with Dewey on the grass">
  </div>
  <div class="grass" aria-hidden="true"></div>
</section>

<section class="sky" style="padding-top:72px">
  <div class="wrap">
    <p class="label">How it plays</p>
    <h2>Three moves, one rainy sky</h2>
    <div class="cols">
      <div><img class="shot" src="assets/2-play.jpg" alt="Dewey rolling under the rain"><h3>Roll</h3><p class="muted">Hold a thumb in the lower left or lower right of the screen to roll that way.</p></div>
      <div><img class="shot" src="assets/3-upside-down.jpg" alt="Dewey upside down on the clouds"><h3>Flip</h3><p class="muted">Double-tap the middle of the screen to invert gravity. Time slows for a moment while the world turns over.</p></div>
      <div><img class="shot" src="assets/4-snow.jpg" alt="Rain turned to snow"><h3>Catch</h3><p class="muted">Snowflakes, suns and hearts float across, out of reach from either ground. Flip at the right moment to catch them on the way across.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What's inside</h2>
    <ul class="features">
      <li><strong>Three power-ups</strong><span>The snowflake turns the rain to slow, drifting snow for 30 seconds, the sun thins out the rain, and the heart gives back a hit.</span></li>
      <li><strong>Forty-five levels</strong><span>Every 50 drops the rain falls a little faster and a little thicker.</span></li>
      <li><strong>Three hearts</strong><span>Dewey can take two hits. The third ends the game.</span></li>
      <li><strong>Game Center</strong><span>A weekly leaderboard and 17 achievements, if you're signed in. The game plays the same if you aren't.</span></li>
      <li><strong>Your high score follows you</strong><span>It is saved on your iPhone and kept in step across your devices through iCloud.</span></li>
      <li><strong>Made for headphones</strong><span>An original score, a snowfall theme, and stereo sound effects placed where they happen on screen.</span></li>
      <li><strong>No ads, if you prefer</strong><span>A single in-app purchase removes the ad on the game-over screen for good, on every device signed in to your Apple Account.</span></li>
    </ul>
  </div>
</section>

<section class="studio">
  <div class="wrap">
    <img src="assets/samara-logo-white.png" alt="Samara Titles">
    <p>Samara Titles is an independent studio making small, carefully finished games for iPhone. A samara is the winged seed of a maple tree: the one that spins as it falls. Tumbledew is our first title.</p>
  </div>
</section>
</main>
""" + FOOT

(HERE / "index.html").write_text(INDEX)
build_doc("support.html", "2", "Tumbledew Support · Samara Titles", "s")
build_doc("privacy.html", "3", "Privacy Policy · Samara Titles", "p", short_version_box=True)
NOT_FOUND = head("Page not found · Samara Titles", "", "Page not found.") + """
<main class="doc"><div class="wrap"><h1>Page not found</h1>
<p>That page doesn't exist. Try the <a href="/">home page</a>, <a href="/support">Tumbledew support</a> or the <a href="/privacy">privacy policy</a>.</p></div></main>
""" + FOOT
(HERE / "404.html").write_text(NOT_FOUND)
(HERE / "CNAME").write_text("samaratitles.com\n")
(HERE / ".nojekyll").write_text("")
print("built docs/: index, support, privacy, 404")
