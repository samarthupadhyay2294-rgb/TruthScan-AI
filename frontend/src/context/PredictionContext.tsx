import {
  createContext,
  useCallback,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { predictionService } from "@/services/prediction.service";
import { historyService } from "@/services/history.service";
import type {
  HistoryItem,
  PredictionRequest,
  PredictionResult,
} from "@/types";

interface PredictionContextValue {
  currentPrediction: PredictionResult | null;
  isAnalyzing: boolean;
  error: string | null;
  history: HistoryItem[];
  analyze: (request: PredictionRequest) => Promise<PredictionResult>;
  clearPrediction: () => void;
  loadHistory: () => Promise<void>;
  deleteHistoryItem: (id: string) => Promise<void>;
}

export const PredictionContext = createContext<PredictionContextValue | null>(
  null
);

export function PredictionProvider({ children }: { children: ReactNode }) {
  const [currentPrediction, setCurrentPrediction] =
    useState<PredictionResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  const analyze = useCallback(async (request: PredictionRequest) => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const result = await predictionService.analyze(request);
      setCurrentPrediction(result);
      return result;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Analysis failed";
      setError(message);
      throw err;
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  const clearPrediction = useCallback(() => {
    setCurrentPrediction(null);
    setError(null);
  }, []);

  const loadHistory = useCallback(async () => {
    try {
      const response = await historyService.getHistory({ limit: 50 });
      setHistory(response.items);
    } catch {
      setHistory([]);
    }
  }, []);

  const deleteHistoryItem = useCallback(async (id: string) => {
    await historyService.deleteHistoryItem(id);
    setHistory((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const value = useMemo(
    () => ({
      currentPrediction,
      isAnalyzing,
      error,
      history,
      analyze,
      clearPrediction,
      loadHistory,
      deleteHistoryItem,
    }),
    [
      currentPrediction,
      isAnalyzing,
      error,
      history,
      analyze,
      clearPrediction,
      loadHistory,
      deleteHistoryItem,
    ]
  );

  return (
    <PredictionContext.Provider value={value}>
      {children}
    </PredictionContext.Provider>
  );
}
