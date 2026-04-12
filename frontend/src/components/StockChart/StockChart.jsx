import { useState } from 'react'
import {
    ComposedChart,
    Line,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from 'recharts'
import client from '../../api/client'

function StockChart() {
    const [ticker, setTicker] = useState('')
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const fetchChart = async () => {
        if (!ticker) return
        setLoading(true)
        setError('')
        try {
            const res = await client.get(`/stocks/${ticker}/history?days=30`)
            setData(res.data)
        } catch (e) {
            setError('Акция не найдена')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="bg-gray-900 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white">График цены</h2>

            <div className="flex gap-3">
                <input
                    placeholder="Тикер (005930)"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value)}
                    className="bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 w-40"
                />
                <button
                    onClick={fetchChart}
                    disabled={loading}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                    {loading ? 'Загрузка...' : 'Показать'}
                </button>
            </div>

            {error && <p className="text-red-400 text-sm">{error}</p>}

            {data.length > 0 && (
                <ResponsiveContainer width="100%" height={400}>
                    <ComposedChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                        <XAxis
                            dataKey="date"
                            tick={{ fill: '#9ca3af', fontSize: 12 }}
                            tickFormatter={(v) => v.slice(5)}
                        />
                        <YAxis
                            yAxisId="price"
                            tick={{ fill: '#9ca3af', fontSize: 12 }}
                            tickFormatter={(v) => `₩${(v / 1000).toFixed(0)}k`}
                        />
                        <YAxis
                            yAxisId="volume"
                            orientation="right"
                            tick={{ fill: '#9ca3af', fontSize: 12 }}
                            tickFormatter={(v) => `${(v / 1000000).toFixed(0)}M`}
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                            labelStyle={{ color: '#e5e7eb' }}
                        />
                        <Legend />
                        <Bar yAxisId="volume" dataKey="volume" fill="#374151" name="Объём" />
                        <Line
                            yAxisId="price"
                            type="monotone"
                            dataKey="close"
                            stroke="#a855f7"
                            dot={false}
                            strokeWidth={2}
                            name="Цена закрытия"
                        />
                    </ComposedChart>
                </ResponsiveContainer>
            )}
        </div>
    )
}

export default StockChart