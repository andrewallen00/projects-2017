from __future__ import absolute_import

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


# from django.conf import settings
# from importlib import import_module
from django.contrib.sessions.models import Session

from zerver.models import (
    UserProfile, get_user_profile_by_id,
    get_user_profile_by_email, get_realm
)

from zerver.lib.test_classes import (
    ZulipTestCase,
)

# session_engine = import_module(settings.SESSION_ENGINE)


class TestSessions(ZulipTestCase):
    def test_delete_session(self):
        self.login('hamlet@zulip.com')
        result = self.client.get("/")
        print(result)
        print(type(result))
        print(result.content)
        print(result.status_code)
        self.assertIn('_auth_user_id', self.client.session)
        user_profile = get_user_profile_by_email('hamlet@zulip.com')
        print(user_sessions(user_profile))
        for session in user_sessions(user_profile):
            delete_session(session)
        # print(user_sessions(user_profile))
        result = self.client.get("/")
        self.assertEqual('/login', result.url)
        print(result)
        print(type(result))
        print(result.url)

    def test_delete_user_session(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile = get_user_profile_by_email('hamlet@zulip.com')
        delete_user_sessions(user_profile)
        result = self.client.get("/")
        # print(result)
        # print(type(result))
        self.assertEqual('/login', result.url)
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        result = self.client.get("/")
        delete_user_sessions(user_profile)
        # print(result)
        # print(type(result))
        self.assertIn('_auth_user_id', self.client.session)

    def test_delete_realm_user_sessions(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        realm = get_realm('zulip')
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        result = self.client.get('/')
        # print(result)
        delete_realm_user_sessions(realm)
        result = self.client.get('/')
        # print(result)
        self.assertEqual('/login', result.url)

    def test_delete_all_user_sessions(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        result = self.client.get('/')
        # print(result)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        result = self.client.get('/')
        # print(result)
        delete_all_user_sessions()
        result = self.client.get('/')
        # print(result)
        self.assertEqual('/login', result.url)

    def test_delete_all_deactivated_user_sessions(self):
        self.login('hamlet@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        result = self.client.get('/')
        print(result)
        user_profile_1 = get_user_profile_by_email('hamlet@zulip.com')
        print(user_profile_1.is_active)
        for session in Session.objects.all():
            print(session.get_decoded())
        self.client_post('/accounts/logout/')
        # print(user_profile_1.realm.deactivated)
        # user_profile_1.realm.deactivated = True
        user_profile_1.is_active = False
        print(user_profile_1.is_active)
        for session in Session.objects.all():
            print(session.get_decoded())
            user_id = get_session_user(session)
            print(user_id)
        delete_all_deactivated_user_sessions()
        test = self.client.get('/')
        print(test)
        # self.assertEqual('/login', result.url)
        self.login('othello@zulip.com')
        self.assertIn('_auth_user_id', self.client.session)
        user_profile_2 = get_user_profile_by_email('othello@zulip.com')
        result = self.client.get('/')
        print(result)
        user_profile_2.is_active = True
        print(user_profile_2.is_active)
        delete_all_deactivated_user_sessions()
        result = self.client.get('/')
        print(result)
        self.assertIn('_auth_user_id', self.client.session)
