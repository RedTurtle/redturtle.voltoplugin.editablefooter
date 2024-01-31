# -*- coding: utf-8 -*-
from redturtle.voltoplugin.editablefooter.interfaces import (
    IEditableFooterSettings,
)
from plone import api
from plone.registry.interfaces import IRegistry
from plone.restapi.services import Service
from zope.component import getUtility
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

try:
    from plone.volto.interfaces import IVoltoSettings

    HAS_PLONE_VOLTO = True
except ImportError:
    HAS_PLONE_VOLTO = False

import json


@implementer(IPublishTraverse)
class EditableFooterGet(Service):
    def reply(self):
        res = {"footer_top": None, "footer_columns": None}
        footer_top = api.portal.get_registry_record(
            "footer_top", interface=IEditableFooterSettings, default=""
        )
        footer_columns = api.portal.get_registry_record(
            "footer_columns", interface=IEditableFooterSettings, default=""
        )
        if footer_top:
            res["footer_top"] = json.loads(footer_top)
        if not footer_columns:
            return res
        data = json.loads(footer_columns)
        portal_url = self.get_portal_url()
        for el in data or []:
            if isinstance(el, dict):
                for item in el.get("items") or []:
                    if (
                        isinstance(item, dict)
                        and item.get("text")  # noqa: W503
                        and isinstance(item.get("text"), dict)  # noqa: W503
                        and item.get("text").get("data")  # noqa: W503
                    ):
                        item["text"]["data"] = item["text"]["data"].replace(
                            'href="/', f'href="{portal_url}/'
                        )
        res["footer_columns"] = data
        return res

    def get_portal_url(self):
        portal_url = api.portal.get().absolute_url()
        # BBB
        if portal_url.endswith("/api"):
            portal_url = portal_url[:4]
        if not HAS_PLONE_VOLTO:
            return portal_url
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings_frontend_domain = getattr(settings, "frontend_domain", None)
        if not settings_frontend_domain:
            return portal_url
        if settings_frontend_domain != "http://localhost:3000":
            portal_url = settings_frontend_domain
        if portal_url.endswith("/"):
            portal_url = portal_url[:-1]
        return portal_url
