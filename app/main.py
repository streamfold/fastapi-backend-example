import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.main import api_router
from app.core.config import settings

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import DEPLOYMENT_ENVIRONMENT, SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

def initialize_tracing():
    if settings.AXIOM_API_KEY:
        from rotel import Config, Rotel

        rotel = Rotel(
            enabled = True,
            debug_log = ["traces"],
            exporter = Config.otlp_exporter(
                endpoint="https://api.axiom.co",
                protocol="http",
                headers={
                    "Authorization": f"Bearer {settings.AXIOM_API_KEY}",
                    "X-Axiom-Dataset": settings.AXIOM_DATA_SET,
                }
            ),
        )
        rotel.start()

        resource = Resource(
            attributes={
                SERVICE_NAME: "fastapi-backend-example",
                DEPLOYMENT_ENVIRONMENT: settings.ENVIRONMENT,
            }
        )
        provider = TracerProvider(resource=resource)
        processor = BatchSpanProcessor(
            OTLPSpanExporter(),
        )
        provider.add_span_processor(processor)

        trace.set_tracer_provider(provider)

def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

initialize_tracing()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

FastAPIInstrumentor.instrument_app(app)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
