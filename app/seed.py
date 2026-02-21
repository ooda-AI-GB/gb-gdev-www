import json
from datetime import datetime
from app.database import SessionLocal
from app.models import App, TeamMember, BlogPost


def seed_if_empty():
    db = SessionLocal()
    try:
        if db.query(App).count() > 0:
            return
        _seed_apps(db)
        _seed_team(db)
        _seed_blog(db)
        db.commit()
    finally:
        db.close()


def _seed_apps(db):
    apps = [
        {
            "slug": "crm-pro",
            "name": "CRM Pro",
            "tagline": "Your entire sales pipeline, AI-powered",
            "description": "Full-featured CRM with contact management, deal pipeline, activity tracking, and AI-powered competitive intelligence. Built to replace HubSpot and Salesforce at a fraction of the cost.",
            "category": "productivity",
            "live_url": "https://gdev-crm.gigabox.app",
            "features": json.dumps(["Contact management with pipeline stages", "Deal tracking and forecasting", "Activity logging and notes", "AI-powered competitive intelligence", "Full REST API", "Custom dashboards"]),
            "replaces": "HubSpot, Salesforce",
            "evolution_count": 16,
            "status": "live",
            "sort_order": 1,
        },
        {
            "slug": "help-desk",
            "name": "Help Desk Pro",
            "tagline": "Support tickets, solved by AI",
            "description": "Ticketing system with knowledge base, SLA tracking, auto-categorization, and customer self-service portal. Replaces Intercom and Zendesk.",
            "category": "productivity",
            "live_url": "https://gdev-help.gigabox.app",
            "features": json.dumps(["Ticket management with priorities", "Knowledge base with search", "SLA tracking and alerts", "Auto-categorization", "Customer portal", "Full REST API"]),
            "replaces": "Intercom, Zendesk",
            "evolution_count": 13,
            "status": "live",
            "sort_order": 2,
        },
        {
            "slug": "analytics-pro",
            "name": "Analytics Pro",
            "tagline": "Business intelligence without the price tag",
            "description": "Dashboards, data sources, AI-powered queries, and trend analysis. Connect your data, ask questions in plain English, get insights.",
            "category": "analytics",
            "live_url": "https://gdev-analytics.gigabox.app",
            "features": json.dumps(["Custom dashboards and widgets", "Multiple data source connectors", "AI-powered natural language queries", "Trend analysis and forecasting", "Automated report generation", "Full REST API"]),
            "replaces": "Tableau, Looker",
            "evolution_count": 14,
            "status": "live",
            "sort_order": 3,
        },
        {
            "slug": "social-pro",
            "name": "Social Pro",
            "tagline": "Multi-platform social, one dashboard",
            "description": "Social media management with post scheduling, content calendar, inbox monitoring, engagement analytics, and AI content generation.",
            "category": "marketing",
            "live_url": "https://gdev-social.gigabox.app",
            "features": json.dumps(["Multi-platform post scheduling", "Content calendar with drag-and-drop", "Unified inbox monitoring", "Engagement analytics", "AI content generation", "Full REST API"]),
            "replaces": "Hootsuite, Buffer",
            "evolution_count": 14,
            "status": "live",
            "sort_order": 4,
        },
        {
            "slug": "cloud-pro",
            "name": "Cloud Pro",
            "tagline": "See every dollar your cloud spends",
            "description": "Infrastructure cost tracking, resource monitoring, waste detection, and optimization recommendations. Know exactly where your cloud budget goes.",
            "category": "devops",
            "live_url": "https://gdev-cloud.gigabox.app",
            "features": json.dumps(["Multi-cloud cost tracking", "Resource inventory and tagging", "Waste detection alerts", "Budget threshold monitoring", "AI optimization recommendations", "Full REST API"]),
            "replaces": "CloudHealth, Vantage",
            "evolution_count": 14,
            "status": "live",
            "sort_order": 5,
        },
        {
            "slug": "jobs-pro",
            "name": "Jobs Pro",
            "tagline": "Hire faster with AI-powered ATS",
            "description": "Job board with listings, applications, applicant tracking, and AI-powered candidate scoring. From posting to hire, one platform.",
            "category": "productivity",
            "live_url": "https://gdev-jobs.gigabox.app",
            "features": json.dumps(["Job posting and management", "Application tracking pipeline", "AI candidate scoring", "Interview scheduling", "Company profiles", "Full REST API"]),
            "replaces": "Lever, Greenhouse",
            "evolution_count": 14,
            "status": "live",
            "sort_order": 6,
        },
        {
            "slug": "watchtower",
            "name": "Watchtower",
            "tagline": "The operations control room",
            "description": "Internal monitoring dashboard tracking all projects, evolutions, builds, fleet status, and infrastructure health. The nerve center of the platform.",
            "category": "operations",
            "live_url": "https://gdev-watchtower.gigabox.app",
            "features": json.dumps(["Project and evolution tracking", "Build status monitoring", "VM fleet control", "Health history and alerts", "Task log viewer", "Auto-refresh dashboards"]),
            "replaces": "Internal tool",
            "evolution_count": 12,
            "status": "live",
            "sort_order": 7,
        },
    ]
    for data in apps:
        db.add(App(**data))


