/**
 * Public base path for client-side asset fetches and plain <a> download links.
 *
 * Next.js Link components automatically prepend basePath — this constant is only
 * needed for raw fetch() calls and non-Link <a href> attributes.
 *
 * Set NEXT_PUBLIC_BASE_PATH=/wgu-atlas in the GitHub Actions workflow.
 * Omit (or set to "") for local dev.
 */
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
