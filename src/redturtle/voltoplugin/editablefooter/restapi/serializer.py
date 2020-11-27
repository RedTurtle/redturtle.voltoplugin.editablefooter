# -*- coding: utf-8 -*-
from redturtle.voltoplugin.editablefooter.interfaces import (
    IEditableFooterSettings,
)
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(ISerializeToJson)
@adapter(IEditableFooterSettings)
class EditableFooterControlpanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super(
            EditableFooterControlpanelSerializeToJson, self
        ).__call__()
        conf = json_data["data"].get("footer_columns", "")
        if conf:
            json_data["data"]["footer_columns"] = json.loads(conf)
        return json_data
