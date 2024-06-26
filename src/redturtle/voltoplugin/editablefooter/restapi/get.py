# -*- coding: utf-8 -*-
from plone import api
from plone.registry.interfaces import IRegistry
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings
from redturtle.voltoplugin.editablefooter.restapi import fix_footer_top_blocks
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
class FooterColumns(Service):
    def reply(self):
        record = api.portal.get_registry_record(
            "footer_columns", interface=IEditableFooterSettings, default=""
        )
        if not record:
            return []
        data = json.loads(record)
        portal_url = self.get_portal_url()
        for el in data or []:
            if isinstance(el, dict):
                footer_top = el.get("footerTop", {}).get("blocks", {})
                if footer_top:
                    el["footerTop"]["blocks"] = fix_footer_top_blocks(
                        context=self.context,
                        blocks=footer_top,
                        transformer=IBlockFieldSerializationTransformer,
                    )

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
        return json_compatible(data)

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
