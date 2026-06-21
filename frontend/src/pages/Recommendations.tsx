import { Card } from '../components/Card';

export function Recommendations() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Recommendations</h1>
        <p className="mt-2 text-slate-600">Prioritized human action queue. Recommendations can be accepted, rejected, manually implemented, or monitored.</p>
      </div>
      <Card title="MVP scaffold">
        <p className="text-slate-600">This screen is scaffolded for the first implementation sprint. Connect it to the DRF endpoints listed in the docs.</p>
      </Card>
    </div>
  );
}
