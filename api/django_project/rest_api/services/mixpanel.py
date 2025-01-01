from mixpanel import Mixpanel

from django_project import settings


class MixpanelService:
    def __init__(self, mxp: Mixpanel) -> None:
        self.mxp = mxp

    def track_event(self, merchant_id: int, event_name: str, properties: dict) -> None:
        if settings.IS_PRODUCTION:
            self.mxp.track(merchant_id, event_name, properties)
