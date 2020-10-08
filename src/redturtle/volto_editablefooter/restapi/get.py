# -*- coding: utf-8 -*-
from redturtle.volto_editablefooter.interfaces import IEditableFooterSettings
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
        json_data = []
        for i in range(4):
            title_id = "column_{}_title".format(i + 1)
            text_id = "column_{}_text".format(i + 1)
            title = api.portal.get_registry_record(
                title_id, interface=IEditableFooterSettings, default=""
            )
            text = json.loads(
                api.portal.get_registry_record(
                    text_id, interface=IEditableFooterSettings, default=""
                )
            )
            if title or (text["data"] not in ["", "<p><br/></p>"]):
                json_data.append({"title": title, "text": text})
        return json_data
