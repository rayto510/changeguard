import { FC } from 'react'
import './App.css'

const App: FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow">
        <nav className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-indigo-600">ChangeGuard</h1>
        </nav>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-12 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Schema Change Tracking</h2>
          <p className="text-gray-600 mb-6">
            Welcome to ChangeGuard - Track and manage breaking and non-breaking API/schema changes.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">🔄 Track Changes</h3>
              <p className="text-gray-600">Monitor all schema modifications and their impact</p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">⚠️ Breaking Changes</h3>
              <p className="text-gray-600">Identify and manage breaking changes proactively</p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">💬 Collaborate</h3>
              <p className="text-gray-600">Discuss changes with your team in one place</p>
            </div>

            <div className="border border-gray-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">🔔 Notifications</h3>
              <p className="text-gray-600">Stay updated with real-time notifications</p>
            </div>
          </div>

          <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              Backend API Status: <span className="font-semibold">Ready at /api/v1</span>
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
