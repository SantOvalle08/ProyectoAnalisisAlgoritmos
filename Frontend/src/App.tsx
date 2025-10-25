import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import DataAcquisitionPage from './pages/DataAcquisitionPage';
import SimilarityPage from './pages/SimilarityPage';
import FrequencyPage from './pages/FrequencyPage';
import ClusteringPage from './pages/ClusteringPage';
import VisualizationsPage from './pages/VisualizationsPage';

// Crear el cliente de React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/data-acquisition" element={<DataAcquisitionPage />} />
            <Route path="/similarity" element={<SimilarityPage />} />
            <Route path="/frequency" element={<FrequencyPage />} />
            <Route path="/clustering" element={<ClusteringPage />} />
            <Route path="/visualizations" element={<VisualizationsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
