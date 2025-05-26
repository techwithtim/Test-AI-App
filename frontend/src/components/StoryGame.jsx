import { useState, useEffect } from 'react';

function StoryGame({ story, onNewStory }) {
  const [currentNodeId, setCurrentNodeId] = useState(null);
  const [currentNode, setCurrentNode] = useState(null);
  const [options, setOptions] = useState([]);
  const [isEnding, setIsEnding] = useState(false);
  const [isWinningEnding, setIsWinningEnding] = useState(false);

  // Initialize the game with the root node
  useEffect(() => {
    if (story && story.root_node) {
      const rootNodeId = story.root_node.id;
      setCurrentNodeId(rootNodeId);
    }
  }, [story]);

  // Update the current node and options when the node ID changes
  useEffect(() => {
    if (currentNodeId && story && story.all_nodes) {
      const node = story.all_nodes[currentNodeId];
      
      setCurrentNode(node);
      setIsEnding(node.is_ending);
      setIsWinningEnding(node.is_winning_ending);
      
      // Use the actual options defined in the node
      if (!node.is_ending && node.options && node.options.length > 0) {
        setOptions(node.options);
      } else {
        setOptions([]);
      }
    }
  }, [currentNodeId, story]);

  // Choose an option and advance to that node
  const chooseOption = (nextNodeId) => {
    // Move to the next node
    setCurrentNodeId(nextNodeId);
  };

  // Restart the current story from the beginning
  const restartStory = () => {
    if (story && story.root_node) {
      setCurrentNodeId(story.root_node.id);
    }
  };

  return (
    <div className="story-game">
      <header className="story-header">
        <h2>{story.title}</h2>
      </header>

      <div className="story-content">
        {currentNode && (
          <div className="story-node">
            <p>{currentNode.content}</p>
            
            {isEnding ? (
              <div className="story-ending">
                <h3>{isWinningEnding ? 'Congratulations!' : 'The End'}</h3>
                <p className={isWinningEnding ? 'winning-message' : 'ending-message'}>
                  {isWinningEnding 
                    ? 'You reached a winning ending!' 
                    : 'Your adventure has come to an end.'}
                </p>
              </div>
            ) : (
              <div className="story-options">
                <h3>What will you do?</h3>
                <div className="options-list">
                  {options.map((option, index) => (
                    <button
                      key={index}
                      onClick={() => chooseOption(option.node_id)}
                      className="option-btn"
                    >
                      {option.text}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="story-controls">
        <button onClick={restartStory} className="reset-btn">
          🔄 Restart Story
        </button>
        
        {onNewStory && (
          <button onClick={onNewStory} className="new-story-btn">
            ✨ New Story
          </button>
        )}
      </div>
    </div>
  );
}

export default StoryGame; 