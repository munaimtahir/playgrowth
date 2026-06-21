export type AppProfile = {
  id: number;
  name: string;
  package_name: string;
  primary_positioning: string;
  target_countries: string;
  monetization_model: string;
};

export type Recommendation = {
  id: number;
  title: string;
  category: string;
  status: string;
  diagnosis: string;
  suggested_human_action: string;
  copyable_text: string;
  do_not_do_yet: string;
  confidence_score: number;
  risk_level: string;
  effort_level: string;
  watch_metric: string;
};

export type DashboardSummary = {
  app: AppProfile;
  kpis: {
    installs: number;
    store_visitors: number;
    conversion_rate: number;
    day_1_retention: number;
    day_7_retention: number;
  };
  bottleneck: string;
  evidence: string[];
  confidence_score: number;
  top_recommendations: Recommendation[];
  recent_actions: any[];
};
