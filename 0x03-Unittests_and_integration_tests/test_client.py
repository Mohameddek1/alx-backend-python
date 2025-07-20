# #!/usr/bin/env python3
# """Unittests and integration tests for GithubOrgClient"""

# import unittest
# from unittest.mock import patch, PropertyMock, Mock
# from parameterized import parameterized, parameterized_class
# from client import GithubOrgClient
# from fixtures import (
#     org_payload,
#     repos_payload,
#     expected_repos,
#     apache2_repos,
# )


# class TestGithubOrgClient(unittest.TestCase):
#     """Unit tests for GithubOrgClient"""

#     @parameterized.expand([
#         ("google",),
#         ("abc",),
#     ])
#     @patch("client.get_json")
#     def test_org(self, org_name, mock_get_json):
#         """Test org method returns correct payload"""
#         mock_get_json.return_value = {"login": org_name}
#         client = GithubOrgClient(org_name)
#         self.assertEqual(client.org, {"login": org_name})
#         mock_get_json.assert_called_once_with(
#             f"https://api.github.com/orgs/{org_name}"
#         )

#     def test_public_repos_url(self):
#         """Test that _public_repos_url returns the correct repos_url"""
#         with patch(
#             "client.GithubOrgClient.org",
#             new_callable=PropertyMock
#         ) as mock_org:
#             mock_org.return_value = {
#                 "repos_url": "https://api.github.com/orgs/test/repos"
#             }
#             client = GithubOrgClient("test")
#             self.assertEqual(
#                 client._public_repos_url,
#                 "https://api.github.com/orgs/test/repos"
#             )
#             mock_org.assert_called_once()

#     @patch("client.get_json")
#     def test_public_repos(self, mock_get_json):
#         """Test that public_repos returns correct repo names"""
#         mock_get_json.return_value = [
#             {"name": "r1"},
#             {"name": "r2"}
#         ]
#         with patch(
#             "client.GithubOrgClient._public_repos_url",
#             new_callable=PropertyMock
#         ) as mock_url:
#             mock_url.return_value = "https://api/repos"
#             client = GithubOrgClient("test")
#             self.assertEqual(client.public_repos(), ["r1", "r2"])
#             mock_get_json.assert_called_once_with("https://api/repos")

#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, key, expected):
#         """Test that has_license returns correct boolean"""
#         self.assertEqual(GithubOrgClient.has_license(repo, key), expected)


# @parameterized_class([
#     {
#         "org_payload": org_payload,
#         "repos_payload": repos_payload,
#         "expected_repos": expected_repos,
#         "apache2_repos": apache2_repos,
#     }
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration tests for GithubOrgClient"""

#     @classmethod
#     def setUpClass(cls):
#         """Set up class-wide mocks"""
#         cls.get_patcher = patch("requests.get")
#         cls.mock_get = cls.get_patcher.start()

#         cls.mock_get.side_effect = [
#             Mock(json=lambda: cls.org_payload),
#             Mock(json=lambda: cls.repos_payload),
#         ]

#     @classmethod
#     def tearDownClass(cls):
#         """Tear down patcher"""
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Integration test for public_repos"""
#         client = GithubOrgClient(self.org_payload["login"])
#         self.assertEqual(client.public_repos(), self.expected_repos)

#     def test_public_repos_with_license(self):
#         """Integration test for public_repos with license filtering"""
#         client = GithubOrgClient(self.org_payload["login"])
#         self.assertEqual(
#             client.public_repos(license="apache-2.0"),
#             self.apache2_repos
#         )


# if __name__ == "__main__":
#     unittest.main()

#!/usr/bin/env python3
# """Integration test for GithubOrgClient.public_repos method."""

# import unittest
# from unittest.mock import patch, Mock
# from parameterized import parameterized_class
# from fixtures import TEST_PAYLOAD
# from client import GithubOrgClient


# @parameterized_class([
#     {
#         "org_payload": TEST_PAYLOAD[0][0],
#         "repos_payload": TEST_PAYLOAD[0][1],
#         "expected_repos": TEST_PAYLOAD[0][2],
#         "apache2_repos": TEST_PAYLOAD[0][3]
#     }
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration test class for GithubOrgClient.public_repos."""

#     @classmethod
#     def setUpClass(cls):
#         """Set up class method to mock requests.get with fixtures."""
#         cls.get_patcher = patch('requests.get')
#         cls.mock_get = cls.get_patcher.start()

#         def get_json_side_effect(url):
#             """Side effect for requests.get().json() based on URL."""
#             if url == "https://api.github.com/orgs/google":
#                 return cls.org_payload
#             elif url == "https://api.github.com/orgs/google/repos":
#                 return cls.repos_payload
#             return None

#         cls.mock_get.side_effect = lambda url: Mock(json=lambda: get_json_side_effect(url))

#     @classmethod
#     def tearDownClass(cls):
#         """Tear down class method to stop the patcher."""
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Test public_repos without license filter."""
#         client = GithubOrgClient("google")
#         repos = client.public_repos()
#         self.assertEqual(repos, self.expected_repos)

#     def test_public_repos_with_license(self):
#         """Test public_repos with Apache 2.0 license filter."""
#         client = GithubOrgClient("google")
#         repos = client.public_repos(license="apache-2.0")
#         self.assertEqual(repos, self.apache2_repos)


# if __name__ == "__main__":
#     unittest.main()

#!/usr/bin/env python3
"""Unit test for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get and provide side effects"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Setup side_effect for different endpoints
        def side_effect(url):
            if url.endswith('/orgs/google'):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url.endswith('/orgs/google/repos'):
                mock_resp = unittest.mock.Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos returns only repos with given license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
        
if __name__ == "__main__":
    unittest.main()