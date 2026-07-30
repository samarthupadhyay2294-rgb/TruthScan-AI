import { Link } from "react-router-dom";
import { Github, Twitter, Mail } from "lucide-react";
import { APP_NAME, ROUTES } from "@/lib/constants";
import { Separator } from "@/components/ui/separator";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative z-10 border-t border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 py-12">
        <div className="grid gap-8 md:grid-cols-4">
          <div className="md:col-span-2">
            <Link to={ROUTES.HOME} className="inline-flex items-center gap-2">
              <img src="/logo.svg" alt={APP_NAME} className="h-8 w-8" />
              <span className="font-bold gradient-text">{APP_NAME}</span>
            </Link>
            <p className="mt-3 max-w-sm text-sm text-muted-foreground">
              Advanced AI-powered fake news detection. Analyze articles, verify
              sources, and make informed decisions with confidence scores and
              detailed reports.
            </p>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-semibold">Product</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to={ROUTES.ANALYZE} className="hover:text-foreground">
                  Analyze
                </Link>
              </li>
              <li>
                <Link to={ROUTES.DASHBOARD} className="hover:text-foreground">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link to={ROUTES.HISTORY} className="hover:text-foreground">
                  History
                </Link>
              </li>
              <li>
                <Link to={ROUTES.REPORTS} className="hover:text-foreground">
                  Reports
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="mb-3 text-sm font-semibold">Account</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to={ROUTES.LOGIN} className="hover:text-foreground">
                  Sign in
                </Link>
              </li>
              <li>
                <Link to={ROUTES.REGISTER} className="hover:text-foreground">
                  Register
                </Link>
              </li>
              <li>
                <Link to={ROUTES.SETTINGS} className="hover:text-foreground">
                  Settings
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <Separator className="my-8" />

        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <p className="text-sm text-muted-foreground">
            © {currentYear} {APP_NAME}. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-muted-foreground">
            <a href="https://github.com" target="_blank" rel="noreferrer" aria-label="GitHub">
              <Github className="h-4 w-4 hover:text-foreground" />
            </a>
            <a href="https://twitter.com" target="_blank" rel="noreferrer" aria-label="Twitter">
              <Twitter className="h-4 w-4 hover:text-foreground" />
            </a>
            <a href="mailto:support@truthlens.ai" aria-label="Email">
              <Mail className="h-4 w-4 hover:text-foreground" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
