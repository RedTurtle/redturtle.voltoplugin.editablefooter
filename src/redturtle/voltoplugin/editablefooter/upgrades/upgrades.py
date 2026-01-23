from Products.CMFCore.utils import getToolByName


PROFILE_ID = "redturtle.voltoplugin.editablefooter:default"


def to_1001(context):
    setup = getToolByName(context, "portal_setup")

    # Reimport rolemap (assign new permission to Manager)
    setup.runImportStepFromProfile(PROFILE_ID, "rolemap")

    # Reimport controlpanel (use new permission)
    setup.runImportStepFromProfile(PROFILE_ID, "controlpanel")
