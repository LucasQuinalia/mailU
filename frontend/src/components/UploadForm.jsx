import React, { useState } from 'react'

function UploadForm({ setResult }) {
  const [file, setFile] = useState(null)
  const [text, setText] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setText("")
    }
  }

  const handleTextChange = (e) => {
    setText(e.target.value)
    if (e.target.value) {
      setFile(null)
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
    if (file) {
      formData.append("file", file)
    }
    if (text.trim()) {
      formData.append("text", text.trim())
    }

    try {
      const res = await fetch("http://localhost:8000/email/classify", {
        method: "POST",
        body: formData
      })

      if (!res.ok) {
        const errorText = await res.text()
        throw new Error(`Erro na requisição: ${res.status} - ${errorText}`)
      }

      const data = await res.json()
      
      if (data.error) {
        throw new Error(data.error)
      }
      
      setResult(data)
    } catch (err) {
      setError("Erro ao enviar: " + err.message)
    } finally {
      setLoading(false)
    }
  }

  const clearForm = () => {
    setFile(null)
    setText("")
    setError(null)
  }

  return (
    <div className="upload-container">
      <h1>mailU - Classificador de E-mails</h1>
      
      <form onSubmit={handleSubmit}>
        <div>
          <input
            type="file"
            accept=".txt,.pdf"
            onChange={handleFileChange}
          />
        </div>
        
        <div>
          <textarea
            placeholder="Ou cole o texto do e-mail aqui..."
            value={text}
            onChange={handleTextChange}
            rows={6}
            style={{ width: '100%', marginTop: '10px' }}
          />
        </div>

        {error && (
          <div style={{ color: 'red', margin: '10px 0' }}>
            {error}
          </div>
        )}

        <div>
          <button 
            type="button" 
            onClick={clearForm}
            disabled={loading}
            style={{ marginRight: '10px' }}
          >
            Limpar
          </button>
          <button 
            type="submit" 
            disabled={loading || (!file && !text.trim())}
          >
            {loading ? 'Processando...' : 'Classificar'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default UploadForm
