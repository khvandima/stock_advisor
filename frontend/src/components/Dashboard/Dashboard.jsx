import { useState } from 'react'
import Portfolio from '../Portfolio/Portfolio'
import StockChart from '../StockChart/StockChart'
import Signals from '../Signals/Signals'
import AIChat from '../AIChat/AIChat'
import News from '../News/News'
import useStore from '../../store/useStore'

function Dashboard() {
    const [activeTab, setActiveTab] = useState('chart')
    const logout = useStore((state) => state.logout)

    const tabs = [
        { id: 'chart', label: 'Графики' },
        { id: 'signals', label: 'Сигналы' },
        { id: 'news', label: 'Новости' },
    ]

    return (
        <div className="h-screen bg-gray-950 flex flex-col">
            <div className="bg-gray-900 border-b border-gray-800 px-6 py-3 flex items-center justify-between shrink-0">
                <h1 className="text-xl font-bold text-white">📈 Stock AI Advisor</h1>
                <button onClick={logout} className="text-gray-400 hover:text-white text-sm transition-colors">
                    Logout
                </button>
            </div>

            <div className="flex flex-1 overflow-hidden min-h-0">
                {/* Sidebar */}
                <div className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col shrink-0">
                    <div className="overflow-y-auto flex-1 p-4">
                        <Portfolio />
                    </div>
                    <nav className="flex flex-col gap-1 p-4 border-t border-gray-800 shrink-0">
                        {tabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`text-left px-4 py-2 rounded-lg text-sm transition-colors ${
                                    activeTab === tab.id
                                        ? 'bg-purple-600 text-white'
                                        : 'text-gray-400 hover:text-white hover:bg-gray-800'
                                }`}
                            >
                                {tab.label}
                            </button>
                        ))}
                    </nav>
                </div>

                {/* Main content */}
                {/* Main content */}
                <div className="flex-1 flex flex-col overflow-hidden">
                    <div className="h-1/2 p-4 overflow-y-auto border-b border-gray-800">
                        {activeTab === 'chart' && <StockChart />}
                        {activeTab === 'signals' && <Signals />}
                        {activeTab === 'news' && <News />}
                    </div>

                    {/* Bottom - AI чат всегда */}
                    <div className="h-1/2 overflow-hidden">
                        <AIChat />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Dashboard