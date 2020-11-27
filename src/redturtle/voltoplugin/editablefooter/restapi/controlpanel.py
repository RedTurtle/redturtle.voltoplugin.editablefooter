# -*- coding: utf-8 -*-
from plone.restapi.controlpanels import RegistryConfigletPanel
from redturtle.voltoplugin.editablefooter.interfaces import (
    IRedturtleVoltoEditablefooterLayer,
    IEditableFooterSettings,
)
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, IRedturtleVoltoEditablefooterLayer)
@implementer(IEditableFooterSettings)
class EditableFooterControlpanel(RegistryConfigletPanel):
    schema = IEditableFooterSettings
    configlet_id = "EditableFooter"
    configlet_category_id = "Products"
    schema_prefix = None
