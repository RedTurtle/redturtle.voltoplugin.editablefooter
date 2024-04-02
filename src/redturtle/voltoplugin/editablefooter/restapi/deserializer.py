# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.deserializer.controlpanels import ControlpanelDeserializeFromJson
from plone.restapi.interfaces import IBlockFieldDeserializationTransformer
from plone.restapi.interfaces import IDeserializeFromJson
from redturtle.voltoplugin.editablefooter import _
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings
from redturtle.voltoplugin.editablefooter.restapi import fix_footer_top_blocks
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
        data = req.get("footer_columns", [])
        if not data:
            errors.append(
                {
                    "message": api.portal.translate(
                        _("missing_data_label", default="Missing data")
                    ),
                    "field": "footer_columns",
                }
            )
            raise BadRequest(errors)
        if not isinstance(data, list):
            errors.append(
                {
                    "message": api.portal.translate(
                        _(
                            "wrong_type_data_label",
                            default="Wrong type: need to be a list of values",
                        )
                    ),
                    "field": "footer_columns",
                }
            )
            raise BadRequest(errors)
        for path_setting in data:
            footer_top = path_setting.get("footerTop", {}).get("blocks", {})
            if footer_top:
                path_setting["footerTop"]["blocks"] = fix_footer_top_blocks(
                    context=self.context,
                    blocks=footer_top,
                    transformer=IBlockFieldDeserializationTransformer,
                )

        try:
            # later we need to do some validations
            setattr(proxy, "footer_columns", json.dumps(data))
        except ValueError as e:
            errors.append({"message": str(e), "field": "footer_columns", "error": e})

        if errors:
            raise BadRequest(errors)
