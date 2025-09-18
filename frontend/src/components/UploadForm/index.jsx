import React, { useState, useRef } from 'react'
import './upload-form.css'

export default function UploadForm({ setResult }) {
  const [file, setFile] = useState(null)
  const [text, setText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const textareaRef = useRef(null)

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setText("")
    }
  }

  const removeFile = () => {
    setFile(null)
    const fileInput = document.querySelector('input[type="file"]')
    if (fileInput) {
      fileInput.value = ""
    }
  }

  const handleTextChange = (e) => {
    setText(e.target.value)

    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = "auto"
      textarea.style.height = textarea.scrollHeight + "px"
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file && !text.trim()) {
      setError("Por favor, envie um arquivo ou digite um texto")
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    if (file) formData.append("file", file)
    if (text.trim()) formData.append("text", text.trim())

    try {
      const apiUrl = import.meta.env.VITE_API_URL;
      const res = await fetch(`${apiUrl}/classify`, {
        method: "POST",
        body: formData
      })
      if (!res.ok) {
        const errorText = await res.text()
        throw new Error(`Erro na requisição: ${res.status} - ${errorText}`)
      }
      const data = await res.json()
      if (data.error) throw new Error(data.error)
      setResult(data)
    } catch (err) {
      setError("Erro ao enviar: " + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className='page'>
      <div className='color-square square-left'></div>
      <div className='color-square square-right'></div>
      <div className="upload-container">
        <div className="logo">
          <img src="/logo.png" alt="mailU logo"/>
        </div>

        <h1 className="lema">Classifique rapidamente e-mails, gere respostas automáticas e poupe seu precioso tempo.</h1>
        
        <form onSubmit={handleSubmit} className='form'>
          <div>
            <label className="file-upload">
              <input 
                type="file"
                accept=".txt,.pdf"
                onChange={handleFileChange}
                style={{ display: 'none' }}
                id="file-input"/>
              <span>
                <img src="/paperclip.png" alt="ícone" />
                {file ? file.name : "Carregar arquivo .pdf ou .txt"}
              </span>
            </label>
            {file && (
              <div style={{ 
                marginTop: '10px', 
                padding: '8px', 
                background: '#f0f0f0', 
                borderRadius: '4px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span style={{ fontSize: '14px', color: '#666' }}>
                  📄 {file.name} ({(file.size / 1024).toFixed(1)} KB)
                </span>
                <button 
                  type="button" 
                  onClick={removeFile}
                  style={{ 
                    background: '#ff4444', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '3px', 
                    padding: '4px 8px',
                    cursor: 'pointer',
                    fontSize: '12px'
                  }}
                >
                  ✕ Remover
                </button>
              </div>
            )}
          </div>
          
          <div>
            <textarea
              placeholder={file ? "Arquivo selecionado! Você pode adicionar texto adicional aqui se quiser..." : "Ou cole o texto do e-mail aqui..."}
              value={text}
              onChange={handleTextChange}
              className='input-text'
              rows={12}
              ref={textareaRef}
            />
          </div>

          {error && (
            <div style={{ color: 'red', margin: '10px 0' }}>
              {error}
            </div>
          )}

          <div className='button-container'>
            <button 
              type="submit" 
              disabled={loading || (!file && !text.trim())}
              className='button'
            >
              {loading ? 'Processando...' : 'Classificar e-mail e gerar resposta'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}