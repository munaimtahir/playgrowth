export function formatDate(value?: string | null) {
  if (!value) return 'n/a';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

export function formatDateTime(value?: string | null) {
  if (!value) return 'n/a';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' });
}

export function formatNumber(value: number | string | undefined) {
  const numeric = typeof value === 'string' ? Number(value) : value ?? 0;
  return new Intl.NumberFormat('en-US').format(Number.isFinite(numeric) ? numeric : 0);
}

export function formatPercent(value: number | undefined, digits = 1) {
  if (value === undefined || value === null) return '0%';
  return `${Number(value).toFixed(digits)}%`;
}

export function statusTone(status: string) {
  switch (status) {
    case 'high':
    case 'done':
    case 'accepted':
      return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    case 'medium':
    case 'monitoring':
      return 'bg-amber-100 text-amber-800 border-amber-200';
    case 'low':
    case 'new':
      return 'bg-slate-100 text-slate-700 border-slate-200';
    case 'rejected':
      return 'bg-rose-100 text-rose-800 border-rose-200';
    default:
      return 'bg-slate-100 text-slate-700 border-slate-200';
  }
}
