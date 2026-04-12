import { useState } from 'react'
import client from '../../api/client'

function News() {
    const [query, setQuery] = useState('')
    const [news, setNews] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const fetchNews = async () => {
        if (!query) return
        setLoading(true)
        setError('')
        try {
            const res = await client.post('/chat/', {
                query: `Найди последние новости про ${query} и объясни как они влияют на цену акции`,
                thread_id: null,
            })
            setNews([{ content: res.data.response }])
        } catch (e) {
            setError('Ошибка при получении новостей')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="bg-gray-900 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white">Новости и AI анализ</h2>

            <div className="flex gap-3">
                <input
                    placeholder="Компания или тикер (삼성전자, 005930)"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                    onClick={fetchNews}
                    disabled={loading}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                    {loading ? 'Поиск...' : 'Найти'}
                </button>
            </div>

            {error && <p className="text-red-400 text-sm">{error}</p>}

            {news.length > 0 && (
                <div className="bg-gray-800 rounded-xl p-5">
                    <p className="text-gray-100 text-sm whitespace-pre-wrap leading-relaxed">
                        {news[0].content}
                    </p>
                </div>
            )}
        </div>
    )
}

export default News