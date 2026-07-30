import { Link, NavLink, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  ScanSearch,
  History,
  FileText,
  Settings,
  LogOut,
  Menu,
  User,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { useAuth } from "@/hooks/useAuth";
import { APP_NAME, NAV_ITEMS, ROUTES } from "@/lib/constants";
import { cn, getInitials } from "@/lib/utils";

const iconMap = {
  LayoutDashboard,
  ScanSearch,
  History,
  FileText,
  Settings,
} as const;

interface NavbarProps {
  variant?: "marketing" | "dashboard";
}

export function Navbar({ variant = "marketing" }: NavbarProps) {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate(ROUTES.LOGIN);
  };

  const navLinks =
    variant === "marketing"
      ? [
          { label: "Analyze Tool", href: ROUTES.ANALYZE, isRoute: true },
          { label: "Features", href: "/#features", isRoute: false },
          { label: "How it Works", href: "/#how-it-works", isRoute: false },
        ]
      : [];

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to={ROUTES.HOME} className="flex items-center gap-2">
          <img src="/logo.svg" alt={APP_NAME} className="h-8 w-8" />
          <span className="hidden font-bold gradient-text sm:inline">{APP_NAME}</span>
        </Link>

        {variant === "marketing" && (
          <nav className="hidden items-center gap-6 md:flex">
            {navLinks.map((link) =>
              link.isRoute ? (
                <Link
                  key={link.href}
                  to={link.href}
                  className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link.label}
                </Link>
              ) : (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                >
                  {link.label}
                </a>
              )
            )}
          </nav>
        )}

        <div className="flex items-center gap-2">
          <ThemeToggle />

          {isAuthenticated ? (
            <>
              {variant === "marketing" && (
                <Button asChild size="sm" className="hidden sm:inline-flex">
                  <Link to={ROUTES.DASHBOARD}>Dashboard</Link>
                </Button>
              )}

              {variant === "dashboard" && (
                <Sheet>
                  <SheetTrigger asChild>
                    <Button variant="ghost" size="icon" className="lg:hidden">
                      <Menu className="h-5 w-5" />
                    </Button>
                  </SheetTrigger>
                  <SheetContent side="left" className="w-64 pt-10">
                    <nav className="flex flex-col gap-1">
                      {NAV_ITEMS.map((item) => {
                        const Icon = iconMap[item.icon as keyof typeof iconMap];
                        return (
                          <NavLink
                            key={item.href}
                            to={item.href}
                            className={({ isActive }) =>
                              cn(
                                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                                isActive
                                  ? "bg-primary/10 text-primary"
                                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
                              )
                            }
                          >
                            <Icon className="h-4 w-4" />
                            {item.label}
                          </NavLink>
                        );
                      })}
                    </nav>
                  </SheetContent>
                </Sheet>
              )}

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-9 w-9 rounded-full">
                    <Avatar className="h-9 w-9">
                      <AvatarFallback className="bg-primary/10 text-primary">
                        {getInitials(user?.name ?? "U")}
                      </AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>
                    <div className="flex flex-col">
                      <span>{user?.name}</span>
                      <span className="text-xs font-normal text-muted-foreground">
                        {user?.email}
                      </span>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => navigate(ROUTES.PROFILE)}>
                    <User className="mr-2 h-4 w-4" />
                    Profile
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate(ROUTES.SETTINGS)}>
                    <Settings className="mr-2 h-4 w-4" />
                    Settings
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout} className="text-destructive">
                    <LogOut className="mr-2 h-4 w-4" />
                    Log out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Button asChild variant="ghost" size="sm">
                <Link to={ROUTES.LOGIN}>Sign in</Link>
              </Button>
              <Button asChild size="sm">
                <Link to={ROUTES.REGISTER}>Get Started</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export function NavbarBrand() {
  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      className="flex items-center gap-2"
    >
      <img src="/logo.svg" alt={APP_NAME} className="h-8 w-8" />
      <span className="font-bold gradient-text">{APP_NAME}</span>
    </motion.div>
  );
}
