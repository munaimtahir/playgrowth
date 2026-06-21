import { Route, Routes } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { AppProfile } from './pages/AppProfile';
import { DataImport } from './pages/DataImport';
import { Reports } from './pages/Reports';
import { Recommendations } from './pages/Recommendations';
import { Reviews } from './pages/Reviews';
import { ListingAdvisor } from './pages/ListingAdvisor';
import { Experiments } from './pages/Experiments';
import { ActionLog } from './pages/ActionLog';
import { Settings } from './pages/Settings';

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/app-profile" element={<AppProfile />} />
        <Route path="/data-import" element={<DataImport />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/reviews" element={<Reviews />} />
        <Route path="/listing-advisor" element={<ListingAdvisor />} />
        <Route path="/experiments" element={<Experiments />} />
        <Route path="/action-log" element={<ActionLog />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}
