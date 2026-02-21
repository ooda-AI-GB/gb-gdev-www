from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base

app = FastAPI(title="Gigabox", description="Complete Software Stack for Growing Businesses")


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
from app.pages import router as pages_router
from app.api import router as api_router

app.include_router(api_router)
app.include_router(pages_router)


@app.on_event("startup")
def startup_event():
    import app.models
    Base.metadata.create_all(bind=engine)
    from app.seed import seed_if_empty
    seed_if_empty()
