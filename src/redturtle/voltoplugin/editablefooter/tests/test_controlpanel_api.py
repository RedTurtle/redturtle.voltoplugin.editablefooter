# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession
from redturtle.voltoplugin.editablefooter.interfaces import IEditableFooterSettings
from redturtle.voltoplugin.editablefooter.testing import (
    VOLTO_EDITABLEFOOTER_API_FUNCTIONAL_TESTING,
)
from transaction import commit

import json
import unittest


class EditableFooterServiceTest(unittest.TestCase):
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

    def tearDown(self):
        self.api_session.close()

    def test_controlpanel_listed(self):
        response = self.api_session.get("/@controlpanels")

        titles = [x.get("title") for x in response.json()]
        self.assertIn("Editable footer settings", titles)

    def test_route_exists(self):
        response = self.api_session.get("/@controlpanels/editable-footer-settings")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "application/json")


class EditableFooterServiceDeserializerTest(unittest.TestCase):
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

        self.document = api.content.create(
            container=self.portal, type="Document", title="document"
        )
        commit()

    def tearDown(self):
        self.api_session.close()

    def get_record_value(self, field):
        record = api.portal.get_registry_record(
            field, interface=IEditableFooterSettings, default=""
        )
        return record

    def set_record_value(self, field, value):
        api.portal.set_registry_record(field, value, interface=IEditableFooterSettings)
        commit()

    def test_set_wrong_data(self):
        response = self.api_session.patch(self.controlpanel_url, json={"foo": "bar"})

        self.assertEqual(response.status_code, 400)

    def test_deserializer_convert_dict_into_json_string(self):
        data = [{"foo": "", "bar": 2}]
        self.api_session.patch(self.controlpanel_url, json={"footer_columns": data})
        commit()
        self.assertEqual(
            self.get_record_value(field="footer_columns"), json.dumps(data)
        )

    def test_deserializer_raise_error_if_footer_columns_not_a_list(self):
        data = {"foo": "", "bar": 2}
        res = self.api_session.patch(
            self.controlpanel_url, json={"footer_columns": data}
        )
        self.assertEqual(res.status_code, 400)

    def test_deserializer_save_resolveuid_in_footerTop_internal_links(self):
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
        res = self.api_session.patch(
            self.controlpanel_url, json={"footer_columns": data}
        )
        commit()

        stored_value = json.loads(self.get_record_value(field="footer_columns"))

        self.assertEqual(res.status_code, 204)
        self.assertEqual(
            stored_value[0]["footerTop"]["blocks"][
                "2955de0f-ea5e-475f-8efd-34c7060b99b9"
            ]["value"][0]["children"][0]["data"]["url"],
            f"resolveuid/{self.document.UID()}",
        )

    def test_serializer_return_expanded_resolveuid_in_footerTop_internal_links(self):
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
        self.api_session.patch(self.controlpanel_url, json={"footer_columns": data})
        commit()

        res = self.api_session.get(self.controlpanel_url).json()

        self.assertEqual(
            res["data"]["footer_columns"][0]["footerTop"]["blocks"][
                "2955de0f-ea5e-475f-8efd-34c7060b99b9"
            ]["value"][0]["children"][0]["data"]["url"],
            self.document.absolute_url(),
        )

    def test_serializer_convert_string_into_json_object(self):
        self.assertEqual(self.get_record_value(field="footer_columns"), "")
        value = [{"foo": "bar"}]
        self.set_record_value(field="footer_columns", value=json.dumps(value))

        response = self.api_session.get(self.controlpanel_url)
        result = response.json()["data"]["footer_columns"]

        self.assertEquals(result, value)
