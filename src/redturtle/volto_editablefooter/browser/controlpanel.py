# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from redturtle.volto_editablefooter.interfaces import IEditableFooterSettings
from redturtle.volto_editablefooter import _


class EditableFooterForm(controlpanel.RegistryEditForm):

    schema = IEditableFooterSettings
    label = _(
        "editable_footer_settings_label", default="Editable Footer Settings"
    )
    description = _(
        "editable_footer_settings_help",
        default="Set infos for four columns in footer.",
    )


class EditableFooter(controlpanel.ControlPanelFormWrapper):
    form = EditableFooterForm
