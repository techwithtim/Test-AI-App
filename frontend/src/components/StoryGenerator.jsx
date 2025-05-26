import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import ThemeInput from './ThemeInput';
import LoadingStatus from './LoadingStatus';

const API_BASE_URL = '/api';

function StoryGenerator() {
  const navigate = useNavigate();
  const [theme, setTheme] = useState('');
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Effect to handle polling when we have a jobId
  useEffect(() => {
    let pollInterval;
    
    if (jobId && jobStatus === 'processing') {
      pollInterval = setInterval(() => {
        pollJobStatus(jobId);
      }, 5000);
    }

    // Cleanup function
    return () => {
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [jobId, jobStatus]);

  // Create a new story with the given theme
  const generateStory = async (theme) => {
    setIsLoading(true);
    setError(null);
    setTheme(theme);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/stories/create`, { theme });
      const { job_id, status } = response.data;
      setJobId(job_id);
      setJobStatus(status || 'processing');
      
      // Start polling immediately
      pollJobStatus(job_id);
    } catch (err) {
      setError(`Failed to create story: ${err.message}`);
      setIsLoading(false);
    }
  };

  // Poll the job status until it's completed
  const pollJobStatus = async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs/${id}`);
      const { status, story_id, error: jobError } = response.data;
      setJobStatus(status);
      
      if (status === 'completed' && story_id) {
        fetchStory(story_id);
      } else if (status === 'failed' || jobError) {
        setError(jobError || 'Story generation failed. Please try again.');
        setIsLoading(false);
      }
      // If status is 'processing', the useEffect will handle the next poll
    } catch (err) {
      // Don't immediately fail on polling errors, retry a few times
      if (err.response?.status !== 404) {
        setError(`Failed to check story status: ${err.message}`);
        setIsLoading(false);
      }
    }
  };

  // Fetch the complete story
  const fetchStory = async (id) => {
    try {
      setIsLoading(false);
      setJobStatus('completed');
      navigate(`/story/${id}`);
    } catch (err) {
      setError(`Failed to load the story: ${err.message}`);
      setIsLoading(false);
    }
  };

  // Reset the game to start over
  const resetGame = () => {
    setJobId(null);
    setJobStatus(null);
    setError(null);
    setTheme('');
    setIsLoading(false);
  };

  return (
    <div className="story-generator">
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={resetGame}>Try Again</button>
        </div>
      )}

      {!jobId && !error && !isLoading && (
        <ThemeInput onSubmit={generateStory} />
      )}

      {isLoading && (
        <LoadingStatus theme={theme} />
      )}
    </div>
  );
}

export default StoryGenerator; 