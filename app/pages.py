from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import json
import re
import markdown

from app.database import get_db
from app.models import App, TeamMember, BlogPost, ContactSubmission


def strip_markdown(text, length=120):
    """Strip markdown headers/formatting and return plain text preview."""
    lines = text.split('\n')
    plain = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('```') or line.startswith('---'):
            continue
        line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
        line = re.sub(r'`(.+?)`', r'\1', line)
        line = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)
        line = line.lstrip('- ').lstrip('* ')
        if line:
            plain.append(line)
    result = ' '.join(plain)
    if len(result) > length:
        result = result[:length].rsplit(' ', 1)[0] + '...'
    return result

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def parse_features(f):
    if not f:
        return []
    try:
        return json.loads(f)
    except (json.JSONDecodeError, TypeError):
        return []


def parse_tags(t):
    if not t:
        return []
    try:
        return json.loads(t)
    except (json.JSONDecodeError, TypeError):
        return []


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    apps = db.query(App).filter(App.status == "live").order_by(App.sort_order).all()
    posts = db.query(BlogPost).filter(BlogPost.published == True).order_by(
        BlogPost.published_at.desc()
    ).limit(3).all()
    app_count = db.query(App).filter(App.status == "live").count()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "apps": apps,
        "posts": posts,
        "app_count": app_count,
        "parse_features": parse_features,
        "parse_tags": parse_tags,
        "strip_markdown": strip_markdown,
    })


@router.get("/apps")
def apps_gallery(request: Request, category: str = None, db: Session = Depends(get_db)):
    q = db.query(App).order_by(App.sort_order)
    if category:
        q = q.filter(App.category == category)
    apps = q.all()
    categories = [
        ("all", "All"),
        ("productivity", "Productivity"),
        ("analytics", "Analytics"),
        ("marketing", "Marketing"),
        ("operations", "Operations"),
        ("devops", "DevOps"),
    ]
    return templates.TemplateResponse("apps.html", {
        "request": request,
        "apps": apps,
        "categories": categories,
        "selected_category": category or "all",
        "parse_features": parse_features,
    })


@router.get("/apps/{slug}")
def app_detail(request: Request, slug: str, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.slug == slug).first()
    if not app:
        return RedirectResponse(url="/apps", status_code=303)
    features = parse_features(app.features)
    return templates.TemplateResponse("app_detail.html", {
        "request": request,
        "app": app,
        "features": features,
    })


@router.get("/team")
def team_page(request: Request, db: Session = Depends(get_db)):
    members = db.query(TeamMember).filter(TeamMember.active == True).order_by(TeamMember.sort_order).all()
    return templates.TemplateResponse("team.html", {
        "request": request,
        "members": members,
    })


@router.get("/blog")
def blog_list(request: Request, db: Session = Depends(get_db)):
    posts = db.query(BlogPost).filter(BlogPost.published == True).order_by(
        BlogPost.published_at.desc()
    ).all()
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "posts": posts,
        "parse_tags": parse_tags,
    })


@router.get("/blog/{slug}")
def blog_post_page(request: Request, slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug).first()
    if not post:
        return RedirectResponse(url="/blog", status_code=303)
    content_html = markdown.markdown(
        post.content, extensions=["fenced_code", "tables", "nl2br"]
    )
    tags = parse_tags(post.tags)
    return templates.TemplateResponse("blog_post.html", {
        "request": request,
        "post": post,
        "content_html": content_html,
        "tags": tags,
    })


@router.get("/contact")
def contact_page(request: Request):
    sent = request.query_params.get("sent")
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "sent": sent,
    })


@router.post("/contact")
def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(""),
    message: str = Form(...),
    website: str = Form(""),
    db: Session = Depends(get_db),
):
    if website:
        return RedirectResponse(url="/contact?sent=1", status_code=303)
    submission = ContactSubmission(
        name=name,
        email=email,
        company=company if company else None,
        message=message,
        source=request.query_params.get("utm_source", ""),
    )
    db.add(submission)
    db.commit()
    return RedirectResponse(url="/contact?sent=1", status_code=303)


@router.get("/pricing")
def pricing_page(request: Request):
    return templates.TemplateResponse("pricing.html", {"request": request})


@router.get("/partners")
def partners_page(request: Request):
    return templates.TemplateResponse("partners.html", {"request": request})


@router.get("/invite")
def invite_page(request: Request, error: str = None):
    return templates.TemplateResponse("invite.html", {"request": request, "error": error})


@router.get("/invite/success")
def invite_success(request: Request):
    return templates.TemplateResponse("invite_success.html", {"request": request})
