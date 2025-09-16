import React from 'react'

function ResultDisplay({ result, onNewAnalysis }) {
  if (!result) return null

  const { 
    text, 
    classification, 
    auto_response, 
    confidence = 0,
    nlp_analysis = {}
  } = result

  const isProductive = classification === 'produtivo'

  return (
    <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ccc' }}>
      <h2>Resultado da Análise</h2>
      
      <div style={{ marginBottom: '15px' }}>
        <strong>Classificação:</strong> 
        <span style={{ 
          color: isProductive ? 'green' : 'red', 
          marginLeft: '10px',
          fontWeight: 'bold'
        }}>
          {isProductive ? '✅ Produtivo' : '❌ Improdutivo'}
        </span>
        <span style={{ marginLeft: '10px' }}>
          ({confidence.toFixed(0)}% confiança)
        </span>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <strong>Texto analisado:</strong>
        <div style={{ 
          marginTop: '5px', 
          padding: '10px', 
          backgroundColor: '#f5f5f5',
          maxHeight: '150px',
          overflow: 'auto'
        }}>
          {text.length > 200 ? `${text.substring(0, 200)}...` : text}
        </div>
      </div>

      <div style={{ marginBottom: '15px' }}>
        <strong>Resposta sugerida:</strong>
        <div style={{ 
          marginTop: '5px', 
          padding: '10px', 
          backgroundColor: '#e8f4fd',
          border: '1px solid #bee5eb'
        }}>
          {auto_response}
        </div>
      </div>

      {nlp_analysis && Object.keys(nlp_analysis).length > 0 && (
        <div style={{ marginBottom: '15px' }}>
          <strong>Análise NLP:</strong>
          <div style={{ marginTop: '5px', fontSize: '14px' }}>
            <div>Palavras: {nlp_analysis.word_count || 0}</div>
            <div>Palavras únicas: {nlp_analysis.unique_words || 0}</div>
            {nlp_analysis.stemmed && (
              <div>Stemmed: {nlp_analysis.stemmed.slice(0, 10).join(', ')}...</div>
            )}
          </div>
        </div>
      )}

      <button 
        onClick={onNewAnalysis}
        style={{ 
          padding: '10px 20px', 
          backgroundColor: '#007bff', 
          color: 'white', 
          border: 'none',
          cursor: 'pointer'
        }}
      >
        Nova Análise
      </button>
    </div>
  )
}

export default ResultDisplay