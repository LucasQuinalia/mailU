import React, { useState, useRef, useEffect } from 'react'
import confetti from 'canvas-confetti'
import './result-display.css'

export default function ResultDisplay({ result, onNewAnalysis }) {
  if (!result) return null

  const { classification, auto_response } = result
  const isProductive = classification === 'produtivo'

  const [copied, setCopied] = useState(false)
  const timeoutRef = useRef(null)

  useEffect(() => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
    })
  }, [result])

  const handleCopy = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!auto_response) return

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(auto_response)
        setCopied(true)
        timeoutRef.current = setTimeout(() => setCopied(false), 2000)
      } else {
        const textArea = document.createElement('textarea')
        textArea.value = auto_response
        textArea.className = 'temp-copy-textarea'
        document.body.appendChild(textArea)
        textArea.focus()
        textArea.select()
        
        try {
          document.execCommand('copy')
          setCopied(true)
          timeoutRef.current = setTimeout(() => setCopied(false), 2000)
        } catch (err) {
          console.error('Failed to copy text: ', err)
        } finally {
          document.body.removeChild(textArea)
        }
      }
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current)
    }
  }, [])

  return (
    <div className='form'>
      <div>
        <p className='subtitle'>
          Classificação:
          <span className={`classification ${isProductive ? 'productive' : 'unproductive'}`}>
            {isProductive ? ' Produtivo' : ' Improdutivo'}
          </span>
        </p>
      </div>

      <p className='subtitle'>Resposta sugerida:</p>

      <div className='response-container'>
        <div className='copy'>
          <button
            type="button"
            onClick={handleCopy}
            className='button-copy'
            disabled={copied}
            title={copied ? 'Resposta copiada!' : 'Clique para copiar a resposta'}
          >
            <img src="/copy.png" alt="ícone" className='copy-icon'/>
            {copied ? 'Resposta copiada!' : 'Copiar resposta'}
          </button>
        </div>
        <div className='input-text'>
          {auto_response}
        </div>
      </div>

      <div className='button-container'>
        <button
          onClick={onNewAnalysis}
          className='button button-new-analysis'
        >
          Nova Análise
        </button>
      </div>
    </div>
  )
}