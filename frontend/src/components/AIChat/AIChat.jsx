import { useState, useRef, useEffect } from 'react'
import client from '../../api/client'

function AIChat() {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [threadId, setThreadId] = useState(null)
    const bottomRef = useRef(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim() || loading) return
        const userMessage = input.trim()
        setInput('')
        setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
        setLoading(true)

        try {
            const res = await client.post('/chat/', {
                query: userMessage,
                thread_id: threadId,
            })
            setThreadId(res.data.thread_id)
            setMessages((prev) => [...prev, { role: 'assistant', content: res.data.response }])
        } catch (e) {
            setMessages((prev) => [...prev, { role: 'assistant', content: 'Ошибка. Попробуйте снова.' }])
        } finally {
            setLoading(false)
        }
    }

    const newChat = () => {
        setMessages([])
        setThreadId(null)
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="bg-gray-900 rounded-xl flex flex-col h-[600px]">
            <div className="p-4 border-b border-gray-800 flex items-center justify-between">
                <div>
                    <h2 className="text-lg font-semibold text-white">AI Советник</h2>
                    <p className="text-gray-400 text-sm">Спросите про любую корейскую акцию</p>
                </div>
                <button
                    onClick={newChat}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                >
                    Новый чат
                </button>
            </div>

            {/* Сообщения */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 mt-10">
                        <p className="text-4xl mb-3">📈</p>
                        <p>Спросите про Samsung, SK Hynix, Kakao...</p>
                        <p className="text-sm mt-1">Например: "Стоит ли покупать 삼성전자?"</p>
                    </div>
                )}
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
                                msg.role === 'user'
                                    ? 'bg-purple-600 text-white'
                                    : 'bg-gray-800 text-gray-100'
                            }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-800 px-4 py-3 rounded-2xl text-gray-400 text-sm">
                            Анализирую...
                        </div>
                    </div>
                )}
                <div ref={bottomRef} />
            </div>

            {/* Инпут */}
            <div className="p-4 border-t border-gray-800 flex gap-3">
        <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Спросите про акцию..."
            rows={1}
            className="flex-1 bg-gray-800 text-white px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-purple-500 resize-none"
        />
                <button
                    onClick={sendMessage}
                    disabled={loading || !input.trim()}
                    className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-3 rounded-xl font-medium transition-colors disabled:opacity-50"
                >
                    →
                </button>
            </div>
        </div>
    )
}

export default AIChat