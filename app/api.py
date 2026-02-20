from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import json

from app.database import get_db
from app.auth import require_api_key
from app.models import App, TeamMember, BlogPost, ContactSubmission, SiteAnalytics

router = APIRouter(prefix="/api/v1")


# --- Pydantic Schemas ---

class AppCreate(BaseModel):
    slug: str
    name: str
    tagline: str
    description: str
    category: str
    live_url: Optional[str] = None
    screenshot_url: Optional[str] = None
    features: Optional[str] = None
    replaces: Optional[str] = None
    evolution_count: int = 0
    status: str = "live"
    sort_order: int = 0

class AppUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    live_url: Optional[str] = None
    screenshot_url: Optional[str] = None
    features: Optional[str] = None
    replaces: Optional[str] = None
    evolution_count: Optional[int] = None
    status: Optional[str] = None
    sort_order: Optional[int] = None

class TeamCreate(BaseModel):
    name: str
    role: str
    bio: Optional[str] = None
    credentials: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    sort_order: int = 0
    active: bool = True

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    bio: Optional[str] = None
    credentials: Optional[str] = None
    avatar_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    sort_order: Optional[int] = None
    active: Optional[bool] = None

class BlogCreate(BaseModel):
    slug: str
    title: str
    subtitle: Optional[str] = None
    content: str
    author: str
    category: str
    tags: Optional[str] = None
    read_time_minutes: int = 5

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    published: Optional[bool] = None
    read_time_minutes: Optional[int] = None

class ContactStatusUpdate(BaseModel):
    status: str

class AnalyticsEvent(BaseModel):
    page: str
    referrer: Optional[str] = None
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None
    visitor_id: Optional[str] = None


# --- Helpers ---

def row_to_dict(row):
    d = {}
    for c in row.__table__.columns:
        val = getattr(row, c.name)
        if isinstance(val, datetime):
            val = val.isoformat()
        d[c.name] = val
    return d


# --- Apps ---

