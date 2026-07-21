import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { ThemeProvider } from "@/providers/theme-provider";
import { Toaster } from "@/components/ui/sonner";

function NotFoundComponent() {
  return (
    <div className="min-h-screen grid place-items-center px-4 mesh-bg">
      <div className="text-center">
        <div className="text-8xl font-bold gradient-text tracking-tight">404</div>
        <h2 className="mt-4 text-xl font-semibold">Molecule not found</h2>
        <p className="mt-2 text-sm text-muted-foreground max-w-sm">
          The compound you're searching for isn't in our database.
        </p>
        <a href="/" className="mt-6 inline-flex items-center rounded-full px-5 py-2 text-sm font-medium text-white"
          style={{ background: "var(--gradient-primary)" }}>Back to home</a>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();
  useEffect(() => { reportLovableError(error, { boundary: "tanstack_root_error_component" }); }, [error]);
  return (
    <div className="min-h-screen grid place-items-center px-4">
      <div className="text-center max-w-md">
        <h1 className="text-xl font-semibold">Something went wrong</h1>
        <p className="mt-2 text-sm text-muted-foreground">{error.message}</p>
        <button
          onClick={() => { router.invalidate(); reset(); }}
          className="mt-6 rounded-full px-5 py-2 text-sm font-medium text-white"
          style={{ background: "var(--gradient-primary)" }}
        >Try again</button>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "DrugAI — Accelerating Drug Discovery with AI" },
      { name: "description", content: "AI-powered drug discovery platform for toxicity prediction, ADMET profiling, drug-target interaction, and explainable molecular intelligence." },
      { name: "author", content: "DrugAI Intelligence" },
      { property: "og:title", content: "DrugAI — Accelerating Drug Discovery with AI" },
      { property: "og:description", content: "AI-powered drug discovery platform for toxicity prediction, ADMET profiling, drug-target interaction, and explainable molecular intelligence." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: "DrugAI — Accelerating Drug Discovery with AI" },
      { name: "twitter:description", content: "AI-powered drug discovery platform for toxicity prediction, ADMET profiling, drug-target interaction, and explainable molecular intelligence." },
      { property: "og:image", content: "https://storage.googleapis.com/gpt-engineer-file-uploads/attachments/og-images/4b920af7-947a-4df7-8aa9-a73830166eb9" },
      { name: "twitter:image", content: "https://storage.googleapis.com/gpt-engineer-file-uploads/attachments/og-images/4b920af7-947a-4df7-8aa9-a73830166eb9" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "icon", href: "/favicon.ico", type: "image/x-icon" },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="dark">
      <head>
        <HeadContent />
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <Outlet />
        <Toaster />
      </ThemeProvider>
    </QueryClientProvider>
  );
}
