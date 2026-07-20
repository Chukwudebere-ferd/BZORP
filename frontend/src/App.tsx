import { useState, useEffect } from 'react'
import './App.css'

interface Email {
  id: string
  subject: string
  from: string
  date: string
}

const GoogleLogo = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M19.6 10.227c0-.71-.064-1.392-.18-2.045H10v3.866h5.38a4.597 4.597 0 0 1-1.996 3.018v2.508h3.234c1.892-1.742 2.982-4.305 2.982-7.347z" fill="#4285F4"/>
    <path d="M10 20c2.7 0 4.964-.895 6.618-2.424l-3.234-2.508c-.896.6-2.042.955-3.384.955-2.603 0-4.806-1.758-5.592-4.12H1.07v2.59A9.998 9.998 0 0 0 10 20z" fill="#34A853"/>
    <path d="M4.408 11.903A5.994 5.994 0 0 1 4.09 10c0-.656.112-1.294.318-1.903V5.507H1.07A9.985 9.985 0 0 0 0 10c0 1.614.387 3.14 1.07 4.493l3.338-2.59z" fill="#FBBC05"/>
    <path d="M10 3.98c1.468 0 2.786.505 3.824 1.496l2.868-2.868C14.96.67 12.695 0 10 0 6.087 0 2.752 2.24 1.07 5.507l3.338 2.59C5.194 5.738 7.397 3.98 10 3.98z" fill="#EA4335"/>
  </svg>
)

function getStatus(): { connected: boolean; email: string; telegramId: string } {
  const params = new URLSearchParams(window.location.search)
  const status = params.get('status')
  const email = params.get('email') || ''
  const telegramId = params.get('telegram_id') || ''
  return { connected: status === 'connected', email, telegramId }
}

function App() {
  const [telegramId, setTelegramId] = useState('')
  const [connecting, setConnecting] = useState(false)
  const [error, setError] = useState('')
  const [emails, setEmails] = useState<Email[]>([])
  const [loadingEmails, setLoadingEmails] = useState(false)
  const [emailCount, setEmailCount] = useState(0)

  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')
  const state = params.get('state')

  const { connected, email: connectedEmail, telegramId: connectedTid } = getStatus()

  useEffect(() => {
    if (connected && connectedTid) {
      setLoadingEmails(true)
      fetch(`/api/gmail/emails?telegram_id=${encodeURIComponent(connectedTid)}`)
        .then((r) => r.json())
        .then((data) => {
          setEmails(data.emails || [])
          setEmailCount(data.email_count || 0)
        })
        .catch(() => setError('Failed to load emails'))
        .finally(() => setLoadingEmails(false))
    }
  }, [connected, connectedTid])

  const handleConnect = async () => {
    setError('')
    if (!telegramId.trim()) {
      setError('Please enter your Telegram ID')
      return
    }
    setConnecting(true)
    try {
      const res = await fetch(`/api/auth/google/login?telegram_id=${encodeURIComponent(telegramId.trim())}`)
      const data = await res.json()
      if (data.auth_url) {
        window.location.href = data.auth_url
      } else {
        setError('Failed to get authentication URL')
        setConnecting(false)
      }
    } catch {
      setError('Failed to connect. Please try again.')
      setConnecting(false)
    }
  }

  if (code && state) {
    return (
      <div className="auth-card">
        <div className="connecting-message">
          <div className="spinner" />
          <p>Connecting your Gmail account…<br />Please wait.</p>
        </div>
      </div>
    )
  }

  if (connected) {
    return (
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Bzorp</h1>
          <div className="connected-badge">
            <span className="dot" />
            {connectedEmail}
          </div>
        </div>

        <div className="dashboard-card">
          <h2>Recent Emails</h2>
          <p className="dashboard-subtitle">Last 24 hours &middot; {emailCount} emails</p>

          {loadingEmails ? (
            <div className="connecting-message">
              <div className="spinner" />
              <p>Loading emails…</p>
            </div>
          ) : emails.length === 0 ? (
            <p className="empty-state">No emails in the last 24 hours.</p>
          ) : (
            <div className="email-list">
              {emails.map((e) => (
                <div key={e.id} className="email-item">
                  <div className="email-from">{e.from}</div>
                  <div className="email-subject">{e.subject}</div>
                  <div className="email-date">{e.date}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="auth-card">
      <h1 className="auth-title">Sign in</h1>
      <p className="auth-subtitle">Connect your Gmail to get daily email summaries on Telegram.</p>

      <div className="form-group">
        <label htmlFor="telegramId" className="form-label">Telegram ID</label>
        <input
          type="text"
          id="telegramId"
          className={`form-input${error ? ' error' : ''}`}
          placeholder="Enter your Telegram ID"
          value={telegramId}
          onChange={(e) => { setTelegramId(e.target.value); setError('') }}
          onKeyDown={(e) => e.key === 'Enter' && handleConnect()}
          disabled={connecting}
          autoFocus
        />
        {error && <div className="form-error">{error}</div>}
      </div>

      <button
        className={`btn-google${connecting ? ' btn-connecting' : ''}`}
        onClick={handleConnect}
        disabled={connecting}
      >
        {connecting ? (
          <div className="spinner" />
        ) : (
          <GoogleLogo />
        )}
        {connecting ? 'Connecting…' : 'Connect Gmail'}
      </button>
    </div>
  )
}

export default App
