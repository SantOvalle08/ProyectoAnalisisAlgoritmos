import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Database, 
  GitCompare, 
  BarChart3, 
  Network, 
  LineChart, 
  Home 
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

const navigation = [
  { name: 'Inicio', href: '/', icon: Home },
  { name: 'Adquisición de Datos', href: '/data-acquisition', icon: Database },
  { name: 'Similitud Textual', href: '/similarity', icon: GitCompare },
  { name: 'Análisis de Frecuencias', href: '/frequency', icon: BarChart3 },
  { name: 'Clustering', href: '/clustering', icon: Network },
  { name: 'Visualizaciones', href: '/visualizations', icon: LineChart },
];

export default function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Análisis Bibliométrico
              </h1>
              <p className="text-sm text-gray-600">
                Universidad del Quindío - Análisis de Algoritmos
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 overflow-x-auto">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`
                    flex items-center gap-2 py-4 px-3 border-b-2 text-sm font-medium whitespace-nowrap
                    ${
                      isActive
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            © 2025 Universidad del Quindío - Santiago Ovalle Cortés & Juan Sebastián Noreña
          </p>
        </div>
      </footer>
    </div>
  );
}
