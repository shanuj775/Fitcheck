import { useState } from "react"

// Use environment variable for backend URL, fallback to empty string for local dev
const BACKEND_URL = import.meta.env.VITE_API_URL || ""

function statusStyle(status) {
  if (status === "Verified") return "status verified"
  if (status === "Inaccurate") return "status inaccurate"
  if (status === "False") return "status false"
  return "status"
}

function App() {
  const [file, setFile] = useState(null)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")
  const [uploaded, setUploaded] = useState(false)
  const [kbText, setKbText] = useState("")
  const [kbLoading, setKbLoading] = useState(false)
  const [kbStatus, setKbStatus] = useState("")

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!file) {
      setMessage("Please select a PDF file before uploading.")
      return
    }

    setLoading(true)
    setMessage("")
    setResults([])

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${BACKEND_URL}/factcheck`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Failed to process PDF.")
      }

      const data = await response.json()
      setResults(data.results)
      if (!data.results.length) {
        setMessage("No claims were extracted from the PDF.")
      }
      // Show upload success confirmation
      setUploaded(true)
      setMessage("File is uploaded successfully.")
    } catch (error) {
      setMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  const downloadCsv = () => {
    if (!results.length) return

    const csvRows = [
      ["Claim", "Status", "Confidence", "Evidence", "Source"],
      ...results.map((item) => [
        item.claim,
        item.status,
        item.confidence,
        item.evidence,
        item.source,
      ]),
    ]

    const csvContent = csvRows
      .map((row) => row.map((value) => `"${String(value).replace(/"/g, '""')}"`).join(","))
      .join("\n")

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = "factcheck_report.csv"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const loadKB = async () => {
    setKbLoading(true)
    setKbStatus("")
    try {
      const res = await fetch(`${BACKEND_URL}/kb`)
      if (!res.ok) throw new Error("Failed to load KB")
      const data = await res.json()
      setKbText(JSON.stringify(data, null, 2))
      setKbStatus("Loaded")
    } catch (err) {
      setKbStatus("Error loading KB")
    } finally {
      setKbLoading(false)
    }
  }

  const saveKB = async () => {
    setKbLoading(true)
    setKbStatus("")
    try {
      const parsed = JSON.parse(kbText)
      const res = await fetch(`${BACKEND_URL}/kb`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed),
      })
      if (!res.ok) throw new Error("Failed to save KB")
      const data = await res.json()
      setKbStatus(`Saved (${data.count} entries)`)
    } catch (err) {
      setKbStatus("Error saving KB: " + (err.message || err))
    } finally {
      setKbLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header>
        <h1>🛡️ TruthLayer AI</h1>
        <p>Upload a PDF and get AI-powered claim extraction plus live verification.</p>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="upload-form">
          <label className="file-label">
            <span>Select PDF</span>
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => {
                const f = event.target.files[0] ?? null
                setFile(f)
                if (f) {
                  setUploaded(true)
                  setMessage('File is uploaded successfully.')
                } else {
                  setUploaded(false)
                }
              }}
            />
            {file && (
              <div className="file-info fade-in">
                <span className="file-name">{file.name}</span>
                <span className="checkmark" aria-hidden>
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="11" stroke="#16a34a" strokeWidth="2" fill="#16a34a" fillOpacity="0.12" />
                    <path d="M7 12.5l2.5 2.5L17 8" stroke="#047857" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </span>
              </div>
            )}
          </label>

          <button type="submit" disabled={loading}>
            {loading ? "Processing PDF..." : "Upload and Fact Check"}
          </button>
        </form>

        <section style={{ marginTop: 18 }}>
          <h3>Local Knowledge Base</h3>
          <div style={{ display: 'flex', gap: 12, marginBottom: 8, alignItems: 'center' }}>
            <button type="button" onClick={loadKB} disabled={kbLoading}>Load KB</button>
            <button type="button" onClick={saveKB} disabled={kbLoading}>Save KB</button>
            <span style={{ color: '#374151' }}>{kbStatus}</span>
          </div>
          <textarea value={kbText} onChange={(e) => setKbText(e.target.value)} rows={8} style={{ width: '100%', fontFamily: 'monospace', fontSize: 13 }} />
          <small style={{ color: '#6b7280' }}>KB entries must be a JSON array of objects with keys: claim, evidence, source.</small>
        </section>

        {message && <div className="message">{message}</div>}

        {results.length > 0 && (
          <section className="results-section">
            <div className="results-header">
              <h2>Fact Check Report</h2>
              <button type="button" onClick={downloadCsv}>
                Download CSV
              </button>
            </div>
            <div className="results-table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Claim</th>
                    <th>Status</th>
                    <th>Confidence</th>
                    <th>Evidence</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((item, index) => (
                    <tr key={index}>
                      <td>{item.claim}</td>
                      <td className={statusStyle(item.status)}>{item.status}</td>
                      <td>{item.confidence}</td>
                      <td>{item.evidence}</td>
                      <td>
                        <a href={item.source} target="_blank" rel="noreferrer">
                          Link
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
