import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../api/client';
import { Card } from '../components/Card';
import { useAppContext } from '../context/AppContext';
import { formatDate, statusTone } from '../lib/format';
import type { ReviewItem, ReviewTheme } from '../types';

export function Reviews() {
  const { selectedApp } = useAppContext();
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [themes, setThemes] = useState<ReviewTheme[]>([]);
  const [message, setMessage] = useState('');

  const refresh = async () => {
    if (!selectedApp) return;
    const reviewItems = await apiGet<{ results: ReviewItem[] } | ReviewItem[]>(`/reviews/?app=${selectedApp.id}`);
    const themeItems = await apiGet<{ results: ReviewTheme[] } | ReviewTheme[]>(`/review-themes/?app=${selectedApp.id}`);
    setReviews(Array.isArray(reviewItems) ? reviewItems : reviewItems.results);
    setThemes(Array.isArray(themeItems) ? themeItems : themeItems.results);
  };

  useEffect(() => {
    refresh().catch(() => {
      setReviews([]);
      setThemes([]);
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedApp, message]);

  const analyze = async () => {
    if (!selectedApp) return;
    setMessage('');
    await apiPost('/reviews/analyze/', { app: selectedApp.id });
    setMessage('Review analysis updated.');
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Review analysis</p>
          <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950">Turn reviews into product signals</h1>
          <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-600">
            This screen clusters recent feedback so you can fix the product issue manually instead of guessing.
          </p>
        </div>
        <button type="button" onClick={analyze} disabled={!selectedApp} className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white disabled:opacity-60">
          Analyze reviews
        </button>
      </div>

      {!selectedApp && <Card title="No app selected"><p className="text-sm text-slate-600">Select an app profile first.</p></Card>}
      {message && <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700">{message}</div>}

      {selectedApp && (
        <div className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
          <Card title="Recent reviews">
            <div className="space-y-3">
              {reviews.map((review) => (
                <article key={review.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-slate-950 px-2 py-1 text-xs font-semibold text-white">{review.rating}★</span>
                    <span className="text-xs uppercase tracking-[0.22em] text-slate-500">{formatDate(review.date)}</span>
                    {review.status && <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(review.status)}`}>{review.status}</span>}
                  </div>
                  <p className="mt-3 text-sm leading-6 text-slate-700">{review.review_text}</p>
                  {review.ai_summary && <p className="mt-3 text-sm text-slate-600"><span className="font-medium text-slate-900">AI summary:</span> {review.ai_summary}</p>}
                  {review.suggested_reply && <p className="mt-2 text-sm text-slate-600"><span className="font-medium text-slate-900">Draft reply:</span> {review.suggested_reply}</p>}
                </article>
              ))}
              {reviews.length === 0 && <p className="text-sm text-slate-600">No reviews imported yet.</p>}
            </div>
          </Card>

          <Card title="Detected themes">
            <div className="space-y-3">
              {themes.map((theme) => (
                <article key={theme.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-full bg-white px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] text-slate-500">{theme.category}</span>
                    <span className={`rounded-full border px-2 py-1 text-xs font-medium uppercase tracking-[0.22em] ${statusTone(theme.severity)}`}>{theme.severity}</span>
                    <span className="rounded-full border border-slate-200 bg-white px-2 py-1 text-xs font-medium text-slate-500">{theme.count}</span>
                  </div>
                  <p className="mt-3 font-semibold text-slate-900">{theme.theme}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{theme.recommendation}</p>
                </article>
              ))}
              {themes.length === 0 && <p className="text-sm text-slate-600">Run review analysis to detect themes.</p>}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
