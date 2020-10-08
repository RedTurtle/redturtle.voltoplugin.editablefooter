# -*- coding: utf-8 -*-
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import (
    ControlpanelDeserializeFromJson,
    FakeDXContext,
)
from plone.restapi.interfaces import IDeserializeFromJson
from plone.restapi.interfaces import IFieldDeserializer
from redturtle.volto_editablefooter.interfaces import IEditableFooterSettings
from z3c.form.interfaces import IManagerValidator
from zExceptions import BadRequest
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.schema import getFields
from zope.schema.interfaces import ValidationError

import json


@implementer(IDeserializeFromJson)
@adapter(IEditableFooterSettings)
class EditableFooterControlpanelDeserializeFromJson(
    ControlpanelDeserializeFromJson
):
    def __call__(self):
        req = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(
            self.schema, prefix=self.schema_prefix
        )
        errors = []
        data = req.get("footer_columns", {})
        if not data:
            errors.append(
                {"message": "Missing data", "field": "footer_columns"}
            )
            raise BadRequest(errors)
        try:
            # later we need to do some validations
            setattr(proxy, "footer_columns", json.dumps(data))
        except ValueError as e:
            errors.append(
                {"message": str(e), "field": "footer_columns", "error": e}
            )

        if errors:
            raise BadRequest(errors)
