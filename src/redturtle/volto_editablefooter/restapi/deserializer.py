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
        data = json_body(self.controlpanel.request)
        proxy = self.registry.forInterface(
            self.schema, prefix=self.schema_prefix
        )
        schema_data = {}
        errors = []
        fake_context = FakeDXContext()

        for name, field in getFields(self.schema).items():
            field_data = schema_data.setdefault(self.schema, {})

            if name in data:
                deserializer = queryMultiAdapter(
                    (field, fake_context, self.request), IFieldDeserializer
                )
                try:
                    value = data[name]
                    if name.endswith("_text"):
                        value = json.dumps(value)

                    # Make it sane
                    value = deserializer(value)

                    # Validate required etc
                    field.validate(value)
                    # Set the value.
                    setattr(proxy, name, value)

                except ValueError as e:
                    errors.append(
                        {"message": str(e), "field": name, "error": e}
                    )
                except ValidationError as e:
                    errors.append(
                        {"message": e.doc(), "field": name, "error": e}
                    )
                else:
                    field_data[name] = value
        # Validate schemata
        for schema, field_data in schema_data.items():
            validator = queryMultiAdapter(
                (self.context, self.request, None, schema, None),
                IManagerValidator,
            )
            for error in validator.validate(field_data):
                errors.append({"error": error, "message": str(error)})

        if errors:
            raise BadRequest(errors)
