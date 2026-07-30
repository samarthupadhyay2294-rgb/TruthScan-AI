import { NavLink, Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  ScanSearch,
  History,
  FileText,
  Settings,
  ChevronLeft,
  ChevronRight,
  LogIn,
} from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { APP_NAME, NAV_ITEMS, ROUTES } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";

const iconMap = {
  LayoutDashboard,
  ScanSearch,
  History,
  FileText,
  Settings,
} as const;

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const { isAuthenticated } = useAuth();

  return (
    <motion.aside
      initial={false}
      animate={{ width: collapsed ? 80 : 256 }}
      className="fixed left-0 top-0 z-40 hidden h-screen flex-col border-r border-border/50 bg-card/80 backdrop-blur-xl lg:flex"
    >
      <div className="flex h-16 items-center justify-between px-4">
        {!collapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2"
          >
            <img src="/logo.svg" alt={APP_NAME} className="h-8 w-8" />
            <span className="text-sm font-bold gradient-text">{APP_NAME}</span>
          </motion.div>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setCollapsed(!collapsed)}
          className={cn(collapsed && "mx-auto")}
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </Button>
      </div>

      <Separator />

      <nav className="flex-1 space-y-1 p-3">
        {NAV_ITEMS.map((item) => {
          const Icon = iconMap[item.icon as keyof typeof iconMap];
          return (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                  isActive
                    ? "bg-gradient-primary text-primary-foreground shadow-glow"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground",
                  collapsed && "justify-center px-2"
                )
              }
              title={collapsed ? item.label : undefined}
            >
              <Icon className="h-5 w-5 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </NavLink>
          );
        })}
      </nav>

      <div className="p-4 space-y-3">
        {!isAuthenticated && (
          <Button asChild variant="outline" size="sm" className="w-full justify-center gap-2">
            <Link to={ROUTES.LOGIN}>
              <LogIn className="h-4 w-4" />
              {!collapsed && <span>Sign In</span>}
            </Link>
          </Button>
        )}
        {!collapsed && (
          <div className="glass-card rounded-lg p-3 text-xs text-muted-foreground">
            <p className="font-medium text-foreground">Pro Tip</p>
            <p className="mt-1">
              Paste full article text for the most accurate analysis results.
            </p>
          </div>
        )}
      </div>
    </motion.aside>
  );
}
