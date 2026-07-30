import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { reportService } from "@/services/report.service";
import { historyService } from "@/services/history.service";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FileText, Download, Sparkles, Clock } from "lucide-react";
import { toast } from "sonner";
import { formatDistanceToNow } from "date-fns";

interface Report {
  id: number;
  prediction_id: number;
  title: string;
  summary: string | null;
  content: Record<string, unknown>;
  pdf_path: string | null;
  created_at: string;
}

interface HistoryItem {
  id: number;
  text: string;
  label: number;
  label_name: string;
  confidence: number;
  created_at: string;
}

export default function ReportsPage() {
  const { user } = useAuth();
  const [reports, setReports] = useState<Report[]>([]);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [reportsData, historyData] = await Promise.all([
        reportService.getReports(),
        historyService.getHistory(),
      ]);
      setReports(reportsData.items);
      setHistory(historyData.items);
    } catch (error) {
      toast.error("Failed to load data");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateReport = async (predictionId: number) => {
    try {
      await reportService.createReport(predictionId);
      toast.success("Report generated successfully");
      fetchData();
    } catch (error) {
      toast.error("Failed to generate report");
    }
  };

  const handleDownload = async (report: Report) => {
    if (!report.pdf_path) {
      toast.error("PDF not available");
      return;
    }
    toast.info("Download functionality would be implemented here");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950 flex items-center justify-center">
        <div className="text-slate-500 dark:text-slate-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950">
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent">
            Reports
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-2">
            Generate and download detailed analysis reports
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Existing Reports</h2>
            {reports.length === 0 ? (
              <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
                <CardContent className="p-12 text-center">
                  <FileText className="w-16 h-16 mx-auto mb-4 text-slate-400" />
                  <h3 className="text-lg font-semibold mb-2">No reports yet</h3>
                  <p className="text-slate-500 dark:text-slate-400">
                    Generate reports from your analysis history
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {reports.map((report, index) => (
                  <motion.div
                    key={report.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                  >
                    <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm hover:shadow-md transition-shadow">
                      <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                          <FileText className="w-5 h-5 text-blue-600" />
                          {report.title}
                        </CardTitle>
                        <CardDescription className="flex items-center gap-2">
                          <Clock className="w-3 h-3" />
                          {formatDistanceToNow(new Date(report.created_at), {
                            addSuffix: true,
                          })}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 line-clamp-2">
                          {report.summary || "No summary available"}
                        </p>
                        <Button
                          onClick={() => handleDownload(report)}
                          className="w-full gap-2"
                        >
                          <Download className="w-4 h-4" />
                          Download PDF
                        </Button>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            )}
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Generate New Report</h2>
            {history.length === 0 ? (
              <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
                <CardContent className="p-12 text-center">
                  <Sparkles className="w-16 h-16 mx-auto mb-4 text-slate-400" />
                  <h3 className="text-lg font-semibold mb-2">No analyses yet</h3>
                  <p className="text-slate-500 dark:text-slate-400">
                    Analyze some news first to generate reports
                  </p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {history
                  .filter((item) => !reports.some((r) => r.prediction_id === item.id))
                  .slice(0, 10)
                  .map((item, index) => (
                    <motion.div
                      key={item.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3, delay: index * 0.05 }}
                    >
                      <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm hover:shadow-md transition-shadow">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between gap-4 mb-3">
                            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 flex-1">
                              {item.text}
                            </p>
                            <Badge
                              variant={item.label === 1 ? "default" : "destructive"}
                            >
                              {item.label_name}
                            </Badge>
                          </div>
                          <Button
                            onClick={() => handleGenerateReport(item.id)}
                            className="w-full gap-2"
                            size="sm"
                          >
                            <Sparkles className="w-4 h-4" />
                            Generate Report
                          </Button>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
