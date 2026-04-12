import { useState, useEffect } from 'react'
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

    const handleDelete = async (id) => {
        try {
            await client.delete(`/portfolio/${id}`)
            fetchPortfolio()
        } catch (e) {
            console.error(e)
        }
    }

    if (loading) return <div className="text-gray-400">Загрузка...</div>

    return (
        <div className="space-y-6">
            {/* Добавить акцию */}
            <div className="bg-gray-900 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white mb-4">Добавить акцию</h2>
                <div className="flex gap-3 flex-wrap">
                    <input
                        placeholder="Тикер (005930)"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        className="bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 w-36"
                    />
                    <input
                        placeholder="Количество"
                        value={quantity}
                        onChange={(e) => setQuantity(e.target.value)}
                        type="number"
                        className="bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 w-36"
                    />
                    <input
                        placeholder="Цена покупки"
                        value={purchasePrice}
                        onChange={(e) => setPurchasePrice(e.target.value)}
                        type="number"
                        className="bg-gray-800 text-white px-4 py-2 rounded-lg outline-none focus:ring-2 focus:ring-purple-500 w-40"
                    />
                    <button
                        onClick={handleAdd}
                        disabled={adding}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                        {adding ? 'Добавление...' : 'Добавить'}
                    </button>
                </div>
            </div>

            {/* Список акций */}
            <div className="bg-gray-900 rounded-xl p-6">
                <h2 className="text-lg font-semibold text-white mb-4">Мой портфель</h2>
                {items.length === 0 ? (
                    <p className="text-gray-400">Портфель пуст</p>
                ) : (
                    <div className="space-y-3">
                        {items.map((item) => (
                            <div
                                key={item.id}
                                className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-3"
                            >
                                <div>
                                    <span className="text-white font-medium">{item.ticker}</span>
                                    <span className="text-gray-400 text-sm ml-3">
                    {item.quantity} шт. × ₩{item.purchase_price.toLocaleString()}
                  </span>
                                </div>
                                <button
                                    onClick={() => handleDelete(item.id)}
                                    className="text-red-400 hover:text-red-300 text-sm transition-colors"
                                >
                                    Удалить
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