# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.controlpanels import ControlpanelSerializeToJson
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings
from redturtle.voltoplugin.editablefooter.restapi import fix_footer_top_blocks
from zope.component import adapter
from zope.interface import implementer

import json


@implementer(ISerializeToJson)
@adapter(IEditableFooterSettings)
class EditableFooterControlpanelSerializeToJson(ControlpanelSerializeToJson):
    def __call__(self):
        json_data = super().__call__()
        conf = json_data["data"].get("footer_columns", "")
        if not conf:
            return json_data
        footer_columns = json.loads(conf)

        for path_setting in footer_columns:
            footer_top = path_setting.get("footerTop", {}).get("blocks", {})
            if footer_top:
                path_setting["footerTop"]["blocks"] = fix_footer_top_blocks(
                    context=api.portal.get(),
                    blocks=footer_top,
                    transformer=IBlockFieldSerializationTransformer,
                )

        json_data["data"]["footer_columns"] = footer_columns
        return json_data
