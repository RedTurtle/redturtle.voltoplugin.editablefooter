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
        json_data = super(EditableFooterControlpanelSerializeToJson, self).__call__()
        for field in ["footer_columns", "footer_top"]:
            value = json_data["data"].get(field, "")
            if value:
                json_data["data"][field] = json.loads(value)
        return json_data
