import { useState } from 'react'
import Portfolio from '../Portfolio/Portfolio'
import StockChart from '../StockChart/StockChart'
import Signals from '../Signals/Signals'
import AIChat from '../AIChat/AIChat'
import News from '../News/News'
import useStore from '../../store/useStore'

function Dashboard() {
    const [activeTab, setActiveTab] = useState('portfolio')
    const logout = useStore((state) => state.logout)

    const tabs = [
        { id: 'portfolio', label: 'Портфель' },
        { id: 'chart', label: 'Графики' },
        { id: 'signals', label: 'Сигналы' },
        { id: 'chat', label: 'AI Советник' },
        { id: 'news', label: 'Новости' },
    ]

    return (
        <div className="min-h-screen bg-gray-950">
            {/* Header */}
            <div className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
                <h1 className="text-xl font-bold text-white">📈 Stock AI Advisor</h1>
                <button
                    onClick={logout}
                    className="text-gray-400 hover:text-white text-sm transition-colors"
                >
                    Выйти
                </button>
            </div>

            {/* Tabs */}
            <div className="bg-gray-900 border-b border-gray-800 px-6">
                <div className="flex space-x-1">
                    {tabs.map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`px-4 py-3 text-sm font-medium transition-colors border-b-2 ${
                                activeTab === tab.id
                                    ? 'border-purple-500 text-purple-400'
                                    : 'border-transparent text-gray-400 hover:text-white'
                            }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* Content */}
            <div className="p-6">
                {activeTab === 'portfolio' && <Portfolio />}
                {activeTab === 'chart' && <StockChart />}
                {activeTab === 'signals' && <Signals />}
                {activeTab === 'chat' && <AIChat />}
                {activeTab === 'news' && <News />}
            </div>
        </div>
    )
}

export default Dashboard