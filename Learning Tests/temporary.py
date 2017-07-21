from __future__ import absolute_import

import logging

from zerver.lib.sessions import (
    get_session_dict_user,
    get_session_user,
    user_sessions,
    delete_session,
    delete_user_sessions,
    delete_realm_user_sessions,
    delete_all_user_sessions,
    delete_all_deactivated_user_sessions,
)

from zerver.lib.actions import set_default_streams
from mock import patch
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from importlib import import_module
from typing import List, Mapping, Optional, Text

from zerver.models import (
    Realm, Subscription, UserProfile, get_user_profile_by_id,
    get_user_profile_by_email, get_realm, Recipient, Stream
)

from zerver.lib.test_classes import (
    ZulipTestCase,
)

session_engine = import_module(settings.SESSION_ENGINE)


class TestSessions(ZulipTestCase):
    def test_delete_session(self):
        self.login('hamlet@zulip.com')
        user = auth.get_user(self.client)
        assert user.is_authenticated()
        self.assertIn('_auth_user_id', self.client.session)
        user_profile = get_user_profile_by_email('hamlet@zulip.com')
        print(user_sessions(user_profile))
        for session in user_sessions(user_profile):
            delete_session(session)
        print(user_sessions(user_profile))
        user = auth.get_user(self.client)
        assert user.is_anonymous()
        self.assertNotIn('_auth_user_id', self.client.session)
        #self.assertIsNone(get_session_dict_user(self.client.session))

    def test_delete_user_sessions(self):
        self.login('hamlet@zulip.com')
        user1 = auth.get_user(self.client)
        assert user1.is_authenticated()
        #self.assertIn('_auth_user_id', self.client.session)
        user_profile_1 = get_user_profile_by_email('hamlet@zulip.com')
        user_1 = auth.get_user(self.client)
        user_1_id = self.client.session['_auth_user_id']
        print(self.client.session['_auth_user_id'])
        #self.assertIn(user_1.id, self.client.session)
        print(user_profile_1)
        print(user_1)
        #print(user_1.id)
        print(user_sessions(user_profile_1))
        self.login('othello@zulip.com')
        user2 = auth.get_user(self.client)
        assert user2.is_authenticated()
        #self.assertIn('_auth_user_id', self.client.session)
        user_profile_2 = get_user_profile_by_email('othello@zulip.com')
        print(user_profile_2)
        print(user_sessions(user_profile_2))
        delete_user_sessions(user_profile_1)
        assert user1.is_anonymous()
        assert user2.is_authenticated()
        #self.assertNotIn(user_1_id, self.client.session)
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        print(user_profile_2)
        print(user_sessions(user_profile_2))

    def test_delete_all_user_sessions(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_1 = get_user_profile_by_email('hamlet@zulip.com')
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        user_1_id = self.client.session['_auth_user_id']
        print(user_1_id)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_2 = get_user_profile_by_email('othello@zulip.com')
        print(user_profile_2)
        print(user_sessions(user_profile_2))
        user_2_id = self.client.session['_auth_user_id']
        print(user_2_id)
        delete_all_user_sessions()
        self.assertNotIn(user_1_id, self.client.session)
        self.assertNotIn(user_2_id, self.client.session)
        #
        #
        #
        #THESE MAY NOT BE WORKING!!!! CHECK!!
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        print(user_profile_2)
        print(user_sessions(user_profile_2))

    def test_delete_realm_user_sessions(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_1 = get_user_profile_by_email('hamlet@zulip.com')
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        user_1_id = self.client.session['_auth_user_id']
        print(user_1_id)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_2 = get_user_profile_by_email('othello@zulip.com')
        print(user_profile_2)
        print(user_sessions(user_profile_2))
        user_2_id = self.client.session['_auth_user_id']
        print(user_2_id)
        realm = get_realm('zulip')
        print(realm)
        delete_realm_user_sessions(realm)
        self.assertNotIn(user_1_id, self.client.session)
        self.assertNotIn(user_2_id, self.client.session)
        #
        #
        #
        # THESE MAY NOT BE WORKING!!!! CHECK!!
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        print(user_profile_2)
        print(user_sessions(user_profile_2))

    def test_delete_all_deactivated_user_sessions(self):
        self.login('hamlet@zulip.com')
        user_1_id = int(self.client.session['_auth_user_id'])
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_1 = get_user_profile_by_email('hamlet@zulip.com')
        print(user_1_id)
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        print(user_profile_1.is_active)
        user_profile_1.is_active = False
        print(user_profile_1.is_active)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_2 = get_user_profile_by_email('othello@zulip.com')
        user_2_id = int(self.client.session['_auth_user_id'])
        user_profile_2.is_active = True
        print(user_2_id)
        print(user_profile_2)
        print(user_sessions(user_profile_2))
        delete_all_deactivated_user_sessions()
        print(user_profile_1)
        print(user_sessions(user_profile_1))
        print(user_profile_2)
        print(user_sessions(user_profile_2))
        #self.assertNotIn('_auth_user_id', self.client.session)
        print(user_2_id)
        print(type(user_2_id))
        print(self.client.session['_auth_user_id'])
        print(type(self.client.session['_auth_user_id']))
        #assert user.is_authenticated()
        print(int(self.client.session['_auth_user_id']))


