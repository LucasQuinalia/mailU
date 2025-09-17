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
      <div className='page'>
        <div className='footer'>
            <p>Made with &lt;3 by <a href="https://linktr.ee/lucasquinalia">Lucas Quinália</a> for <a href="https://www.autou.io/">AutoU</a></p>
        </div>
      </div>
    </div>
  )
}

export default App
