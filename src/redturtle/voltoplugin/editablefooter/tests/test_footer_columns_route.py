# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.restapi.testing import RelativeSession
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings
from redturtle.voltoplugin.editablefooter.testing import (
    VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING,
)
from transaction import commit
from zope.component import getUtility

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

        self.value = [
            {
                "items": [
                    {"text": {"data": '<a href="https://site.com/">Link 1</a>'}},
                    {"text": {"data": '<a href="/relative/to/this/site">Link 1</a>'}},
                ]
            }
        ]
        self.set_record_value(field="footer_columns", value=json.dumps(self.value))

        self.document = api.content.create(
            container=self.portal, type="Document", title="document"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def set_record_value(self, field, value):
        api.portal.set_registry_record(field, value, interface=IEditableFooterSettings)
        commit()

    def test_route_exists(self):
        response = self.api_session.get("/@footer-columns")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")

    def test_return_json_data(self):
        response = self.api_session.get("/@footer-columns")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # self.value has relative links, but the result should have absolute links
        self.assertNotEqual(result, self.value)
        self.assertEqual(
            json.dumps(result),
            json.dumps(self.value).replace('href=\\"/', f'href=\\"{self.portal_url}/'),
        )

    def test_return_expanded_resolveuid_in_footerTop_internal_links(self):
        data = [
            {
                "footerTop": {
                    "blocks": {
                        "2955de0f-ea5e-475f-8efd-34c7060b99b9": {
                            "@type": "slate",
                            "plaintext": " link ",
                            "value": [
                                {
                                    "children": [
                                        {
                                            "type": "link",
                                            "data": {
                                                "url": self.document.absolute_url(),
                                                "dataElement": "",
                                            },
                                            "children": [{"text": "link"}],
                                        },
                                    ],
                                    "type": "p",
                                }
                            ],
                        }
                    },
                    "blocks_layout": {
                        "items": ["2955de0f-ea5e-475f-8efd-34c7060b99b9"]
                    },
                },
                "rootPath": "/",
            }
        ]
        self.set_record_value(field="footer_columns", value=json.dumps(data))

        response = self.api_session.get("/@footer-columns").json()

        self.assertEqual(
            response[0]["footerTop"]["blocks"]["2955de0f-ea5e-475f-8efd-34c7060b99b9"][
                "value"
            ][0]["children"][0]["data"]["url"],
            self.document.absolute_url(),
        )


class FooterColumnsEndpointTestWithPloneVolto(FooterColumnsEndpointTest):
    layer = VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING

    def setUp(self):
        super().setUp()
        applyProfile(self.portal, "plone.volto:default")

    def test_return_json_data_with_portal_url_if_plone_volto_installed_and_not_configured(
        self,
    ):
        response = self.api_session.get("/@footer-columns")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # self.value has relative links, but the result should have absolute links
        self.assertNotEqual(result, self.value)
        self.assertEqual(
            json.dumps(result),
            json.dumps(self.value).replace('href=\\"/', f'href=\\"{self.portal_url}/'),
        )

    def test_return_json_data_with_frontend_domain_if_set(self):
        from plone.volto.interfaces import IVoltoSettings

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        settings.frontend_domain = "http://foo.org"
        commit()

        response = self.api_session.get("/@footer-columns")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        # self.value has relative links, but the result should have absolute links
        self.assertNotEqual(result, self.value)
        self.assertEqual(
            json.dumps(result),
            json.dumps(self.value).replace(
                'href=\\"/', f'href=\\"{settings.frontend_domain}/'
            ),
        )
