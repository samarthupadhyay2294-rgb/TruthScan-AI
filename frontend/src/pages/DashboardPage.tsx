import { motion } from "framer-motion";
import { useAuth } from "@/hooks/useAuth";
import { useDashboard } from "@/hooks/useApi";
import { StatsCards } from "@/components/dashboard/StatsCards";
import { RecentPredictions } from "@/components/dashboard/RecentPredictions";
import { ActivityChart } from "@/components/dashboard/ActivityChart";
import { PageLoader } from "@/components/common/Loader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3, TrendingUp, Shield, AlertTriangle } from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: dashboard, isLoading } = useDashboard();

  if (isLoading) {
    return <PageLoader />;
  }

  const stats = dashboard?.stats;
  const recent = dashboard?.recent_predictions || [];
  const trend = dashboard?.trend || [];

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
            Welcome back, {user?.name || "User"}!
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-2">
            Here's your fake news detection overview
          </p>
        </motion.div>

        <StatsCards stats={stats} />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <div className="lg:col-span-2">
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                  Activity Trend
                </CardTitle>
                <CardDescription>Your prediction history over time</CardDescription>
              </CardHeader>
              <CardContent>
                <ActivityChart data={trend} />
              </CardContent>
            </Card>
          </div>

          <div>
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="w-5 h-5 text-green-600" />
                  Quick Stats
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-green-50 dark:bg-green-950/30 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Shield className="w-4 h-4 text-green-600" />
                    <span className="text-sm font-medium">Real News</span>
                  </div>
                  <span className="text-lg font-bold text-green-600">
                    {stats?.real_count || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between p-3 bg-red-50 dark:bg-red-950/30 rounded-lg">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-red-600" />
                    <span className="text-sm font-medium">Fake News</span>
                  </div>
                  <span className="text-lg font-bold text-red-600">
                    {stats?.fake_count || 0}
                  </span>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg">
                  <div className="flex items-center gap-2">
                    <BarChart3 className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium">Avg Confidence</span>
                  </div>
                  <span className="text-lg font-bold text-blue-600">
                    {((stats?.avg_confidence || 0) * 100).toFixed(1)}%
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-6"
        >
          <RecentPredictions predictions={recent} />
        </motion.div>
      </div>
    </div>
  );
}
