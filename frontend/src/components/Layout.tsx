import { NavLink, Outlet } from 'react-router-dom';
import { useAppContext } from '../context/AppContext';

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
  const { apps, selectedAppId, selectedApp, setSelectedAppId } = useAppContext();

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(255,210,120,0.35),_transparent_28%),radial-gradient(circle_at_top_right,_rgba(108,93,255,0.16),_transparent_24%),linear-gradient(180deg,_#f9fafb_0%,_#f3f4f6_100%)] text-slate-900">
      <aside className="fixed inset-y-0 left-0 flex w-80 flex-col border-r border-slate-200/80 bg-slate-950/92 px-5 py-6 text-slate-100 shadow-2xl shadow-slate-950/20 backdrop-blur">
        <div className="mb-8">
          <p className="text-xs uppercase tracking-[0.35em] text-amber-300/80">PlayGrowth Copilot</p>
          <h1 className="mt-3 text-2xl font-semibold leading-tight">Growth analysis for offline-first Android games</h1>
          <p className="mt-3 text-sm leading-6 text-slate-300">
            Recommends manual actions only. No Play Console writes, no ad automation, no fake growth.
          </p>
        </div>

        <label className="mb-5 block">
          <span className="mb-2 block text-xs uppercase tracking-[0.25em] text-slate-400">Active app</span>
          <select
            value={selectedAppId ?? ''}
            onChange={(event) => setSelectedAppId(event.target.value ? Number(event.target.value) : null)}
            className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none transition focus:border-amber-300/60 focus:bg-white/10"
          >
            {apps.length === 0 && <option value="">No app profiles yet</option>}
            {apps.map((app) => (
              <option key={app.id} value={app.id}>
                {app.name}
              </option>
            ))}
          </select>
        </label>

        {selectedApp && (
          <div className="mb-6 rounded-3xl border border-amber-300/20 bg-amber-300/10 p-4 text-sm text-amber-50">
            <p className="text-xs uppercase tracking-[0.28em] text-amber-200/80">Positioning</p>
            <p className="mt-2 leading-6">{selectedApp.primary_positioning || 'No positioning yet.'}</p>
          </div>
        )}

        <nav className="flex-1 space-y-1 overflow-y-auto pr-1">
          {nav.map(([to, label]) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                [
                  'group flex items-center justify-between rounded-2xl px-4 py-3 text-sm transition',
                  isActive
                    ? 'bg-white text-slate-950 shadow-lg shadow-amber-300/20'
                    : 'text-slate-300 hover:bg-white/5 hover:text-white',
                ].join(' ')
              }
            >
              <span>{label}</span>
              <span className="text-xs text-slate-400 group-hover:text-slate-500">↗</span>
            </NavLink>
          ))}
        </nav>

        <div className="mt-5 rounded-3xl border border-white/10 bg-white/5 p-4 text-xs leading-5 text-slate-300">
          <p className="font-medium text-white">Safety principle</p>
          <p className="mt-2">The copilot recommends. The developer decides and implements manually.</p>
        </div>
      </aside>
      <main className="ml-80 min-h-screen px-8 py-7">
        <div className="mx-auto max-w-7xl">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
