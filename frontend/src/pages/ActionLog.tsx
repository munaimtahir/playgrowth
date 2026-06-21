import { Card } from '../components/Card';

export function ActionLog() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Manual Action Log</h1>
        <p className="mt-2 text-slate-600">Record what you manually changed outside the system and track outcomes.</p>
      </div>
      <Card title="MVP scaffold">
        <p className="text-slate-600">This screen is scaffolded for the first implementation sprint. Connect it to the DRF endpoints listed in the docs.</p>
      </Card>
    </div>
  );
}