def _seed_team(db):
    members = [
        {
            "name": "Luis Manalac",
            "role": "CEO & Principal AI Engineer",
            "bio": "UC Berkeley Applied Math. First-wave Wall Street quant. Founded startup acquired for $135M. President/CEO Lady Luck Digital (The Last of Us, Uncharted). Built Gigabox: an AI-orchestrated software platform that ships enterprise applications in days.",
            "credentials": "UC Berkeley Applied Math '84",
            "sort_order": 1,
        },
        {
            "name": "Akshay",
            "role": "AI Engineer",
            "bio": "Stanford CS PhD. Building the intelligence layer that powers the Gigabox platform.",
            "credentials": "Stanford CS PhD",
            "sort_order": 2,
        },
        {
            "name": "Eric Manalac",
            "role": "AI/RAG Specialist",
            "bio": "Retrieval-augmented generation and knowledge systems. Making AI that knows what it needs to know.",
            "sort_order": 3,
        },
        {
            "name": "Victor Manalac",
            "role": "Business Analytics",
            "bio": "Turning data into decisions. Analytics architecture and business intelligence.",
            "sort_order": 4,
        },
        {
            "name": "Hannah",
            "role": "Operations",
            "bio": "Infrastructure, logistics, and making sure everything runs. The operational backbone of Gigabox.",
            "sort_order": 5,
        },
        {
            "name": "Nikki",
            "role": "Sales & Marketing",
            "bio": "Client acquisition and market strategy. Connecting the right businesses with the right solutions.",
            "sort_order": 6,
        },
    ]
    for data in members:
        db.add(TeamMember(**data))


