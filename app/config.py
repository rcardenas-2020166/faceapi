import json
from pydantic_settings import BaseSettings

# Orígenes permitidos por ambiente — alineados con AllowedOrigins del WebAPI .NET
_CORS_BY_ENV: dict[str, list[str]] = {
    "dev": [
        "http://localhost:4200",
        "http://192.168.1.4:4200",
    ],
    "stg": [
        "https://simmta.pruebas.gt.mimeta-sa.com",
    ],
    "prod": [
        # Ajustar cuando esté definida la URL de producción del frontend
        "https://simmta.gt.mimeta-sa.com",
    ],
}


class Settings(BaseSettings):
    app_env: str = "dev"
    port: int = 8001
    min_detection_confidence: float = 0.55

    # Permite sobreescribir la lista de orígenes vía env var (JSON string)
    # Ej: CORS_ORIGINS_OVERRIDE='["https://mi-dominio.com"]'
    cors_origins_override: str = ""

    @property
    def cors_origins(self) -> list[str]:
        if self.cors_origins_override:
            return json.loads(self.cors_origins_override)
        return _CORS_BY_ENV.get(self.app_env, _CORS_BY_ENV["dev"])

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
