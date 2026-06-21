import { Card } from '../components/Card';

export function ListingAdvisor() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Listing Advisor</h1>
        <p className="mt-2 text-slate-600">Generate copyable short descriptions, screenshot captions, and feature graphic ideas. No publishing button.</p>
      </div>
      <Card title="MVP scaffold">
        <p className="text-slate-600">This screen is scaffolded for the first implementation sprint. Connect it to the DRF endpoints listed in the docs.</p>
      </Card>
    </div>
  );
}
