/**
 * Prefix a root-absolute path with `import.meta.env.BASE_URL` (GitHub Pages project sites).
 * Examples: `/blog/slug/`, `/favicon.svg`, `/`.
 */
export function withBase(absolutePath: string): string {
  const base = import.meta.env.BASE_URL;
  if (!absolutePath.startsWith('/')) {
    const b = base.replace(/\/?$/, '/');
    return b + absolutePath.replace(/^\//, '');
  }
  const rest = absolutePath.slice(1);
  if (!rest) {
    return base === '/' ? '/' : base.endsWith('/') ? base : `${base}/`;
  }
  const root = base === '/' ? '' : base.replace(/\/$/, '');
  return `${root}/${rest}`;
}

/** Full site URL for a root-absolute path (Open Graph, etc.). */
export function siteUrl(absolutePath: string, site: string | URL): string {
  const path = withBase(absolutePath).replace(/^\//, '');
  const base = typeof site === 'string' ? site : site.href;
  const normalized = base.replace(/\/?$/, '/');
  return new URL(path, normalized).href;
}
