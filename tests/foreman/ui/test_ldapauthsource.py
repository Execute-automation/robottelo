"""Test class for Active Directory Feature

:Requirement: Ldapauthsource

:CaseAutomation: Automated

:CaseLevel: Acceptance

:CaseComponent: UI

:TestType: Functional

:CaseImportance: High

:Upstream: No
"""
from nailgun import entities
from robottelo.config import settings
from robottelo.constants import LDAP_ATTR, LDAP_SERVER_TYPE
from robottelo.datafactory import generate_strings_list
from robottelo.decorators import (
    skip_if_not_set,
    tier1,
    tier2,
    upgrade,
)
from robottelo.test import UITestCase
from robottelo.ui.factory import make_ldapauth
from robottelo.ui.session import Session


class LDAPAuthSourceTestCase(UITestCase):
    """Implements Active Directory feature tests in UI."""

    @classmethod
    @skip_if_not_set('ldap')
    def setUpClass(cls):
        super(LDAPAuthSourceTestCase, cls).setUpClass()
        cls.ldap_user_name = settings.ldap.username
        cls.ldap_user_passwd = settings.ldap.password
        cls.base_dn = settings.ldap.basedn
        cls.group_base_dn = settings.ldap.grpbasedn
        cls.ldap_hostname = settings.ldap.hostname
        cls.ldap_ipa_user_name = settings.ipa.username_ipa
        cls.ldap_ipa_user_passwd = settings.ipa.password_ipa
        cls.ipa_base_dn = settings.ipa.basedn_ipa
        cls.ipa_group_base_dn = settings.ipa.grpbasedn_ipa
        cls.ldap_ipa_hostname = settings.ipa.hostname_ipa

    @tier1
    def test_positive_create_with_ad(self):
        """Create LDAP authentication with AD

        :id: 02693108-83d9-4b2b-969e-2d8a00d0a935

        :steps:

            1. Create a new LDAP Auth source with AD.
            2. Fill in all the fields appropriately for AD.

        :expectedresults: Whether creating LDAP Auth with AD is successful.

        :CaseImportance: Critical
        """
        with Session(self) as session:
            for server_name in generate_strings_list():
                with self.subTest(server_name):
                    make_ldapauth(
                        session,
                        name=server_name,
                        server=self.ldap_hostname,
                        server_type=LDAP_SERVER_TYPE['UI']['ad'],
                        login_name=LDAP_ATTR['login_ad'],
                        first_name=LDAP_ATTR['firstname'],
                        surname=LDAP_ATTR['surname'],
                        mail=LDAP_ATTR['mail'],
                        account_user=self.ldap_user_name,
                        account_passwd=self.ldap_user_passwd,
                        account_basedn=self.base_dn,
                        account_grpbasedn=self.group_base_dn,
                    )
                    self.assertIsNotNone(
                        self.ldapauthsource.search(server_name)
                    )

    @tier1
    def test_positive_delete_with_ad(self):
        """Delete LDAP authentication with AD

        :id: 0fbb09d3-7a19-468d-898c-1484a5682793

        :steps:

            1. Create a new LDAP Auth source with AD.
            2. Delete LDAP Auth source with AD.

        :expectedresults: Whether deleting LDAP Auth with AD is successful.

        :CaseImportance: Critical
        """
        with Session(self) as session:
            for server_name in generate_strings_list():
                with self.subTest(server_name):
                    make_ldapauth(
                        session,
                        name=server_name,
                        server=self.ldap_hostname,
                        server_type=LDAP_SERVER_TYPE['UI']['ad'],
                        login_name=LDAP_ATTR['login_ad'],
                        first_name=LDAP_ATTR['firstname'],
                        surname=LDAP_ATTR['surname'],
                        mail=LDAP_ATTR['mail'],
                        account_user=self.ldap_user_name,
                        account_passwd=self.ldap_user_passwd,
                        account_basedn=self.base_dn,
                        account_grpbasedn=self.group_base_dn,
                    )
                    self.assertIsNotNone(
                        self.ldapauthsource.search(server_name)
                    )
                    self.ldapauthsource.delete(server_name)

    @tier2
    @upgrade
    def test_positive_create_with_ad_org_and_loc(self):
        """Create LDAP auth_source for AD with org and loc assigned.

        :id: 4f595af4-fc01-44c6-a614-a9ec827e3c3c

        :steps:
            1. Create a new LDAP Auth source with AD,
               provide organization and location information.
            2. Fill in all the fields appropriately for AD.

        :expectedresults: Whether creating LDAP Auth with AD and
            associating org and loc is successful.

        :CaseImportance: Critical
        """
        with Session(self) as session:
            orgs = [entities.Organization().create().name]
            locations = [entities.Location().create().name]
            for server_name in generate_strings_list():
                with self.subTest(server_name):
                    make_ldapauth(
                        session,
                        name=server_name,
                        server=self.ldap_hostname,
                        server_type=LDAP_SERVER_TYPE['UI']['ad'],
                        login_name=LDAP_ATTR['login_ad'],
                        first_name=LDAP_ATTR['firstname'],
                        surname=LDAP_ATTR['surname'],
                        mail=LDAP_ATTR['mail'],
                        account_user=self.ldap_user_name,
                        account_passwd=self.ldap_user_passwd,
                        account_basedn=self.base_dn,
                        account_grpbasedn=self.group_base_dn,
                        orgs=orgs,
                        org_select=True,
                        locations=locations,
                        loc_select=True,
                    )
                    self.assertIsNotNone(
                        self.ldapauthsource.search(server_name)
                    )

    @tier2
    def test_positive_create_with_idm_org_and_loc(self):
        """Create LDAP auth_source for IDM with org and loc assigned.

        :id: bc70bcff-1241-4d8e-9713-da752d6c4798

        :steps:
            1. Create a new LDAP Auth source with IDM,
               provide organization and location information.
            2. Fill in all the fields appropriately for IDM.

        :expectedresults: Whether creating LDAP Auth source with IDM and
            associating org and loc is successful.

        :CaseImportance: Critical
        """
        with Session(self) as session:
            orgs = [entities.Organization().create().name]
            locations = [entities.Location().create().name]
            for server_name in generate_strings_list():
                with self.subTest(server_name):
                    make_ldapauth(
                        session,
                        name=server_name,
                        server=self.ldap_ipa_hostname,
                        server_type=LDAP_SERVER_TYPE['UI']['ipa'],
                        login_name=LDAP_ATTR['login'],
                        first_name=LDAP_ATTR['firstname'],
                        surname=LDAP_ATTR['surname'],
                        mail=LDAP_ATTR['mail'],
                        account_user=self.ldap_ipa_user_name,
                        account_passwd=self.ldap_ipa_user_passwd,
                        account_basedn=self.ipa_base_dn,
                        account_grpbasedn=self.ipa_group_base_dn,
                        orgs=orgs,
                        org_select=True,
                        locations=locations,
                        loc_select=True,
                    )
                    self.assertIsNotNone(
                        self.ldapauthsource.search(server_name)
                    )
