import api from "./api";
import type { ChartDataPoint, DashboardStats, HistoryItem } from "@/types";

interface BackendDashboardResponse {
  stats: {
    total_predictions: number;
    fake_count: number;
    real_count: number;
    avg_confidence: number;
    fake_percentage: number;
    real_percentage: number;
  };
  recent_predictions: Array<{
    id: number;
    text: string;
    label: number;
    label_name: string;
    confidence: number;
    created_at: string;
  }>;
  trend: Array<Record<string, unknown>>;
}

function normalizeLabel(labelName: string): HistoryItem["label"] {
  const upper = labelName.toUpperCase();
  if (upper.includes("FAKE")) return "FAKE";
  if (upper.includes("REAL")) return "REAL";
  return "UNCERTAIN";
}

function mapTrend(trend: Array<Record<string, unknown>>): ChartDataPoint[] {
  return trend.map((point) => ({
    date: String(point.date ?? point.day ?? point.created_at ?? ""),
    real: Number(point.real ?? point.real_count ?? 0),
    fake: Number(point.fake ?? point.fake_count ?? 0),
    total: Number(point.total ?? point.count ?? 0),
  }));
}

export interface DashboardData {
  stats: DashboardStats;
  recentPredictions: HistoryItem[];
  trend: ChartDataPoint[];
}

export const dashboardService = {
  async getDashboard(): Promise<DashboardData> {
    const data = await api.get<BackendDashboardResponse>("/dashboard");

    const stats: DashboardStats = {
      total_analyses: data.stats.total_predictions,
      fake_detected: data.stats.fake_count,
      real_verified: data.stats.real_count,
      average_confidence: data.stats.avg_confidence,
      analyses_today: 0,
      analyses_this_week: 0,
      fake_percentage: data.stats.fake_percentage,
      real_percentage: data.stats.real_percentage,
    };

    const recentPredictions: HistoryItem[] = data.recent_predictions.map(
      (item) => ({
        id: String(item.id),
        text_preview:
          item.text.length > 120 ? `${item.text.slice(0, 120)}...` : item.text,
        label: normalizeLabel(item.label_name),
        confidence: item.confidence,
        created_at: item.created_at,
      })
    );

    return {
      stats,
      recentPredictions,
      trend: mapTrend(data.trend),
    };
  },
};
