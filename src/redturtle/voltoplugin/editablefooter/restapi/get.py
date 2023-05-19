# -*- coding: utf-8 -*-
from redturtle.voltoplugin.editablefooter.interfaces import (
    IEditableFooterSettings,
)
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class FooterColumns(Service):
    def __init__(self, context, request):
        super(FooterColumns, self).__init__(context, request)

    def reply(self):
        record = api.portal.get_registry_record(
            "footer_columns", interface=IEditableFooterSettings, default=""
        )
        if not record:
            return []
        data = json.loads(record)
        portal_url = api.portal.get().absolute_url()
        for el in data or []:
            for item in el.get("items") or []:
                if item.get("text") and item.get("text").get("data"):
                    item["text"]["data"] = item["text"]["data"].replace(
                        'href="/', f'href="{portal_url}/'
                    )
        return data
