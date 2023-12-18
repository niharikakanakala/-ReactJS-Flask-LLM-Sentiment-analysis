import React, { useState } from 'react';
import axios from 'axios';
import { BASE_URL } from './constants';

const App = () => {
  const [sentence, setSentence] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(BASE_URL + "/predict", { sentences: [sentence] });
      setResults(response.data);
    } catch (error) {
      console.error('Error:', error);
      setResults({ error: 'Failed to get response.' }); // Set error message in state
    }
    setLoading(false);
  };
  

  return (
    <div style={{ textAlign: 'center', fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <h1 style={{ color: '#333' }}>Text Classifier</h1>
      <form onSubmit={handleSubmit} style={{ margin: '20px 0' }}>
        <input
          type="text"
          value={sentence}
          onChange={(e) => setSentence(e.target.value)}
          placeholder="Enter a sentence"
          style={{ padding: '10px', marginRight: '10px', width: '300px', borderRadius: '4px', border: '1px solid #ddd' }}
        />
        <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Classify
        </button>
      </form>
      {results && results.predictions && Array.isArray(results.predictions) && (
  <div style={{ marginTop: '20px' }}>
    <p><strong>Predictions:</strong> {results.predictions.join(', ')}</p>
    <p><strong>Accuracy:</strong> {results.accuracy}</p>
    {results && results.error && <p>Error: {results.error}</p>}
  </div>
)}

    </div>
  );
};

export default App;
