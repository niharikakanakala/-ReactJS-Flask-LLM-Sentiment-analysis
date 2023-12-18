import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from './src/App';

jest.mock('axios');

describe('App component tests', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByPlaceholderText('Enter a sentence')).toBeInTheDocument;
    expect(screen.getByText('Classify')).toBeInTheDocument;
  });

  test('input field updates on user input', () => {
    render(<App />);
    const inputField = screen.getByPlaceholderText('Enter a sentence');
    fireEvent.change(inputField, { target: { value: 'Test sentence' } });
    expect(inputField.value).toBe('Test sentence');
  });
});

test('submits form and displays results', async () => {
  axios.post.mockResolvedValue({
    data: {
      predictions: ['positive'],
      accuracy: 0.9
    }
  });

  render(<App />);
  fireEvent.change(screen.getByPlaceholderText('Enter a sentence'), { target: { value: 'Great product' } });
  fireEvent.click(screen.getByText('Classify'));

  await waitFor(() => {
    expect(screen.getByText(/Predictions:/i)).toBeInTheDocument;
    expect(screen.getByText(/positive/i)).toBeInTheDocument;
    expect(screen.getByText(/Accuracy:/i)).toBeInTheDocument;
    expect(screen.getByText(/0.9/i)).toBeInTheDocument;
  });
});


test('handles API error', async () => {
  // Mock the API call to reject with an error
  axios.post.mockRejectedValue(new Error('API Error'));

  // Render the component
  render(<App />);

  // Simulate user input and form submission
  fireEvent.change(screen.getByPlaceholderText('Enter a sentence'), { target: { value: 'Test' } });
  fireEvent.click(screen.getByText('Classify'));

  // Wait for the error message to appear and assert its presence
  await waitFor(() => {
    const errorMessage = screen.queryByText('Error: Failed to get response.');
    expect(errorMessage).toBeInTheDocument;
  });
});

