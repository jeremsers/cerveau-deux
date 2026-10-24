/**
 * Configuration Tailwind (Play CDN) du Command Center.
 * Fichier externe plutôt que script inline : la Content-Security-Policy n'autorise
 * aucun script inline (v0.5.2, D2).
 */
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        cyber: {
          950: "#070a12",
          900: "#0d1322",
          850: "#111827",
          800: "#131b2e",
          700: "#1f293d",
          cyan: "#38bdf8",
          blue: "#3b82f6",
          purple: "#8b5cf6",
          emerald: "#10b981",
          amber: "#f59e0b",
          rose: "#f43f5e",
        },
      },
    },
  },
};
