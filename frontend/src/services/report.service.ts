import api from "./api";
import type { Report, ReportSection } from "@/types";

interface BackendReport {
  id: number;
  prediction_id: number;
  title: string;
  summary: string | null;
  content: Record<string, unknown>;
  pdf_path: string | null;
  created_at: string;
}

interface BackendReportList {
  items: BackendReport[];
  total: number;
}

function mapContent(content: Record<string, unknown>): ReportSection[] {
  if (Array.isArray(content.sections)) {
    return content.sections as ReportSection[];
  }

  const sections: ReportSection[] = [];

  if (content.summary) {
    sections.push({
      title: "Summary",
      content: String(content.summary),
      type: "text",
    });
  }

  if (content.analysis) {
    sections.push({
      title: "Analysis",
      content: JSON.stringify(content.analysis, null, 2),
      type: "text",
    });
  }

  if (content.indicators && Array.isArray(content.indicators)) {
    sections.push({
      title: "Indicators",
      content: "Key indicators from the analysis",
      type: "indicator",
      data: { indicators: content.indicators },
    });
  }

  if (sections.length === 0) {
    sections.push({
      title: "Report Content",
      content: JSON.stringify(content, null, 2),
      type: "text",
    });
  }

  return sections;
}

function mapReport(data: BackendReport): Report {
  return {
    id: String(data.id),
    title: data.title,
    prediction_id: String(data.prediction_id),
    summary: data.summary ?? "",
    content: mapContent(data.content),
    generated_at: data.created_at,
    format: data.pdf_path ? "pdf" : "html",
  };
}

export const reportService = {
  async listReports(skip = 0, limit = 50): Promise<{ items: Report[]; total: number }> {
    const data = await api.get<BackendReportList>("/reports", { skip, limit });
    return {
      items: data.items.map(mapReport),
      total: data.total,
    };
  },

  async createReport(predictionId: string): Promise<Report> {
    const data = await api.post<BackendReport>(`/reports/${predictionId}`);
    return mapReport(data);
  },

  async getReport(id: string): Promise<Report | null> {
    const { items } = await this.listReports();
    return items.find((report) => report.id === id) ?? null;
  },
};
