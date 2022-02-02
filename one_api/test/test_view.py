from .test_setup import TestSetup


class TestView(TestSetup):
    def test_unauthenticated_user_can_get_all_characters(self):
        res = self.client.get(self.get_character_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_unauthenticated_user_can_get_all_quotes(self):
        res = self.client.get(self.get_quote_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_unauthenticated_user_cannot_add_favorite_character(self):
        res = self.client.get(self.add_favorite_character, format="json")
        self.assertEqual(res.status_code, 401)

    def test_authenticated_user_can_add_favorite_character(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        res = self.client.post(self.add_favorite_character, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue('id' in res.data['data'])

    def test_authenticated_user_cannot_add_favorite_character_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        self.client.post(self.add_favorite_character, format="json")
        res = self.client.post(self.add_favorite_character, format="json")
        self.assertEqual(res.status_code, 409)

    def test_authenticated_user_can_add_favorite_quote(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        res = self.client.post(self.add_favorite_quote, format="json")
        quote = res.data['data']['quotes']
        self.assertEqual(res.status_code, 201)
        self.assertTrue('id' in res.data['data'])
        self.assertTrue(len(quote) > 0)

    def test_authenticated_user_can_get_favorite_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        self.client.post(self.add_favorite_quote, format="json")
        res = self.client.get(self.get_favourite_items, format="json")
        quote = res.data['data'][0]['quotes']
        self.assertEqual(res.status_code, 200)
        self.assertTrue('id' in res.data['data'][0])
        self.assertTrue(len(quote) > 0)
