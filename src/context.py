"""
NoZak Labs — Project Context for the Radar Agent.

This module defines what the agent cares about. The scoring rubric in
scorer.py reads from here to decide what's relevant noise vs. signal.

Update this file as priorities shift. The agent reflects whatever
is written here on the next scheduled run — no other code changes needed.
"""

# ─── COMPANY CONTEXT ─────────────────────────────────────────────────────────

COMPANY_CONTEXT = """
NoZak Labs is a one-person consulting/build studio operated by Noha Zak,
a Solutions Engineer candidate transitioning from Content Operations + Pega
consulting into formal software engineering.

The company delivers technical work for three client projects and parallel
career positioning for a Solutions Engineer role.
""".strip()

# ─── ACTIVE PROJECTS ─────────────────────────────────────────────────────────

PROJECTS = {
    "Brands of Eden": {
        "tier": 1,
        "stage": "Live, pre-breakeven",
        "summary": (
            "Family e-commerce business on Facebook/Instagram. Sourcing products "
            "for best margin. First order shipped. Possibly launching sister's "
            "skin brand as a second line. NoZak Labs owns the tech stack."
        ),
        "tech_stack": [
            "Chatbot automation (Zizi)",
            "Order/inventory automation",
            "Google Sheets backend",
            "Analytics dashboards",
            "Marketing automation",
        ],
        "looking_for": [
            "E-commerce automation tools (free or low-cost tier)",
            "Chatbot frameworks and conversational AI improvements",
            "Inventory and order management systems",
            "Shopify/WooCommerce alternatives with free tier",
            "Social commerce tools (Facebook/Instagram integration)",
            "Analytics, attribution, and reporting tools",
            "Skincare e-commerce specific tooling (for sister's brand)",
        ],
    },
    "lurniALP": {
        "tier": 1,
        "stage": "Planning",
        "summary": (
            "Brother's project. Adaptive AI learning platform for school "
            "students preparing for the Checkpoint English exam. Noha is "
            "the technical advisor for architecture and AI integration."
        ),
        "tech_stack": [
            "AI/ML for adaptive learning",
            "Curriculum modeling",
            "Quiz/assessment engines",
            "Student progress tracking",
        ],
        "looking_for": [
            "Adaptive learning algorithms and frameworks",
            "Open-source LMS or quiz platforms",
            "AI tutoring frameworks (Khanmigo-style)",
            "Educational content APIs and curriculum datasets",
            "Lightweight ML for student modeling (knowledge tracing, IRT)",
            "EdTech case studies and architecture patterns",
        ],
    },
    "Hykers": {
        "tier": 1,
        "stage": "Planning / validation",
        "summary": (
            "Egypt-focused application similar to Hitch (rideshare/hitchhiking). "
            "Still in planning phase — validation, not yet build."
        ),
        "tech_stack": [
            "Mobile-first architecture (TBD)",
            "Geolocation and matching",
            "Payment integration (Egypt-specific)",
        ],
        "looking_for": [
            "Rideshare/marketplace technical case studies",
            "Geospatial matching algorithms and APIs",
            "Egypt/MENA fintech and payment rails",
            "Mobile development frameworks (React Native, Flutter)",
            "Validation methodologies for two-sided marketplaces",
            "Open-source rideshare reference implementations",
        ],
    },
    "SE Job Hunt": {
        "tier": 1,
        "stage": "Active",
        "summary": (
            "Transitioning to a Solutions Engineer role. Active Advansys "
            "Senior Pega Developer / Solution Architect opportunity. Strong "
            "Pega depth (banking, government), lighter in advanced decisioning "
            "and robotics. Pega SA exam in progress."
        ),
        "looking_for": [
            "Solutions Engineer interview prep and case studies",
            "Pega platform updates, especially Pega 8.x and Constellation",
            "Pega Decisioning and robotics resources (her growth areas)",
            "SE-relevant skills: API design, integration patterns, demos",
            "Playwright / TypeScript automation QA content",
            "Sales engineering content (technical demos, POCs, discovery)",
            "AI agents and automation (her current technical depth area)",
        ],
    },
}

# ─── CROSS-CUTTING INTERESTS ─────────────────────────────────────────────────

CROSS_CUTTING = {
    "tier": 2,
    "summary": "Skills and themes that benefit multiple projects.",
    "looking_for": [
        "AI agents, agentic workflows, multi-agent systems",
        "Workflow automation (n8n, Zapier alternatives, custom Python)",
        "LLM application patterns (RAG, function calling, evals)",
        "Free-tier and open-source SaaS tooling",
        "Python and TypeScript ecosystem updates",
        "GitHub Actions and CI/CD for solo developers",
        "Solo founder / indie hacker case studies",
    ],
}

# ─── EXPLICIT NOISE FILTERS ──────────────────────────────────────────────────
# Topics that are explicitly NOT relevant — agent should score these low
# even if they're trending in AI/tech spaces.

NOISE_FILTERS = [
    "Crypto, NFTs, Web3, blockchain speculation",
    "AI doomerism and AI safety philosophical debates",
    "Foundation model architecture papers (unless directly applicable)",
    "Enterprise-only tools with no free or starter tier",
    "Generic productivity apps with no automation angle",
    "Hardware reviews unrelated to dev workflow",
    "Personal opinion pieces and Twitter/X drama",
    "AI-generated art tools (unless for e-commerce product imagery)",
    "Job postings (unless explicitly Solutions Engineer roles in Egypt/remote)",
]

# ─── SCORING TIER DEFINITIONS ────────────────────────────────────────────────
# These thresholds are used by scorer.py to assign tier labels.

TIER_THRESHOLDS = {
    "act_now": 75,    # Score ≥ 75 → 🔥 Act Now (review during 30-min slot)
    "watch":    50,   # Score 50-74 → 👀 Watch (skim if time)
    "archive":   0,   # Score < 50 → 📦 Archive (don't surface)
}

# Items below this minimum score are dropped entirely (not even archived)
MIN_SCORE_TO_KEEP = 25
