# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from redturtle.voltoplugin.editablefooter.testing import (
    VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING,
)
from redturtle.voltoplugin.editablefooter.interfaces import (
    IEditableFooterSettings,
)
from transaction import commit

import json
import unittest


class FooterColumnsEndpointTest(unittest.TestCase):
    layer = VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.controlpanel_url = "/@controlpanels/editable-footer-settings"
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.value = {"foo": "bar"}
        self.set_record_value(
            field="footer_columns", value=json.dumps(self.value)
        )

    def tearDown(self):
        self.api_session.close()

    def set_record_value(self, field, value):
        api.portal.set_registry_record(
            field, value, interface=IEditableFooterSettings
        )
        commit()

    def test_route_exists(self):
        response = self.api_session.get("/@footer-columns")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"), "application/json"
        )

    def test_return_json_data(self):

        response = self.api_session.get("/@footer-columns")
        result = response.json()

        self.assertEqual(result, self.value)
