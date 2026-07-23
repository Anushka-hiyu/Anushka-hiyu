import os
import json
import urllib.request
import urllib.error
from collections import Counter

USERNAME = os.environ.get("GITHUB_USERNAME", "Anushka-hiyu")
TOKEN = os.environ.get("GITHUB_TOKEN")

API = "https://api.github.com"


# --------------------------------------------------
# GITHUB API
# --------------------------------------------------

def github_get(endpoint):
    request = urllib.request.Request(
        API + endpoint,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Anushka-Profile-Stats",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())

    except urllib.error.HTTPError as error:
        print(f"GitHub API error: {error.code}")
        print(error.read().decode())
        raise


# --------------------------------------------------
# GET PROFILE + REPOSITORIES
# --------------------------------------------------

profile = github_get(f"/users/{USERNAME}")

repos = github_get(
    f"/users/{USERNAME}/repos?per_page=100&sort=updated"
)

# Don't count forks as projects
repos = [
    repo for repo in repos
    if not repo.get("fork", False)
]


# --------------------------------------------------
# BASIC STATS
# --------------------------------------------------

public_repos = profile.get("public_repos", 0)

followers = profile.get("followers", 0)

total_stars = sum(
    repo.get("stargazers_count", 0)
    for repo in repos
)

total_forks = sum(
    repo.get("forks_count", 0)
    for repo in repos
)


# --------------------------------------------------
# LANGUAGES
# --------------------------------------------------

languages = Counter()

for repo in repos:

    if repo.get("language"):
        languages[repo["language"]] += 1


top_languages = languages.most_common(4)


# --------------------------------------------------
# SVG HELPERS
# --------------------------------------------------

def escape(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


language_text = " // ".join(
    escape(language.upper())
    for language, _ in top_languages
)

if not language_text:
    language_text = "DATA UNAVAILABLE"


# --------------------------------------------------
# CREATE SVG
# --------------------------------------------------

svg = f"""
<svg
    width="1200"
    height="310"
    viewBox="0 0 1200 310"
    xmlns="http://www.w3.org/2000/svg"
>

<defs>

    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#0D0712"/>
        <stop offset="55%" stop-color="#08040D"/>
        <stop offset="100%" stop-color="#050308"/>
    </linearGradient>

    <filter id="glow"
        x="-30%"
        y="-30%"
        width="160%"
        height="160%"
    >
        <feGaussianBlur
            stdDeviation="2.5"
            result="blur"
        />

        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

</defs>


<!-- BACKGROUND -->

<rect
    x="2"
    y="2"
    width="1196"
    height="306"
    rx="14"
    fill="url(#bg)"
    stroke="#A855F7"
    stroke-width="2"
/>

<rect
    x="12"
    y="12"
    width="1176"
    height="286"
    rx="10"
    fill="none"
    stroke="#5F3475"
    opacity="0.45"
/>


<!-- TERMINAL DOTS -->

<circle cx="32" cy="30" r="4" fill="#A855F7"/>

<circle
    cx="48"
    cy="30"
    r="4"
    fill="#D8B4FE"
/>

<circle
    cx="64"
    cy="30"
    r="4"
    fill="#76558C"
/>


<!-- HEADER -->

<text
    x="600"
    y="34"
    text-anchor="middle"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
    font-weight="bold"
    letter-spacing="3"
>
    PLAYER // LIVE DATA
</text>


<circle
    cx="1120"
    cy="30"
    r="3"
    fill="#A855F7"
    filter="url(#glow)"
/>

<text
    x="1132"
    y="34"
    fill="#76558C"
    font-family="monospace"
    font-size="9"
>
    LIVE
</text>


<!-- TITLE -->

<text
    x="55"
    y="90"
    fill="#F3E8FF"
    font-family="monospace"
    font-size="24"
    font-weight="bold"
>
    GITHUB RECORD
</text>

<text
    x="55"
    y="115"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
    letter-spacing="2"
>
    @{escape(USERNAME)}
</text>


<!-- STAT CARDS -->

<rect
    x="55"
    y="145"
    width="245"
    height="75"
    rx="7"
    fill="#12091A"
    stroke="#3D2050"
/>

<text
    x="75"
    y="172"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
>
    REPOSITORIES
</text>

<text
    x="75"
    y="204"
    fill="#D8B4FE"
    font-family="monospace"
    font-size="23"
    font-weight="bold"
>
    {public_repos}
</text>


<rect
    x="320"
    y="145"
    width="245"
    height="75"
    rx="7"
    fill="#12091A"
    stroke="#3D2050"
/>

<text
    x="340"
    y="172"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
>
    STARS
</text>

<text
    x="340"
    y="204"
    fill="#D8B4FE"
    font-family="monospace"
    font-size="23"
    font-weight="bold"
>
    {total_stars}
</text>


<rect
    x="585"
    y="145"
    width="245"
    height="75"
    rx="7"
    fill="#12091A"
    stroke="#3D2050"
/>

<text
    x="605"
    y="172"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
>
    FOLLOWERS
</text>

<text
    x="605"
    y="204"
    fill="#D8B4FE"
    font-family="monospace"
    font-size="23"
    font-weight="bold"
>
    {followers}
</text>


<rect
    x="850"
    y="145"
    width="295"
    height="75"
    rx="7"
    fill="#12091A"
    stroke="#3D2050"
/>

<text
    x="870"
    y="172"
    fill="#76558C"
    font-family="monospace"
    font-size="10"
>
    FORKS
</text>

<text
    x="870"
    y="204"
    fill="#D8B4FE"
    font-family="monospace"
    font-size="23"
    font-weight="bold"
>
    {total_forks}
</text>


<!-- LANGUAGES -->

<circle
    cx="58"
    cy="260"
    r="3"
    fill="#A855F7"
    filter="url(#glow)"
/>

<text
    x="72"
    y="264"
    fill="#76558C"
    font-family="monospace"
    font-size="9"
    letter-spacing="1"
>
    TOP LANGUAGES
</text>

<text
    x="205"
    y="264"
    fill="#D8B4FE"
    font-family="monospace"
    font-size="10"
    font-weight="bold"
    letter-spacing="1"
>
    {language_text}
</text>


<!-- BOTTOM STATUS -->

<text
    x="1145"
    y="275"
    text-anchor="end"
    fill="#5F3475"
    font-family="monospace"
    font-size="9"
>
    DATA://SYNCED
</text>

</svg>
"""


# --------------------------------------------------
# SAVE
# --------------------------------------------------

os.makedirs("assets", exist_ok=True)

with open(
    "assets/player-data.svg",
    "w",
    encoding="utf-8"
) as file:
    file.write(svg)


print("PLAYER DATA GENERATED SUCCESSFULLY")
print(f"Repositories: {public_repos}")
print(f"Stars: {total_stars}")
print(f"Followers: {followers}")
print(f"Forks: {total_forks}")
print(f"Languages: {language_text}")
