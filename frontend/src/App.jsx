import { useMemo, useState } from 'react'
import axios from 'axios'
import Editor from '@monaco-editor/react'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000/api' })

export default function App() {
  const [database, setDatabase] = useState('postgres')
  const [question, setQuestion] = useState('')
  const [schema, setSchema] = useState('')
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const language = useMemo(() => (database === 'postgres' ? 'sql' : 'json'), [database])

  const generate = async () => {
    setLoading(true)
    setError('')
    setResults([])
    try {
      const { data } = await api.post('/generate-query/', { database, question })
      setSchema(data.schema)
      setQuery(data.generated_query)
    } catch (e) {
      setError(e.response?.data?.error || e.message)
    } finally {
      setLoading(false)
    }
  }

  const execute = async () => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.post('/execute-query/', { database, query })
      setResults(data.results || [])
    } catch (e) {
      setError(e.response?.data?.error || e.message)
    } finally {
      setLoading(false)
    }
  }

  const reject = () => {
    setQuery('')
    setResults([])
  }

  return (
    <div className="min-h-screen p-8 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-6">
        <nav className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl shadow-2xl">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-blue-300 bg-clip-text text-transparent">NLQ AI Query Engine</h1>
          <p className="text-slate-300">PostgreSQL & MongoDB Natural Language Intelligence</p>
        </nav>

        {error && <div className="rounded-xl border border-rose-400 bg-rose-500/10 p-3 text-rose-200">{error}</div>}

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl space-y-4">
            <h2 className="text-xl font-semibold">Ask in Natural Language</h2>
            <select
              className="w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2"
              value={database}
              onChange={(e) => setDatabase(e.target.value)}
            >
              <option value="postgres">PostgreSQL</option>
              <option value="mongo">MongoDB</option>
            </select>
            <textarea
              rows={4}
              className="w-full rounded-xl border border-slate-600 bg-slate-900 px-3 py-2 text-white"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. Show top 5 customers by total purchase"
            />
            <button onClick={generate} className="w-full rounded-xl bg-gradient-to-r from-purple-500 to-blue-500 px-4 py-3 font-semibold hover:opacity-90 transition">
              Generate Query
            </button>
          </div>

          <div className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl">
            <h2 className="text-xl font-semibold mb-3">Schema Snapshot</h2>
            <pre className="max-h-64 overflow-auto rounded-xl bg-slate-900/70 p-4 text-sm text-slate-200">{schema || 'Schema will appear here...'}</pre>
          </div>
        </section>

        <section className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl space-y-4">
          <h2 className="text-xl font-semibold">Generated Query (Editable)</h2>
          <Editor
            height="240px"
            language={language}
            theme="vs-dark"
            value={query}
            onChange={(value) => setQuery(value || '')}
          />
          <div className="flex gap-3">
            <button onClick={execute} className="rounded-xl bg-emerald-500 px-5 py-2 font-semibold hover:bg-emerald-400 transition">Execute</button>
            <button onClick={reject} className="rounded-xl bg-rose-500 px-5 py-2 font-semibold hover:bg-rose-400 transition">Reject</button>
            {loading && <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-300 border-t-transparent" />}
          </div>
        </section>

        <section className="rounded-2xl border border-white/20 bg-white/10 p-6 backdrop-blur-xl">
          <h2 className="text-xl font-semibold">Results</h2>
          <div className="mt-4 overflow-auto">
            <table className="min-w-full text-sm">
              <thead>
                <tr>
                  {results[0] && Object.keys(results[0]).map((key) => (
                    <th key={key} className="border-b border-slate-600 px-3 py-2 text-left">{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, idx) => (
                  <tr key={idx} className="hover:bg-white/10 transition">
                    {Object.values(row).map((value, i) => (
                      <td key={i} className="border-b border-slate-700 px-3 py-2">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
            {!results.length && <p className="text-slate-300">No results yet.</p>}
          </div>
        </section>
      </div>
    </div>
  )
}
