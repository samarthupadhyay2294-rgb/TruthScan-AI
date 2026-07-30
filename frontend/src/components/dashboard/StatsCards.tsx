import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { BarChart3, Shield, AlertTriangle, TrendingUp } from "lucide-react";

interface StatsCardsProps {
  stats?: {
    total_predictions: number;
    fake_count: number;
    real_count: number;
    avg_confidence: number;
    fake_percentage: number;
    real_percentage: number;
  };
}

export function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      title: "Total Predictions",
      value: stats?.total_predictions || 0,
      icon: BarChart3,
      color: "blue",
      description: "All-time analyses",
    },
    {
      title: "Fake News Detected",
      value: stats?.fake_count || 0,
      icon: AlertTriangle,
      color: "red",
      description: `${stats?.fake_percentage?.toFixed(1) || 0}% of total`,
    },
    {
      title: "Real News Verified",
      value: stats?.real_count || 0,
      icon: Shield,
      color: "green",
      description: `${stats?.real_percentage?.toFixed(1) || 0}% of total`,
    },
    {
      title: "Avg Confidence",
      value: `${((stats?.avg_confidence || 0) * 100).toFixed(1)}%`,
      icon: TrendingUp,
      color: "purple",
      description: "Model accuracy",
    },
  ];

  const colorClasses = {
    blue: "from-blue-500 to-blue-600 bg-blue-50 dark:bg-blue-950/30",
    red: "from-red-500 to-red-600 bg-red-50 dark:bg-red-950/30",
    green: "from-green-500 to-green-600 bg-green-50 dark:bg-green-950/30",
    purple: "from-purple-500 to-purple-600 bg-purple-50 dark:bg-purple-950/30",
  };

  const iconColors = {
    blue: "text-blue-600",
    red: "text-red-600",
    green: "text-green-600",
    purple: "text-purple-600",
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className="border-2 border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-600 dark:text-slate-400">
                      {card.title}
                    </p>
                    <h3 className="text-3xl font-bold mt-2 bg-gradient-to-r from-slate-900 to-slate-700 dark:from-slate-100 dark:to-slate-300 bg-clip-text text-transparent">
                      {card.value}
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
                      {card.description}
                    </p>
                  </div>
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${colorClasses[card.color as keyof typeof colorClasses]}`}>
                    <Icon className={`w-6 h-6 ${iconColors[card.color as keyof typeof iconColors]}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        );
      })}
    </div>
  );
}
