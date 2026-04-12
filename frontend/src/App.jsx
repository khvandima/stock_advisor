import { useState } from 'react'
import LoginForm from './components/Auth/LoginForm'
import Dashboard from './components/Dashboard/Dashboard'
import useStore from './store/useStore'

function App() {
    const token = useStore((state) => state.token)

    return (
        <div className="min-h-screen bg-gray-950 text-gray-100">
            {token ? <Dashboard /> : <LoginForm />}
        </div>
    )
}

export default App