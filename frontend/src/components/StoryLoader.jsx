import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import StoryGame from './StoryGame';
import LoadingStatus from './LoadingStatus';

const API_BASE_URL = '/api';

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [story, setStory] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      loadStory(id);
    }
  }, [id]);

  const loadStory = async (storyId) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
      setStory(response.data);
      setIsLoading(false);
    } catch (err) {
      if (err.response?.status === 404) {
        setError(`Story with ID ${storyId} was not found.`);
      } else {
        setError(`Failed to load story: ${err.message}`);
      }
      setIsLoading(false);
    }
  };


  const createNewStory = () => {
    navigate('/');
  };


  if (isLoading) {
    return <LoadingStatus theme="story" />;
  }

  if (error) {
    return (
      <div className="story-loader">
        <div className="error-message">
          <h2>Story Not Found</h2>
          <p>{error}</p>
          <button onClick={createNewStory}>Go to Story Generator</button>
        </div>
      </div>
    );
  }

  if (story) {
    return (
      <div className="story-loader">

        <StoryGame story={story} onNewStory={createNewStory} />
      </div>
    );
  }

  return null;
}

export default StoryLoader; 