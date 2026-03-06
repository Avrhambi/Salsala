/**
 * Design tokens — enforces the 60-30-10 color rule and 8px spacing rhythm
 * from FRONTEND_CORE.md. All visual constants live here; no magic values
 * in component files.
 */

export const Colors = {
  // 60% — base / background
  background: "#F5F5F0",
  surface: "#FFFFFF",

  // 30% — secondary / cards / nav
  secondary: "#2D3A4A",
  textPrimary: "#1A1A2E",
  textSecondary: "#6B7280",
  border: "#E5E7EB",

  // 10% — accent / CTA
  accent: "#2E86AB",
  accentLight: "#D0EAF4",
  success: "#22C55E",
  error: "#EF4444",
  warning: "#F59E0B",
} as const;

/** All spacing values are multiples of 8 (rhythm from FRONTEND_CORE.md). */
export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
} as const;

export const BorderRadius = {
  sm: 8,
  md: 12,
  lg: 16,
} as const;

/** Minimum touch target — 44pt per MOBILE_NATIVE_FRONT.md. */
export const MIN_TOUCH_TARGET = 44;

export const FontSize = {
  xs: 12,
  sm: 14,
  md: 16,
  lg: 20,
  xl: 24,
  xxl: 30,
} as const;

export const FontWeight = {
  regular: "400" as const,
  medium: "500" as const,
  bold: "700" as const,
};
