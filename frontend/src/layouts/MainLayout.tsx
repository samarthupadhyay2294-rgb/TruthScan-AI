import { Link, Outlet } from "react-router-dom";
import { motion } from "framer-motion";
import { Navbar } from "@/components/common/Navbar";
import { Footer } from "@/components/common/Footer";
import { ROUTES } from "@/lib/constants";

export function MainLayout() {
  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden bg-background">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-blue-600/10" />
      <div className="pointer-events-none absolute -left-32 top-20 h-72 w-72 rounded-full bg-primary/10 blur-3xl" />
      <div className="pointer-events-none absolute -right-32 bottom-20 h-72 w-72 rounded-full bg-blue-400/10 blur-3xl" />

      <Navbar variant="marketing" />

      <motion.main
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="relative z-10 flex-1"
      >
        <Outlet />
      </motion.main>

      <Footer />
    </div>
  );
}

export function MainLayoutHero({ children }: { children: React.ReactNode }) {
  return (
    <section className="container mx-auto px-4 py-16 md:py-24">
      <div className="mx-auto max-w-4xl text-center">
        <Link to={ROUTES.HOME} className="mb-8 inline-flex items-center gap-2">
          <img src="/logo.svg" alt="TruthLens AI" className="h-10 w-10" />
          <span className="text-xl font-bold gradient-text">TruthLens AI</span>
        </Link>
        {children}
      </div>
    </section>
  );
}
