from .test_setup import TestSetup


class TestView(TestSetup):
    def test_user_cannot_register_without_complete_details(self):
        res = self.client.post(
            self.register_url, self.incomplete_registration_data, format='json')
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_register_with_bad_username(self):
        res = self.client.post(
            self.register_url, self.bad_username_registration_data, format='json')
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_with_complete_data(self):
        res = self.client.post(
            self.register_url, self.registration_data, format='json')
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_wrong_credentials(self):
        self.client.post(
            self.register_url, self.registration_data, format='json')
        final_res = self.client.post(
            self.login_url, self.bad_login_data, format='json')
        self.assertEqual(final_res.status_code, 401)

    def test_user_can_login_with_correct_credentials_and_receive_tokens(self):
        self.client.post(
            self.register_url, self.registration_data, format='json')
        final_res = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(final_res.status_code, 200)
        self.assertTrue('access' in final_res.data['data'])
