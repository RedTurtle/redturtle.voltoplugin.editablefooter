# -*- coding: utf-8 -*-
from plone.restapi.controlpanels.interfaces import IControlpanel
from redturtle.voltoplugin.editablefooter import _
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import SourceText


class IRedturtleVoltoEditablefooterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEditableFooterSettings(IControlpanel):
    footer_top = SourceText(
        title=_("footer_top_label", default="Footer top"),
        description=_(
            "footer_top_help",
            default="Insert some text that will be shown as first element in the footer, before the columns.",
        ),
        required=False,
        default="",
    )
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
