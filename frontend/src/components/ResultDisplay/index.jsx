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

  const handleCopy = async () => {
    if (!auto_response) return

    if (!navigator.clipboard) {
      const el = document.createElement('textarea')
      el.value = auto_response
      document.body.appendChild(el)
      el.select()
      try {
        document.execCommand('copy')
        setCopied(true)
        timeoutRef.current = setTimeout(() => setCopied(false), 2000)
      } catch (err) {
        console.error('Fallback copy failed', err)
      } finally {
        document.body.removeChild(el)
      }
      return
    }

    try {
      await navigator.clipboard.writeText(auto_response)
      setCopied(true)
      timeoutRef.current = setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Erro ao copiar:', err)
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
          <img src="/copy.png" alt="ícone" className='copy-icon'/>
          <button
            onClick={handleCopy}
            className='button-copy'
            disabled={copied}
          >
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