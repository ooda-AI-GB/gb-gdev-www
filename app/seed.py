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
            "tagline": "Your window into your entire platform",
            "description": "Monitor every app in your stack from one dashboard. Track status, evolution history, deployment health, and performance — all in one place. Available exclusively on the annual plan.",
            "category": "operations",
            "live_url": None,
            "features": json.dumps(["Unified app status dashboard", "Evolution history tracking", "Deployment health monitoring", "Performance metrics", "Auto-refresh dashboards", "Annual plan exclusive"]),
            "replaces": None,
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
            "name": "Luis",
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
            "name": "Eric",
            "role": "AI/RAG Specialist",
            "bio": "Retrieval-augmented generation and knowledge systems. Making AI that knows what it needs to know.",
            "sort_order": 3,
        },
        {
            "name": "Victor",
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
            "content": """We ran a full cost audit across our cloud infrastructure. What we found was ugly.

## The Damage

A single background service had been crash-looping for two weeks on a misconfigured database password. Cost: **$63 in 14 days**. Nobody noticed because it was in a separate project with no alerts.

Three orphaned projects from a previous client engagement were still running compute. Another $30/month in pure waste.

A workflow automation VM we set up for testing but never used in production: $4/month doing absolutely nothing.

## The Fix

Two hours of focused cleanup:

- Killed the crash-looping service
- Deleted the 3 orphaned projects
- Deleted the unused VM
- Optimized AI model selection (same quality, 80% cheaper)
- Identified database instances to consolidate

**Result:** $69/month saved on AI services alone. Total projected savings: ~$120/month.

## The Lesson

If you're not auditing your cloud spend monthly, you're burning money. Period. The waste accumulates silently. No one gets an alert for "this thing costs $4/month and does nothing."

We built Cloud Pro specifically to catch this. It monitors your infrastructure, flags waste, and tracks every dollar. Because the first step to optimization is visibility.""",
            "author": "Luis Manalac",
            "category": "case_study",
            "tags": json.dumps(["finops", "cloud", "cost-optimization", "operations"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 10, 0, 0),
            "read_time_minutes": 4,
        },
        {
            "slug": "why-12-apps-one-platform",
            "title": "Why We Built 12 Apps Instead of One",
            "subtitle": "The case for specialized tools that share everything",
            "content": """Most platforms try to cram everything into one monolithic app. We went the other direction.

## The Monolith Problem

Every all-in-one tool you've used has the same issue: it's mediocre at everything and great at nothing. The CRM module in your project management tool is always worse than a dedicated CRM. The analytics in your help desk never match a real BI tool.

And when one module breaks or needs maintenance, the whole platform goes down.

## Our Approach

Gigabox is 12 independent apps that share data natively:

- **CRM Pro** handles contacts and pipeline
- **Help Desk Pro** handles tickets and knowledge base
- **Analytics Pro** handles dashboards and insights
- **Finance Pro** tracks expenses and generates tax reports
- **Productivity Pro** manages tasks and projects
- **Legal Pro** tracks contracts and compliance

Each app is purpose-built for its domain. Each has its own database. Each can be updated independently without affecting the others.

But they all talk to each other. Create a contact in CRM and it's available in Help Desk. Close a deal and Analytics updates the revenue dashboard automatically. Onboard a client and the AI assistant sets up their profile across every app in seconds.

## The Result

You get enterprise-grade functionality in each domain, with the integration benefits of a single platform. No copy-paste between tools. No CSV imports. No "check the other app for that data."

Twelve specialized tools. One login. One invoice. One AI assistant that ties it all together.""",
            "author": "Luis Manalac",
            "category": "philosophy",
            "tags": json.dumps(["architecture", "platform", "integration", "product"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 12, 0, 0),
            "read_time_minutes": 3,
        },
        {
            "slug": "per-seat-pricing-is-a-tax-on-growth",
            "title": "Per-Seat Pricing Is a Tax on Growth",
            "subtitle": "Why we charge a flat rate for unlimited users",
            "content": """Every SaaS company you use charges per seat. It's the industry standard. It's also a terrible deal for growing businesses.

## The Math

A 25-person company using the standard enterprise stack:

- **CRM:** $150/seat x 10 sales reps = $1,500/mo
- **Help Desk:** $115/seat x 5 agents = $575/mo
- **Analytics:** $75/seat x 5 viewers = $375/mo
- **Project Management:** $25/seat x 25 users = $625/mo
- **Contract Management:** $60/seat x 5 legal = $300/mo

That's **$3,375/mo** — and it goes up every time you hire someone. Add 10 more people and your software cost jumps $1,000+/month without any new functionality.

## The Perverse Incentive

Per-seat pricing punishes you for growing. It creates a world where managers ask "do they really need access?" instead of "how do we get everyone the tools they need?"

It means your intern can't look up a customer record because you didn't buy them a CRM seat. Your CEO can't check the support queue because Zendesk charges extra for "light agents."

## Our Model

Gigabox costs $2,000/month. For everyone. All 12 apps. Unlimited users.

Hire 10 people tomorrow? Same price. Open a new office with 50 employees? Same price. Give your board members read-only access to every dashboard? Same price.

Your software costs should be predictable, not a variable that scales against you. We charge for the platform, not the people.""",
            "author": "Luis Manalac",
            "category": "business",
            "tags": json.dumps(["pricing", "saas", "business-model", "growth"]),
            "published": True,
            "published_at": datetime(2026, 2, 20, 14, 0, 0),
            "read_time_minutes": 4,
        },
    ]
    for data in posts:
        db.add(BlogPost(**data))
