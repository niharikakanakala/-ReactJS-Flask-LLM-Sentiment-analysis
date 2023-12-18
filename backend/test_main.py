import unittest
from main import main
import numpy as np

class TestSentimentAnalysis(unittest.TestCase):

    def test_accuracy(self):
        
        data = main(["I love this product"])
        self.assertTrue(isinstance(data[1], np.float64))
        self.assertTrue(data[1] > 0.5)

    def test_sentiment_prediction(self):
        # Test sentiment prediction for specific sentences
        test_cases = [
            {"sentence": "I love dancing", "expected_sentiment": 'positive'},
            {"sentence": "This is terrible", "expected_sentiment": 'negative'},
            # Add more test cases as needed
        ]

        for test_case in test_cases:
            new_sentences = [test_case["sentence"]]
            predictions = main(new_sentences)
            # print(predictions[0])
            self.assertEqual(predictions[0], test_case["expected_sentiment"])


    def test_sentiment_prediction_2(self):
       
        sentences = ['I am a bad person', 'I am lazy']
        predictions = main(sentences)
        expected_predictions = ['negative', 'negative']
        self.assertListEqual(predictions[0].tolist(), expected_predictions)


    def test_sentiment_prediction_3(self):
       
        sentences = ['I love this car!', 'The weather is bad', 'I regret not studying']
        predictions = main(sentences)
        expected_predictions = ['positive', 'negative', 'negative']
        self.assertListEqual(predictions[0].tolist(), expected_predictions)

     # Test case for missing data
    def test_predict_no_data(self):
        tester = main.test_client(self)
        response = tester.post('/predict', json={})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
