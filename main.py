from fastapi import FastAPI
from presentation_layer.user_routes import user_router
from presentation_layer.course_routes import course_router
from presentation_layer.module_routes import module_router
from presentation_layer.resource_routes import resource_router
from presentation_layer.enrollment_routes import enrollment_router
from presentation_layer.auth import auth_router
from presentation_layer.media_routes import media_router
from presentation_layer.course_report_routes import course_reports_router
from contextlib import asynccontextmanager
from database import db_manager
from fastapi.middleware.cors import CORSMiddleware
from configs import settings
from fastapi_pagination import add_pagination




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Starting")
    db_manager.init_database_pool(5, 10)
    db_manager.init_db_tables()
    yield 
    print("Application shutdown")
    db_manager.close_database_pool()



app = FastAPI(
    version = "0.0.1",
    title = "VRX Learn", 
    lifespan = lifespan
)

# Add Basic Pagination Support using fastapi-pagination.
add_pagination(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors.allowed_origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(course_router)
app.include_router(module_router)
app.include_router(resource_router)
app.include_router(enrollment_router)
app.include_router(media_router)
app.include_router(course_reports_router)
