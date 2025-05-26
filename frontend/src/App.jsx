import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css'
import StoryGenerator from './components/StoryGenerator'
import StoryLoader from './components/StoryLoader'

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>Interactive Story Generator</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<StoryGenerator />} />
            <Route path="/story/:id" element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
