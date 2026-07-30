import api from "./api";
import type {
  PredictionIndicator,
  PredictionRequest,
  PredictionResult,
} from "@/types";

interface BackendPredictResponse {
  prediction: {
    id: number;
    text: string;
    label: number;
    label_name: string;
    confidence: number;
    source: string;
    filename?: string | null;
    analysis?: Record<string, unknown> | null;
    created_at: string;
  };
  explainability: {
    top_keywords: Array<{ word?: string; keyword?: string; score?: number; weight?: number }>;
    suspicious_words: string[];
  };
  ai_analysis: {
    summary?: string | null;
    keywords?: string[];
    sentiment?: Record<string, unknown> | null;
    credibility_score?: number | null;
    bias?: Record<string, unknown> | null;
  };
}

function normalizeLabel(labelName: string): PredictionResult["label"] {
  const upper = labelName.toUpperCase();
  if (upper.includes("FAKE")) return "FAKE";
  if (upper.includes("REAL")) return "REAL";
  return "UNCERTAIN";
}

function mapPrediction(data: BackendPredictResponse): PredictionResult {
  const { prediction, explainability, ai_analysis } = data;
  const label = normalizeLabel(prediction.label_name);
  const fakeScore = label === "FAKE" ? prediction.confidence : 1 - prediction.confidence;
  const realScore = label === "REAL" ? prediction.confidence : 1 - prediction.confidence;

  const indicators: PredictionIndicator[] = [];

  explainability.suspicious_words.slice(0, 5).forEach((word, index) => {
    indicators.push({
      name: word,
      value: Math.max(0.5, prediction.confidence - index * 0.05),
      description: `Suspicious language pattern detected: "${word}"`,
      severity: index < 2 ? "high" : index < 4 ? "medium" : "low",
    });
  });

  explainability.top_keywords.slice(0, 5).forEach((kw, index) => {
    const name = kw.word || kw.keyword || `Keyword ${index + 1}`;
    indicators.push({
      name,
      value: kw.score ?? kw.weight ?? 0.5,
      description: `Key term influencing classification: "${name}"`,
      severity: "medium",
    });
  });

  if (ai_analysis.credibility_score != null) {
    indicators.push({
      name: "Credibility Score",
      value: ai_analysis.credibility_score,
      description: "AI-assessed source and content credibility",
      severity:
        ai_analysis.credibility_score < 0.4
          ? "high"
          : ai_analysis.credibility_score < 0.7
            ? "medium"
            : "low",
    });
  }

  return {
    id: String(prediction.id),
    text: prediction.text,
    label,
    confidence: prediction.confidence,
    real_score: realScore,
    fake_score: fakeScore,
    indicators,
    created_at: prediction.created_at,
  };
}

export const predictionService = {
  async analyze(request: PredictionRequest): Promise<PredictionResult> {
    const data = await api.post<BackendPredictResponse>("/predict", {
      text: request.text,
    });
    return mapPrediction(data);
  },

  async uploadFile(file: File): Promise<PredictionResult> {
    const formData = new FormData();
    formData.append("file", file);
    const data = await api.post<BackendPredictResponse>("/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return mapPrediction(data);
  },
};
