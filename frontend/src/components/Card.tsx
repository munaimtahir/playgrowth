import { ReactNode } from 'react';

export function Card({ title, children }: { title?: string; children: ReactNode }) {
  return (
    <section className="rounded-[1.5rem] border border-slate-200/80 bg-white/85 p-5 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur">
      {title && <h2 className="mb-4 text-base font-semibold tracking-tight text-slate-900">{title}</h2>}
      {children}
    </section>
  );
}
