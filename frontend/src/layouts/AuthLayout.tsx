import { Outlet } from "react-router-dom";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { APP_NAME, ROUTES } from "@/lib/constants";

export function AuthLayout() {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background p-4">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-primary/10 via-background to-secondary/20" />
      <div className="pointer-events-none absolute -left-20 top-1/4 h-96 w-96 rounded-full bg-primary/20 blur-3xl" />
      <div className="pointer-events-none absolute -right-20 bottom-1/4 h-96 w-96 rounded-full bg-blue-500/15 blur-3xl" />

      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="mb-8 text-center">
          <Link to={ROUTES.HOME} className="inline-flex items-center gap-3">
            <img src="/logo.svg" alt={APP_NAME} className="h-12 w-12 drop-shadow-glow" />
            <span className="text-2xl font-bold gradient-text">{APP_NAME}</span>
          </Link>
          <p className="mt-2 text-sm text-muted-foreground">
            Detect misinformation with AI-powered analysis
          </p>
        </div>

        <div className="glass-card border border-white/20 bg-card/80 p-6 shadow-glass backdrop-blur-xl md:p-8">
          <Outlet />
        </div>
      </motion.div>
    </div>
  );
}
