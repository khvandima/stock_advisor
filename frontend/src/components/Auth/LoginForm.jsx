import { useState } from 'react'
import client from '../../api/client'
import useStore from '../../store/useStore'

function LoginForm() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const setToken = useStore((state) => state.setToken)

    const handleSubmit = async () => {
        setLoading(true)
        setError('')
        try {
            const form = new FormData()
            form.append('username', email)
            form.append('password', password)
            const res = await client.post('/auth/login', form)
            setToken(res.data.access_token)
        } catch (e) {
            setError('Неверный email или пароль')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md shadow-xl">
                <h1 className="text-2xl font-bold text-white mb-2">Stock AI Advisor</h1>
                <p className="text-gray-400 mb-6">Корейский фондовый рынок</p>

                <div className="space-y-4">
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <input
                        type="password"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button
                        onClick={handleSubmit}
                        disabled={loading}
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                        {loading ? 'Вход...' : 'Войти'}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default LoginForm