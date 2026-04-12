import { useState } from 'react'
import client from '../../api/client'

function Signals() {
    const [ticker, setTicker] = useState('')
    const [signal, setSignal] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const fetchSignal = async () => {
        if (!ticker) return
        setLoading(true)
        setError('')
        try {
            const res = await client.get(`/stocks/${ticker}/signal`)
            setSignal(res.data)
        } catch (e) {
            setError('Акция не найдена')
        } finally {
            setLoading(false)
        }
    }

    const signalColor = {
        bullish: 'text-green-400',
        bearish: 'text-red-400',
        neutral: 'text-yellow-400',
    }

    const signalLabel = {
        bullish: '🐂 Бычий',
        bearish: '🐻 Медвежий',
        neutral: '➡️ Нейтральный',
    }

    return (
        <div className="bg-gray-900 rounded-xl p-6 space-y-4">
            <h2 className="text-lg font-semibold text-white">Технические сигналы</h2>

            <div className="flex gap-3">
                <input
                    placeholder="Тикер (005930)"
                    value={ticker}
                    onChange={(e) => setTicker(e.target.value)}
                    className="bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 w-40"
                />
                <button
                    onClick={fetchSignal}
                    disabled={loading}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                    {loading ? 'Анализ...' : 'Анализировать'}
                </button>
            </div>

            {error && <p className="text-red-400 text-sm">{error}</p>}

            {signal && (
                <div className="space-y-4">
                    <div className="bg-gray-800 rounded-xl p-6 text-center">
                        <p className="text-gray-400 text-sm mb-2">Общий сигнал</p>
                        <p className={`text-3xl font-bold ${signalColor[signal.signal]}`}>
                            {signalLabel[signal.signal]}
                        </p>
                    </div>

                    <div className="grid grid-cols-3 gap-4">
                        <div className="bg-gray-800 rounded-xl p-4 text-center">
                            <p className="text-gray-400 text-sm mb-1">RSI</p>
                            <p className={`text-2xl font-bold ${
                                signal.rsi < 30 ? 'text-green-400' :
                                    signal.rsi > 70 ? 'text-red-400' : 'text-white'
                            }`}>
                                {signal.rsi.toFixed(1)}
                            </p>
                            <p className="text-gray-500 text-xs mt-1">
                                {signal.rsi < 30 ? 'Перепродан' : signal.rsi > 70 ? 'Перекуплен' : 'Норма'}
                            </p>
                        </div>

                        <div className="bg-gray-800 rounded-xl p-4 text-center">
                            <p className="text-gray-400 text-sm mb-1">MA20</p>
                            <p className="text-2xl font-bold text-white">
                                ₩{signal.ma20.toLocaleString()}
                            </p>
                        </div>

                        <div className="bg-gray-800 rounded-xl p-4 text-center">
                            <p className="text-gray-400 text-sm mb-1">MA50</p>
                            <p className="text-2xl font-bold text-white">
                                ₩{signal.ma50.toLocaleString()}
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Signals