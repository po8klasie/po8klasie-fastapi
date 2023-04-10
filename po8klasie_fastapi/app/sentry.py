import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from po8klasie_fastapi.app.config import settings


def setup_sentry():
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            integrations=[
                StarletteIntegration(),
                FastApiIntegration(),
            ],
            traces_sample_rate=1.0,
        )
