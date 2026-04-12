import { useState, useEffect } from 'react'
import { Trash2 } from 'lucide-react'
import client from '../../api/client'

function Portfolio() {
    const [items, setItems] = useState([])
    const [loading, setLoading] = useState(true)
    const [ticker, setTicker] = useState('')
    const [quantity, setQuantity] = useState('')
    const [purchasePrice, setPurchasePrice] = useState('')
    const [adding, setAdding] = useState(false)

    const fetchPortfolio = async () => {
        try {
            const res = await client.get('/portfolio/')
            setItems(res.data)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchPortfolio()
    }, [])

    const handleAdd = async () => {
        if (!ticker || !quantity || !purchasePrice) return
        setAdding(true)
        try {
            await client.post('/portfolio/add', {
                ticker,
                quantity: parseInt(quantity),
                purchase_price: parseFloat(purchasePrice),
            })
            setTicker('')
            setQuantity('')
            setPurchasePrice('')
            fetchPortfolio()
        } catch (e) {
            console.error(e)
        } finally {
            setAdding(false)
        }
    }

    const handleDelete = async (id, ticker) => {
        if (!window.confirm(`Удалить ${ticker} из портфеля?`)) return
        try {
            await client.delete(`/portfolio/${id}`)
            fetchPortfolio()
        } catch (e) {
            console.error(e)
        }
    }

    if (loading) return <div className="text-gray-400 text-sm">Загрузка...</div>

    return (
        <div className="space-y-4">
            <div>
                <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Добавить акцию</h2>
                <div className="space-y-2">
                    <input
                        placeholder="Тикер (005930)"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        className="w-full bg-gray-800 text-white px-3 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                    />
                    <input
                        placeholder="Количество"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        type="number"
                        className="w-full bg-gray-800 text-white px-3 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                    />
                    <input
                        placeholder="Цена покупки (₩)"
                        value={purchasePrice}
                        onChange={(e) => setPurchasePrice(e.target.value)}
                        type="number"
                        className="w-full bg-gray-800 text-white px-3 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 text-sm"
                    />
                    <button
                        onClick={handleAdd}
                        disabled={adding}
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white py-2 rounded-lg text-sm font-medium transition-colors disabled:opacity-50"
                    >
                        {adding ? 'Добавление...' : '+ Добавить'}
                    </button>
                </div>
            </div>

            <div>
                <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">Портфель</h2>
                {items.length === 0 ? (
                    <p className="text-gray-500 text-sm">Портфель пуст</p>
                ) : (
                    <div className="space-y-2">
                        {items.map((item) => (
                            <div
                                key={item.id}
                                className="flex items-center justify-between bg-gray-800 rounded-lg px-3 py-2"
                            >
                                <div>
                                    <div className="text-white font-medium text-sm">{item.ticker}</div>
                                    <div className="text-gray-400 text-xs">
                                        {item.quantity} шт · ₩{item.purchase_price.toLocaleString()}
                                    </div>
                                </div>
                                <button
                                    onClick={() => handleDelete(item.id, item.ticker)}
                                    className="text-red-500 hover:text-red-300 transition-colors"
                                    title="Удалить"
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

export default Portfolio