# This file is a part of the AnyBlok / Pyramid project
#
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase
from pyramid.httpexceptions import HTTPUnauthorized


class TestCredential(PyramidBlokTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCredential, cls).setUpClass()
        cls.User = cls.registry.User
        cls.CredentialStore = cls.registry.User.CredentialStore
        cls.User.insert(login='user.1', first_name="User", last_name="1")
        cls.CredentialStore.insert(login='user.1', password="P1")

    def setUp(self):
        # to load pyramid configuration
        super(TestCredential, self).setUp()

    def test_check_login_ok(self):
        self.assertEqual(
            self.User.check_login(login="user.1", password="P1"),
            'user.1'
        )

    def test_check_login_ko(self):
        with self.assertRaises(HTTPUnauthorized):
            self.User.check_login(login="user.1", password="P2")

    def test_view_login_ok(self):
        self.webserver.post_json(
            '/login', dict(login="user.1", password="P1"), status=302)

    def test_view_login_ko(self):
        self.webserver.post_json(
            '/login', dict(login="user.1", password="P2"), status=401)