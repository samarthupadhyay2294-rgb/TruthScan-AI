import api from "./api";
import type { HistoryFilters, HistoryItem, PaginatedResponse } from "@/types";

interface BackendHistoryItem {
  id: number;
  text: string;
  label: number;
  label_name: string;
  confidence: number;
  source: string;
  filename?: string | null;
  created_at: string;
}

interface BackendHistoryResponse {
  items: BackendHistoryItem[];
  total: number;
  page: number;
  page_size: number;
}

function normalizeLabel(labelName: string): HistoryItem["label"] {
  const upper = labelName.toUpperCase();
  if (upper.includes("FAKE")) return "FAKE";
  if (upper.includes("REAL")) return "REAL";
  return "UNCERTAIN";
}

function mapHistoryItem(item: BackendHistoryItem): HistoryItem {
  return {
    id: String(item.id),
    text_preview: item.text.length > 120 ? `${item.text.slice(0, 120)}...` : item.text,
    label: normalizeLabel(item.label_name),
    confidence: item.confidence,
    created_at: item.created_at,
  };
}

export const historyService = {
  async getHistory(
    filters: HistoryFilters = {}
  ): Promise<PaginatedResponse<HistoryItem>> {
    const page = filters.page ?? 1;
    const pageSize = filters.limit ?? 20;

    const data = await api.get<BackendHistoryResponse>("/history", {
      page,
      page_size: pageSize,
    });

    let items = data.items.map(mapHistoryItem);

    if (filters.label) {
      items = items.filter((item) => item.label === filters.label);
    }

    if (filters.search) {
      const query = filters.search.toLowerCase();
      items = items.filter((item) =>
        item.text_preview.toLowerCase().includes(query)
      );
    }

    return {
      items,
      total: data.total,
      page: data.page,
      limit: data.page_size,
      total_pages: Math.ceil(data.total / data.page_size),
    };
  },

  async deleteHistoryItem(id: string): Promise<void> {
    await api.delete(`/history/${id}`);
  },
};
