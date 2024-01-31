# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import (
    ControlpanelDeserializeFromJson,
)
from plone.restapi.interfaces import IDeserializeFromJson
from redturtle.voltoplugin.editablefooter.interfaces import (
    IEditableFooterSettings,
)
from zExceptions import BadRequest
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(IDeserializeFromJson)
@adapter(IEditableFooterSettings)
class EditableFooterControlpanelDeserializeFromJson(ControlpanelDeserializeFromJson):
    def __call__(self):
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(self.schema, prefix=self.schema_prefix)
        errors = []
        footer_top = req.get("footer_top", {})
        footer_columns = req.get("footer_columns", {})

        if not footer_columns:
            errors.append({"message": "Missing data", "field": "footer_columns"})
            raise BadRequest(errors)
        try:
            # later we need to do some validations
            setattr(proxy, "footer_columns", json.dumps(footer_columns))
        except ValueError as e:
            errors.append({"message": str(e), "field": "footer_columns", "error": e})
        try:
            # later we need to do some validations
            setattr(proxy, "footer_top", json.dumps(footer_top))
        except ValueError as e:
            errors.append({"message": str(e), "field": "footer_top", "error": e})
        if errors:
            raise BadRequest(errors)
