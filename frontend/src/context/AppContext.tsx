import { createContext, ReactNode, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { getList } from '../api/client';
import type { AppProfile } from '../types';

type AppContextValue = {
  apps: AppProfile[];
  selectedAppId: number | null;
  selectedApp: AppProfile | null;
  setSelectedAppId: (id: number | null) => void;
  refreshApps: () => Promise<void>;
};

const AppContext = createContext<AppContextValue | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [apps, setApps] = useState<AppProfile[]>([]);
  const [selectedAppId, setSelectedAppId] = useState<number | null>(() => {
    const stored = localStorage.getItem('playgrowth.selectedAppId');
    return stored ? Number(stored) : null;
  });

  const refreshApps = useCallback(async () => {
    const items = await getList<AppProfile>('/apps/');
    setApps(items);
    setSelectedAppId((current) => {
      if (current && items.some((item) => item.id === current)) {
        return current;
      }
      return items[0]?.id ?? null;
    });
  }, []);

  useEffect(() => {
    refreshApps().catch(() => setApps([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (apps.length === 0) return;
    if (!selectedAppId || !apps.some((item) => item.id === selectedAppId)) {
      setSelectedAppId(apps[0].id);
    }
  }, [apps, selectedAppId]);

  useEffect(() => {
    if (selectedAppId) {
      localStorage.setItem('playgrowth.selectedAppId', String(selectedAppId));
    } else {
      localStorage.removeItem('playgrowth.selectedAppId');
    }
  }, [selectedAppId]);

  const selectedApp = useMemo(
    () => apps.find((item) => item.id === selectedAppId) ?? apps[0] ?? null,
    [apps, selectedAppId],
  );

  const value = useMemo(
    () => ({
      apps,
      selectedAppId: selectedApp?.id ?? selectedAppId,
      selectedApp,
      setSelectedAppId,
      refreshApps,
    }),
    [apps, selectedApp, selectedAppId, refreshApps],
  );

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useAppContext() {
  const value = useContext(AppContext);
  if (!value) {
    throw new Error('useAppContext must be used inside AppProvider');
  }
  return value;
}
