# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from redturtle.voltoplugin.editablefooter import _
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings


class EditableFooterForm(controlpanel.RegistryEditForm):
    schema = IEditableFooterSettings
    label = _("editable_footer_settings_label", default="Editable Footer Settings")
    description = _(
        "editable_footer_settings_help",
        default="Set infos for columns in footer.",
    )


class EditableFooter(controlpanel.ControlPanelFormWrapper):
    form = EditableFooterForm
