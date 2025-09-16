import React, { useState } from 'react'
import UploadForm from './components/UploadForm'
import ResultDisplay from './components/ResultDisplay'
import './styles/App.css'

function App() {
  const [result, setResult] = useState(null)

  const handleNewAnalysis = () => {
    setResult(null)
  }

  return (
    <div className="app">
      <UploadForm setResult={setResult} />
      {result && <ResultDisplay result={result} onNewAnalysis={handleNewAnalysis} />}
    </div>
  )
}

export default App
