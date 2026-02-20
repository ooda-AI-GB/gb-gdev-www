from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class App(Base):
    __tablename__ = "apps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    tagline = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    live_url = Column(String(500))
    screenshot_url = Column(String(500))
    features = Column(Text)
    replaces = Column(String(500))
    evolution_count = Column(Integer, default=0)
    status = Column(String(20), default="live")
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    role = Column(String(200), nullable=False)
    bio = Column(Text)
    credentials = Column(String(500))
    avatar_url = Column(String(500))
    linkedin_url = Column(String(500))
    sort_order = Column(Integer, default=0)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False)
    subtitle = Column(String(500))
    content = Column(Text, nullable=False)
    author = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(Text)
    published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    read_time_minutes = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(300), nullable=False)
    company = Column(String(300))
    message = Column(Text, nullable=False)
    source = Column(String(200))
    status = Column(String(20), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SiteAnalytics(Base):
    __tablename__ = "site_analytics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    page = Column(String(500), nullable=False)
    referrer = Column(String(500))
    utm_source = Column(String(200))
    utm_campaign = Column(String(200))
    visitor_id = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
