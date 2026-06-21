export type AppProfile = {
  id: number;
  name: string;
  package_name: string;
  play_store_url: string;
  category: string;
  app_type: string;
  primary_positioning: string;
  target_countries: string;
  monetization_model: string;
  current_version: string;
  notes: string;
};

export type Recommendation = {
  id: number;
  title: string;
  category: string;
  priority: 'high' | 'medium' | 'low';
  status: 'new' | 'accepted' | 'rejected' | 'done' | 'monitoring';
  diagnosis: string;
  suggested_human_action: string;
  copyable_text: string;
  do_not_do_yet: string;
  why_this_matters: string;
  confidence_score: number;
  risk_level: 'low' | 'medium' | 'high';
  effort_level: 'low' | 'medium' | 'high';
  watch_metric: string;
  evidence_json: string[];
  created_at?: string;
  updated_at?: string;
};

export type RecommendationDraft = {
  category: string;
  title: string;
  priority: 'high' | 'medium' | 'low';
  diagnosis: string;
  evidence: string[];
  suggested_human_action: string;
  copyable_text: string;
  do_not_do_yet: string;
  why_this_matters: string;
  risk_level: 'low' | 'medium' | 'high';
  effort_level: 'low' | 'medium' | 'high';
  confidence_score: number;
  watch_metric: string;
};

export type GrowthReport = {
  id: number;
  report_type: string;
  report_date: string;
  period_start: string;
  period_end: string;
  summary: string;
  bottleneck: string;
  evidence_json: string[];
  next_actions_json: Recommendation[];
  confidence_score: number;
  ai_provider: string;
};

export type ManualAction = {
  id: number;
  action_date: string;
  action_type: string;
  title: string;
  description: string;
  changed_location: string;
  before_text: string;
  after_text: string;
  expected_metric: string;
  followup_date: string | null;
  outcome_notes: string;
  recommendation: number | null;
};

export type ReviewItem = {
  id: number;
  date: string;
  rating: number;
  reviewer_name: string;
  review_text: string;
  category: string;
  ai_summary: string;
  suggested_reply: string;
  status: string;
  language: string;
};

export type ReviewTheme = {
  id: number;
  date_range_start: string;
  date_range_end: string;
  category: string;
  theme: string;
  count: number;
  severity: string;
  examples_json: string[];
  recommendation: string;
};

export type Experiment = {
  id: number;
  name: string;
  hypothesis: string;
  area: string;
  variant_a: string;
  variant_b: string;
  primary_metric: string;
  secondary_metric: string;
  minimum_duration_days: number;
  minimum_sample_size: number;
  status: string;
  result: string;
  decision: string;
};

export type ImportBatch = {
  id: number;
  import_type: string;
  source_filename: string;
  row_count: number;
  status: string;
  error_summary: string;
  created_at: string;
};

export type DashboardSummary = {
  app: AppProfile;
  window: {
    start: string;
    end: string;
  };
  kpis: {
    installs: number;
    store_visitors: number;
    conversion_rate: number;
    day_1_retention: number;
    day_7_retention: number;
    reviews: number;
    rating: number;
    crashes: number;
    anrs: number;
    ads_spend: number;
    cpi: number;
    active_users: number;
    average_session_length: number;
  };
  bottleneck: string;
  evidence: string[];
  confidence_score: number;
  watch_metric: string;
  top_recommendations: Recommendation[];
  next_recommendation: Recommendation | null;
  recent_actions: ManualAction[];
  review_themes: ReviewTheme[];
  latest_report: GrowthReport | null;
  recent_reports: GrowthReport[];
};

export type ApiRoot = {
  name: string;
  status: string;
  version: string;
  endpoints: Record<string, string>;
};

export type ListingAdvisorResult = {
  app: AppProfile;
  listing_snapshot: unknown | null;
  summary: string;
  next_actions: RecommendationDraft[];
};
