import { NavLink, Outlet } from 'react-router-dom';

const nav = [
  ['/', 'Dashboard'],
  ['/app-profile', 'App Profile'],
  ['/data-import', 'Data Import'],
  ['/reports', 'Growth Reports'],
  ['/recommendations', 'Recommendations'],
  ['/reviews', 'Reviews'],
  ['/listing-advisor', 'Listing Advisor'],
  ['/experiments', 'Experiments'],
  ['/action-log', 'Action Log'],
  ['/settings', 'Settings'],
];

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <aside className="fixed inset-y-0 left-0 w-72 border-r border-slate-200 bg-white p-5">
        <div className="mb-8">
          <h1 className="text-xl font-bold">PlayGrowth Copilot</h1>
          <p className="mt-2 text-sm text-slate-600">AI-assisted growth analyst. No auto-publishing.</p>
        </div>
        <nav className="space-y-1">
          {nav.map(([to, label]) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `block rounded-xl px-3 py-2 text-sm ${isActive ? 'bg-slate-900 text-white' : 'text-slate-700 hover:bg-slate-100'}`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="ml-72 p-8">
        <Outlet />
      </main>
    </div>
  );
}
