from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def with_security_examples(app: FastAPI):
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        components = openapi_schema.setdefault("components", {})
        resp = components.setdefault("responses", {})
        resp["UnauthorizedError"] = {
            "description": "Missing or invalid authentication credentials",
            "content": {"application/json": {"example": {"detail": "Not authenticated"}}}
        }
        resp["ForbiddenError"] = {
            "description": "The user does not have enough privileges",
            "content": {"application/json": {"example": {"detail": "Not enough permissions"}}}
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi
