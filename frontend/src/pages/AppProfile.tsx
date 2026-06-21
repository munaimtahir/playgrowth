import { Card } from '../components/Card';

export function AppProfile() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">App Profile</h1>
        <p className="mt-2 text-slate-600">Store app identity, positioning, target countries, monetization model, and notes used by the recommendation engine.</p>
      </div>
      <Card title="MVP scaffold">
        <p className="text-slate-600">This screen is scaffolded for the first implementation sprint. Connect it to the DRF endpoints listed in the docs.</p>
      </Card>
    </div>
  );
}
