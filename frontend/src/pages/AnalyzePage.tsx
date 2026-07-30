import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { usePrediction } from "@/hooks/usePrediction";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Upload, FileText, AlertCircle, CheckCircle, Brain, Sparkles, Info } from "lucide-react";
import { toast } from "sonner";
import { ROUTES } from "@/lib/constants";

export default function AnalyzePage() {
  const { isAuthenticated } = useAuth();
  const { analyze, uploadFile, currentPrediction, isAnalyzing, error } = usePrediction();
  const [text, setText] = useState("");

  const handleAnalyze = async () => {
    const sanitizedText = text.trim();
    if (sanitizedText.length < 10) {
      toast.error("Please enter at least 10 characters");
      return;
    }

    try {
      await analyze({ text: sanitizedText });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Analysis failed";
      toast.error(message);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 10 * 1024 * 1024) {
      toast.error("File size must be less than 10MB");
      return;
    }

    const allowedTypes = ["text/plain", "application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];
    if (!allowedTypes.includes(file.type)) {
      toast.error("Only TXT, PDF, and DOCX files are supported");
      return;
    }

    await uploadFile(file);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.85) return "bg-green-500";
    if (confidence >= 0.65) return "bg-yellow-500";
    return "bg-red-500";
  };

  const getLabelColor = (label: string) => {
    if (label === "REAL") return "text-green-600 bg-green-50 dark:bg-green-950/30";
    if (label === "FAKE") return "text-red-600 bg-red-50 dark:bg-red-950/30";
    return "text-yellow-600 bg-yellow-50 dark:bg-yellow-950/30";
  };

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
            Analyze News
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-2">
            Detect fake news with AI-powered analysis
          </p>

          {!isAuthenticated && (
            <div className="mt-4 p-4 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 text-sm text-blue-900 dark:text-blue-200">
                <Info className="w-5 h-5 text-blue-500 shrink-0" />
                <span>You are analyzing as a guest. Feel free to use the tool! <Link to={ROUTES.LOGIN} className="underline font-medium hover:text-blue-600">Sign in</Link> or <Link to={ROUTES.REGISTER} className="underline font-medium hover:text-blue-600">Create an account</Link> to save prediction history and export PDF reports.</span>
              </div>
            </div>
          )}
        </motion.div>

        <Tabs defaultValue="text" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 max-w-md">
            <TabsTrigger value="text" className="gap-2">
              <FileText className="w-4 h-4" />
              Paste Text
            </TabsTrigger>
            <TabsTrigger value="upload" className="gap-2">
              <Upload className="w-4 h-4" />
              Upload File
            </TabsTrigger>
          </TabsList>

          <TabsContent value="text" className="space-y-6">
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Enter News Text</CardTitle>
                <CardDescription>
                  Paste the news article or text you want to analyze
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste your news text here..."
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  className="min-h-[200px] resize-none"
                  disabled={isAnalyzing}
                />
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-500 dark:text-slate-400">
                    {text.length} characters
                  </span>
                  <Button
                    onClick={handleAnalyze}
                    disabled={isAnalyzing || text.length < 10}
                    className="gap-2"
                  >
                    {isAnalyzing ? (
                      <>
                        <Sparkles className="w-4 h-4 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Brain className="w-4 h-4" />
                        Analyze
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="upload" className="space-y-6">
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Upload File</CardTitle>
                <CardDescription>
                  Upload a TXT, PDF, or DOCX file for analysis
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-lg p-8 text-center hover:border-blue-500 dark:hover:border-blue-500 transition-colors">
                  <input
                    type="file"
                    accept=".txt,.pdf,.docx"
                    onChange={handleFileUpload}
                    disabled={isAnalyzing}
                    className="hidden"
                    id="file-upload"
                  />
                  <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex flex-col items-center gap-4"
                  >
                    <Upload className="w-12 h-12 text-slate-400" />
                    <div>
                      <p className="font-medium text-slate-900 dark:text-slate-100">
                        Click to upload or drag and drop
                      </p>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                        TXT, PDF, DOCX up to 10MB
                      </p>
                    </div>
                  </label>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-800 dark:bg-red-950/30 dark:text-red-300"
          >
            {error}
          </motion.div>
        )}

        {currentPrediction && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-blue-600" />
                  Analysis Result
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="flex items-center justify-between">
                  <Badge
                    className={`text-lg px-4 py-2 ${getLabelColor(currentPrediction.label)}`}
                  >
                    {currentPrediction.label === "REAL" ? (
                      <CheckCircle className="w-4 h-4 mr-2" />
                    ) : (
                      <AlertCircle className="w-4 h-4 mr-2" />
                    )}
                    {currentPrediction.label}
                  </Badge>
                  <div className="text-right">
                    <p className="text-sm text-slate-500 dark:text-slate-400">Confidence</p>
                    <p className="text-2xl font-bold">
                      {(currentPrediction.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Real Score</span>
                    <span>{(currentPrediction.real_score * 100).toFixed(1)}%</span>
                  </div>
                  <Progress value={currentPrediction.real_score * 100} className="h-2" />
                  <div className="flex justify-between text-sm">
                    <span>Fake Score</span>
                    <span>{(currentPrediction.fake_score * 100).toFixed(1)}%</span>
                  </div>
                  <Progress value={currentPrediction.fake_score * 100} className="h-2" />
                </div>

                <div className="space-y-3">
                  <h3 className="font-semibold">Key Indicators</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {currentPrediction.indicators.slice(0, 6).map((indicator, index) => (
                      <div
                        key={index}
                        className="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-800/50"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-medium text-sm">{indicator.name}</span>
                          <Badge
                            variant={
                              indicator.severity === "high"
                                ? "destructive"
                                : indicator.severity === "medium"
                                  ? "default"
                                  : "secondary"
                            }
                            className="text-xs"
                          >
                            {indicator.severity}
                          </Badge>
                        </div>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          {indicator.description}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
                  <h3 className="font-semibold mb-2">Analyzed Text</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-4">
                    {currentPrediction.text}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  );
}
