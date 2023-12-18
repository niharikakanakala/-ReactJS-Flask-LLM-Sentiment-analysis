import unittest
from main import app

class FlaskTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_success(self):
        response = self.app.post('/predict', json={'sentences': ['I love this!', 'I hate that!']})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('predictions', data)
        self.assertIn('accuracy', data)
        self.assertIsInstance(data['predictions'], list)
        self.assertIsInstance(data['accuracy'], float)

    def test_predict_no_data(self):
        response = self.app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)

    def test_predict_missing_sentences(self):
        response = self.app.post('/predict', json={'wrong_key': 'test'})
        self.assertEqual(response.status_code, 400)

    def test_predict_invalid_data_type(self):
        response = self.app.post('/predict', json={'sentences': 'Not a list'})
        self.assertEqual(response.status_code, 400)

    def test_predict_empty_sentence_list(self):
        response = self.app.post('/predict', json={'sentences': []})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['predictions']), 0)

if __name__ == '__main__':
    unittest.main()
