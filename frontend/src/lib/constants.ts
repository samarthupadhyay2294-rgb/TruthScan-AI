export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export const APP_NAME = import.meta.env.VITE_APP_NAME || "TruthLens AI";
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || "1.0.0";

export const STORAGE_KEYS = {
  ACCESS_TOKEN: "truthlens_access_token",
  REFRESH_TOKEN: "truthlens_refresh_token",
  USER: "truthlens_user",
  THEME: "truthlens_theme",
} as const;

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  DASHBOARD: "/dashboard",
  ANALYZE: "/analyze",
  HISTORY: "/history",
  REPORTS: "/reports",
  SETTINGS: "/settings",
  PROFILE: "/profile",
  ABOUT: "/about",
  CONTACT: "/contact",
  ADMIN: "/admin",
} as const;

export const PREDICTION_LABELS = {
  REAL: "Real",
  FAKE: "Fake",
  UNCERTAIN: "Uncertain",
} as const;

export const CONFIDENCE_THRESHOLDS = {
  HIGH: 0.85,
  MEDIUM: 0.65,
  LOW: 0.45,
} as const;

export const NAV_ITEMS = [
  { label: "Dashboard", href: ROUTES.DASHBOARD, icon: "LayoutDashboard" },
  { label: "Analyze", href: ROUTES.ANALYZE, icon: "ScanSearch" },
  { label: "History", href: ROUTES.HISTORY, icon: "History" },
  { label: "Reports", href: ROUTES.REPORTS, icon: "FileText" },
  { label: "Settings", href: ROUTES.SETTINGS, icon: "Settings" },
] as const;

export const FEATURES = [
  {
    title: "AI-Powered Analysis",
    description:
      "Advanced machine learning models analyze text patterns, sources, and linguistic markers to detect misinformation.",
    icon: "Brain",
  },
  {
    title: "Real-Time Detection",
    description:
      "Get instant credibility scores and detailed breakdowns for any news article or text content.",
    icon: "Zap",
  },
  {
    title: "Detailed Reports",
    description:
      "Comprehensive analysis reports with confidence scores, key indicators, and source verification.",
    icon: "FileBarChart",
  },
  {
    title: "History Tracking",
    description:
      "Track all your analyses over time with searchable history and trend visualization.",
    icon: "TrendingUp",
  },
] as const;
