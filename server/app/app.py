from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.consumable.routes import router as consumable_router
from api.user.routes import router as user_router
from config.database import initiate_database
from config.settings import app_configs, settings

# Create the FastAPI app
app = FastAPI(**app_configs)

# Define the CORS client origin
origins = settings.CLIENT_ORIGIN

# Add CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include sub-module API routers
app.include_router(
    consumable_router,
    prefix="/consumable",
    tags=["Consumable"],
)

app.include_router(
    user_router,
    prefix="/user",
    tags=["User"],
)

# Set the environment
if settings.ENVIRONMENT.is_deployed:
    environment = (settings.ENVIRONMENT,)


# Initialize the database
@app.on_event("startup")
async def start_database():
    await initiate_database()
