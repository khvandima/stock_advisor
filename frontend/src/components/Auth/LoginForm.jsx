import { useState } from 'react'
import client from '../../api/client'
import useStore from '../../store/useStore'

function LoginForm() {
    const [mode, setMode] = useState('login')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [fullName, setFullName] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const setToken = useStore((state) => state.setToken)

    const handleSubmit = async () => {
        setLoading(true)
        setError('')
        try {
            if (mode === 'login') {
                const form = new FormData()
                form.append('username', email)
                form.append('password', password)
                const res = await client.post('/auth/login', form)
                setToken(res.data.access_token)
            } else {
                await client.post('/auth/register', {
                    email,
                    password,
                    full_name: fullName,
                })
                const form = new FormData()
                form.append('username', email)
                form.append('password', password)
                const res = await client.post('/auth/login', form)
                setToken(res.data.access_token)
            }
        } catch (e) {
            setError(mode === 'login' ? 'Неверный email или пароль' : 'Ошибка регистрации')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="bg-gray-900 p-8 rounded-2xl w-full max-w-md shadow-xl">
                <h1 className="text-2xl font-bold text-white mb-2">Stock AI Advisor</h1>
                <p className="text-gray-400 mb-6">Korean Stock Market</p>

                <div className="flex mb-6 bg-gray-800 rounded-lg p-1">
                    <button
                        onClick={() => { setMode('login'); setError('') }}
                        className={`flex-1 py-2 rounded-md text-sm font-medium transition-colors ${
                            mode === 'login' ? 'bg-purple-600 text-white' : 'text-gray-400'
                        }`}
                    >
                        Login
                    </button>
                    <button
                        onClick={() => { setMode('register'); setError('') }}
                        className={`flex-1 py-2 rounded-md text-sm font-medium transition-colors ${
                            mode === 'register' ? 'bg-purple-600 text-white' : 'text-gray-400'
                        }`}
                    >
                        Register
                    </button>
                </div>

                <div className="space-y-4">
                    {mode === 'register' && (
                        <input
                            type="text"
                            placeholder="Имя"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-purple-500"
                        />
                    )}
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <input
                        type="password"
                        placeholder="Password"
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
                        {loading ? '...' : mode === 'login' ? 'Login' : 'Register'}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default LoginForm