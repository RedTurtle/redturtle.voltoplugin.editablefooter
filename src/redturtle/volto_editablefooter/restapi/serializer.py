# -*- coding: utf-8 -*-
from redturtle.volto_editablefooter.interfaces import IEditableFooterSettings
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
        for i in range(4):
            field_id = "column_{}_text".format(i + 1)
            json_data["data"][field_id] = json.loads(
                json_data["data"][field_id]
            )
        for field, props in json_data["schema"]["properties"].items():
            if field.endswith("_text"):
                props["default"] = json.loads(props["default"])
        return json_data