@router.get("/apps")
def list_apps(category: Optional[str] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(App).order_by(App.sort_order)
    if category:
        q = q.filter(App.category == category)
    if status:
        q = q.filter(App.status == status)
    return [row_to_dict(a) for a in q.all()]

@router.get("/apps/{slug}")
def get_app(slug: str, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.slug == slug).first()
    if not app:
        raise HTTPException(404, "App not found")
    return row_to_dict(app)

@router.post("/apps", dependencies=[Depends(require_api_key)])
def create_app(data: AppCreate, db: Session = Depends(get_db)):
    if db.query(App).filter(App.slug == data.slug).first():
        raise HTTPException(409, "App with this slug already exists")
    app = App(**data.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    return row_to_dict(app)

@router.put("/apps/{slug}", dependencies=[Depends(require_api_key)])
def update_app(slug: str, data: AppUpdate, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.slug == slug).first()
    if not app:
        raise HTTPException(404, "App not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(app, k, v)
    db.commit()
    db.refresh(app)
    return row_to_dict(app)

@router.delete("/apps/{slug}", dependencies=[Depends(require_api_key)])
def delete_app(slug: str, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.slug == slug).first()
    if not app:
        raise HTTPException(404, "App not found")
    db.delete(app)
    db.commit()
    return {"deleted": True}


# --- Team ---

@router.get("/team")
def list_team(db: Session = Depends(get_db)):
    members = db.query(TeamMember).filter(TeamMember.active == True).order_by(TeamMember.sort_order).all()
    return [row_to_dict(m) for m in members]

@router.post("/team", dependencies=[Depends(require_api_key)])
def create_member(data: TeamCreate, db: Session = Depends(get_db)):
    member = TeamMember(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return row_to_dict(member)

@router.put("/team/{id}", dependencies=[Depends(require_api_key)])
def update_member(id: int, data: TeamUpdate, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == id).first()
    if not member:
        raise HTTPException(404, "Team member not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(member, k, v)
    db.commit()
    db.refresh(member)
    return row_to_dict(member)

@router.delete("/team/{id}", dependencies=[Depends(require_api_key)])
def delete_member(id: int, db: Session = Depends(get_db)):
    member = db.query(TeamMember).filter(TeamMember.id == id).first()
    if not member:
        raise HTTPException(404, "Team member not found")
    db.delete(member)
    db.commit()
    return {"deleted": True}


# --- Blog ---

@router.get("/blog")
def list_posts(
    all: bool = Query(False, description="Include drafts (requires API key)"),
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(BlogPost).order_by(BlogPost.created_at.desc())
    if not all:
        q = q.filter(BlogPost.published == True)
    if category:
        q = q.filter(BlogPost.category == category)
    return [row_to_dict(p) for p in q.all()]

@router.get("/blog/{slug}")
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return row_to_dict(post)

@router.post("/blog", dependencies=[Depends(require_api_key)])
def create_post(data: BlogCreate, db: Session = Depends(get_db)):
    if db.query(BlogPost).filter(BlogPost.slug == data.slug).first():
        raise HTTPException(409, "Post with this slug already exists")
    post = BlogPost(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return row_to_dict(post)

@router.put("/blog/{slug}", dependencies=[Depends(require_api_key)])
def update_post(slug: str, data: BlogUpdate, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(404, "Post not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(post, k, v)
    db.commit()
    db.refresh(post)
    return row_to_dict(post)

@router.post("/blog/{slug}/publish", dependencies=[Depends(require_api_key)])
def publish_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(404, "Post not found")
    post.published = True
    post.published_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return row_to_dict(post)

@router.delete("/blog/{slug}", dependencies=[Depends(require_api_key)])
def delete_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db.delete(post)
    db.commit()
    return {"deleted": True}


# --- Contacts ---

@router.get("/contacts", dependencies=[Depends(require_api_key)])
def list_contacts(status: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(ContactSubmission).order_by(ContactSubmission.created_at.desc())
    if status:
        q = q.filter(ContactSubmission.status == status)
    return [row_to_dict(c) for c in q.all()]

@router.put("/contacts/{id}/status", dependencies=[Depends(require_api_key)])
def update_contact_status(id: int, data: ContactStatusUpdate, db: Session = Depends(get_db)):
    contact = db.query(ContactSubmission).filter(ContactSubmission.id == id).first()
    if not contact:
        raise HTTPException(404, "Contact not found")
    contact.status = data.status
    db.commit()
    db.refresh(contact)
    return row_to_dict(contact)


# --- Analytics ---

@router.post("/analytics")
def track_event(data: AnalyticsEvent, db: Session = Depends(get_db)):
    event = SiteAnalytics(**data.model_dump())
    db.add(event)
    db.commit()
    return {"tracked": True}

@router.get("/analytics", dependencies=[Depends(require_api_key)])
def get_analytics(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    events = db.query(SiteAnalytics).filter(
        SiteAnalytics.created_at >= since
    ).order_by(SiteAnalytics.created_at.desc()).all()
    return [row_to_dict(e) for e in events]

@router.get("/analytics/summary", dependencies=[Depends(require_api_key)])
def analytics_summary(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=days)
    base = db.query(SiteAnalytics).filter(SiteAnalytics.created_at >= since)
    total_views = base.count()
    unique_visitors = base.with_entities(
        sqlfunc.count(sqlfunc.distinct(SiteAnalytics.visitor_id))
    ).scalar() or 0
    top_pages = (
        base.with_entities(SiteAnalytics.page, sqlfunc.count(SiteAnalytics.id).label("views"))
        .group_by(SiteAnalytics.page)
        .order_by(sqlfunc.count(SiteAnalytics.id).desc())
        .limit(10).all()
    )
    top_sources = (
        base.filter(SiteAnalytics.utm_source.isnot(None))
        .with_entities(SiteAnalytics.utm_source, sqlfunc.count(SiteAnalytics.id).label("count"))
        .group_by(SiteAnalytics.utm_source)
        .order_by(sqlfunc.count(SiteAnalytics.id).desc())
        .limit(10).all()
    )
    return {
        "period_days": days,
        "total_views": total_views,
        "unique_visitors": unique_visitors,
        "top_pages": [{"page": p, "views": v} for p, v in top_pages],
        "top_sources": [{"source": s, "count": c} for s, c in top_sources],
    }
