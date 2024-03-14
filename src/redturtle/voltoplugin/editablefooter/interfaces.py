# -*- coding: utf-8 -*-
from plone.restapi.controlpanels.interfaces import IControlpanel
from redturtle.voltoplugin.editablefooter import _
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText


class IRedturtleVoltoEditablefooterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEditableFooterSettings(IControlpanel):
    footer_columns = SourceText(
        title=_("footer_columns_label", default="Footer columns"),
        description=_(
            "footer_columns_help",
            default="Set a list of custom columns for the footer. "
            "You can have different sets for each portal's languages.",
        ),
        required=True,
        default="",
    )
