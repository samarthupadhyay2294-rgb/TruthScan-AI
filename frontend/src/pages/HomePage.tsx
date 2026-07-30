import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  FileBarChart,
  Shield,
  TrendingUp,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { APP_NAME, FEATURES, ROUTES } from "@/lib/constants";
import { useAuth } from "@/hooks/useAuth";

const iconMap = {
  Brain,
  Zap,
  FileBarChart,
  TrendingUp,
} as const;

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="relative">
      <section className="container mx-auto px-4 py-20 md:py-32">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mx-auto max-w-4xl text-center"
        >
          <Badge variant="secondary" className="mb-6 glass">
            <Shield className="mr-1 h-3 w-3" />
            AI-Powered Misinformation Detection
          </Badge>

          <h1 className="text-4xl font-bold tracking-tight md:text-6xl lg:text-7xl">
            See Through the{" "}
            <span className="gradient-text">Noise</span> with {APP_NAME}
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
            Analyze news articles and text content in real-time. Get confidence
            scores, detailed indicators, and comprehensive reports powered by
            advanced machine learning.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Button asChild size="lg" className="shadow-glow">
              <Link to={ROUTES.ANALYZE}>
                Start Analyzing
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to={ROUTES.DASHBOARD}>View Dashboard</Link>
            </Button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mx-auto mt-16 max-w-5xl"
        >
          <div className="glass-card overflow-hidden rounded-2xl border border-white/20 p-1 shadow-glow">
            <div className="rounded-xl bg-gradient-to-br from-primary/20 via-card to-secondary/20 p-8 md:p-12">
              <div className="grid gap-6 md:grid-cols-3">
                {[
                  { label: "Accuracy", value: "94.2%", color: "text-success" },
                  { label: "Analyses", value: "10K+", color: "text-primary" },
                  { label: "Avg. Response", value: "<2s", color: "text-warning" },
                ].map((stat) => (
                  <div key={stat.label} className="text-center">
                    <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{stat.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      <section id="features" className="border-t border-border/50 bg-muted/30 py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="mb-12 text-center"
          >
            <h2 className="text-3xl font-bold md:text-4xl">Powerful Features</h2>
            <p className="mt-4 text-muted-foreground">
              Everything you need to verify information and combat misinformation
            </p>
          </motion.div>

          <motion.div
            variants={container}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            className="grid gap-6 md:grid-cols-2 lg:grid-cols-4"
          >
            {FEATURES.map((feature) => {
              const Icon = iconMap[feature.icon as keyof typeof iconMap];
              return (
                <motion.div key={feature.title} variants={item}>
                  <Card className="glass-card h-full border-white/10 transition-shadow hover:shadow-glow">
                    <CardHeader>
                      <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                        <Icon className="h-5 w-5 text-primary" />
                      </div>
                      <CardTitle className="text-lg">{feature.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <CardDescription>{feature.description}</CardDescription>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="text-3xl font-bold">How It Works</h2>
            <p className="mt-4 text-muted-foreground">
              Three simple steps to verify any content
            </p>
          </div>

          <div className="mx-auto mt-12 grid max-w-4xl gap-8 md:grid-cols-3">
            {[
              { step: "1", title: "Paste Content", desc: "Enter text or upload a document" },
              { step: "2", title: "AI Analysis", desc: "Our ML models analyze patterns and sources" },
              { step: "3", title: "Get Results", desc: "Receive scores, indicators, and reports" },
            ].map((step, i) => (
              <motion.div
                key={step.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="text-center"
              >
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-gradient-primary text-lg font-bold text-primary-foreground shadow-glow">
                  {step.step}
                </div>
                <h3 className="font-semibold">{step.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
