# -*- coding: utf-8 -*-
from plone.restapi.controlpanels.interfaces import IControlpanel
from redturtle.volto_editablefooter import _
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText
from zope.schema import TextLine


import json


class IRedturtleVoltoEditablefooterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEditableFooterSettings(IControlpanel):
    column_1_title = TextLine(
        title=_("column_1_title_label", default="Column 1: title"),
        description="",
        required=False,
        default="",
    )
    column_1_text = SourceText(
        title=_("column_1_text_label", default="Column 1: text"),
        description="",
        required=False,
        default=json.dumps({"content-type": "text/html", "data": ""}),
    )
    column_2_title = TextLine(
        title=_("column_2_title_label", default="Column 2: title"),
        description="",
        required=False,
        default="",
    )
    column_2_text = SourceText(
        title=_("column_2_text_label", default="Column 2: text"),
        description="",
        required=False,
        default=json.dumps({"content-type": "text/html", "data": ""}),
    )
    column_3_title = TextLine(
        title=_("column_3_title_label", default="Column 3: title"),
        description="",
        required=False,
        default="",
    )
    column_3_text = SourceText(
        title=_("column_3_text_label", default="Column 3: text"),
        description="",
        required=False,
        default=json.dumps({"content-type": "text/html", "data": ""}),
    )
    column_4_title = TextLine(
        title=_("column_4_title_label", default="Column 4: title"),
        description="",
        required=False,
        default="",
    )
    column_4_text = SourceText(
        title=_("column_4_text_label", default="Column 4: text"),
        description="",
        required=False,
        default=json.dumps({"content-type": "text/html", "data": ""}),
    )
