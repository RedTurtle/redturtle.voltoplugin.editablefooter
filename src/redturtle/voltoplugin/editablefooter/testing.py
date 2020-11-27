# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PloneRestApiDXLayer
from plone.testing import z2

import redturtle.voltoplugin.editablefooter
import plone.restapi


class VoltoEditableFooterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.voltoplugin.editablefooter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "redturtle.voltoplugin.editablefooter:default")


VOLTO_EDITABLEFOOTER_FIXTURE = VoltoEditableFooterLayer()


VOLTO_EDITABLEFOOTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_EDITABLEFOOTER_FIXTURE,),
    name="VoltoEditableFooterLayer:IntegrationTesting",
)


VOLTO_EDITABLEFOOTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_EDITABLEFOOTER_FIXTURE,),
    name="VoltoEditableFooterLayer:FunctionalTesting",
)


class VoltoEditableFooterRestApiLayer(PloneRestApiDXLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        super(VoltoEditableFooterRestApiLayer, self).setUpZope(
            app, configurationContext
        )

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.voltoplugin.editablefooter)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "redturtle.voltoplugin.editablefooter:default")


VOLTO_EDITABLEFOOTER_API_FIXTURE = VoltoEditableFooterRestApiLayer()
VOLTO_EDITABLEFOOTER_API_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VOLTO_EDITABLEFOOTER_API_FIXTURE,),
    name="VoltoEditableFooterRestApiLayer:Integration",
)

VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VOLTO_EDITABLEFOOTER_API_FIXTURE, z2.ZSERVER_FIXTURE),
    name="VoltoEditableFooterRestApiLayer:Functional",
)