def _seed_blog(db):
    posts = [
        {
            "slug": "cloud-waste-audit",
            "title": "We Found $714/Month in Cloud Waste in Two Hours",
            "subtitle": "A FinOps case study from our own infrastructure",
            "content": """We ran a full cost audit across two GCP accounts today. What we found was ugly.

## The Damage

A single Cloud Run service — `slack-coworker` — had been crash-looping for two weeks on a bad Postgres password. Cost: **$63 in 14 days**. Nobody noticed because it was in a separate project with no alerts.

Three orphaned projects from a previous client engagement were still running compute. Another $30/month in pure waste.

An n8n workflow VM we set up for testing but never used in production: $4/month doing absolutely nothing.

## The Fix

Two hours of focused cleanup:

- Killed the crash-looping Cloud Run service
- Deleted the 3 orphaned projects
- Deleted the n8n VM
- Migrated all Gemini calls from Pro to Flash (same quality, 80% cheaper)
- Identified Cloud SQL instances to consolidate

**Result:** $69/month saved on Vertex AI alone. Total projected savings: ~$120/month.

## The Lesson

If you're not auditing your cloud spend monthly, you're burning money. Period. The waste accumulates silently. No one gets an alert for "this thing costs $4/month and does nothing."

We built Cloud Pro specifically to catch this. It monitors your infrastructure, flags waste, and tracks every dollar. Because the first step to optimization is visibility.""",
            "author": "Luis Manalac",
            "category": "case_study",
            "tags": json.dumps(["finops", "gcp", "cloud", "cost-optimization"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 10, 0, 0),
            "read_time_minutes": 4,
        },
        {
            "slug": "every-layer-is-waste",
            "title": "Every Layer Is Waste",
            "subtitle": "Why we keep simplifying our architecture",
            "content": """Our build pipeline started at 8 steps. Today it's 5. Next month it might be 3.

## The Original Pipeline

1. User describes app in Slack
2. Gemini AI rewrites the prompt (architect layer)
3. Sanitizer validates dependencies
4. Verifier checks the output
5. OpenCode CLI generates code
6. Watchdog monitors for timeouts
7. Push to GitHub
8. Deploy to Coolify

Every layer was added for a reason. The architect catches bad prompts. The sanitizer fixes dependency conflicts. The verifier ensures the output is deployable.

But every layer is also a failure point. And every layer adds latency.

## The Realization

When we swapped Gemini for Claude on the code generation step, something interesting happened: Claude didn't need the architect. It didn't corrupt URLs. It didn't hallucinate package names. It followed the CLAUDE.md rules file and just... built the app correctly.

So we removed the architect. And the sanitizer. And the verifier. And the watchdog.

**8 steps became 5:**

1. User describes app
2. Clone golden template
3. Claude transforms it
4. Push to GitHub
5. Deploy

Same result. Fewer moving parts. Faster builds. Fewer bugs.

## The Principle

Every abstraction layer you add is technical debt you're pre-paying. If the underlying system improves enough, those layers become pure overhead.

Review your stack regularly. Ask: "If I removed this layer, what would break?" If the answer is "nothing, because the thing it was protecting against no longer happens" — delete it.""",
            "author": "Luis Manalac",
            "category": "philosophy",
            "tags": json.dumps(["architecture", "simplicity", "engineering"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 12, 0, 0),
            "read_time_minutes": 3,
        },
        {
            "slug": "8-steps-to-5",
            "title": "From 8 Steps to 5: How We Replaced Our Build Pipeline",
            "subtitle": "The Uno to CC Worker migration story",
            "content": """Last week our build pipeline had 8 moving parts across 4 services. Today it has 5 steps and one service. Here's how we got there.

## The Old Way

Our original pipeline used **Uno** (a Slack bot) to receive build requests, **Viva** (a Kubernetes worker) to execute code generation with OpenCode CLI, and **Gemini** to architect the prompts. It worked. Apps got built. But the chain was fragile.

The Gemini architect would sometimes corrupt `git` URLs into `gitpython`. The sanitizer would sometimes strip valid dependencies. The verifier would flag false positives. Each layer added ~30 seconds and a 5% failure rate.

Multiply that across 8 steps and your end-to-end success rate drops to ~66%.

## The New Way

We built **CC Worker** — a lightweight agent that runs on a VM, picks up tasks from a queue, and executes them with Claude.

The entire pipeline:

1. **API call** creates a task with an instruction
2. **CC Worker** picks it up, clones the golden template
3. **Claude** reads the CLAUDE.md rules and transforms the app
4. **Git push** to GitHub
5. **Coolify** auto-deploys

No architect. No sanitizer. No verifier. No watchdog. Claude follows the rules file and gets it right the first time.

## The Results

We ran three experiments:

- **Fresh scaffold:** 2 minutes 45 seconds. Zero bugs. All rules followed.
- **Fork-transform:** 13 files modified. Auth and billing preserved perfectly.
- **Full pipeline (API to live URL):** 15 files. Deployed to production. Working.

The success rate went from ~66% to effectively 100% across our test runs.

## Why It Worked

The key insight: a good rules file (CLAUDE.md) replaces multiple validation layers. Instead of building systems to catch and fix AI mistakes, we wrote clear instructions that prevent the mistakes in the first place.

Less code. Fewer services. Better results.""",
            "author": "Luis Manalac",
            "category": "engineering",
            "tags": json.dumps(["pipeline", "claude", "cc-worker", "architecture"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 14, 0, 0),
            "read_time_minutes": 5,
        },
    ]
    for data in posts:
        db.add(BlogPost(**data))
