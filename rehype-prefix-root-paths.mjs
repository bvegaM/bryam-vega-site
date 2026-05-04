/**
 * Prefix root-absolute img src / a href in markdown HTML for non-root `base` deploys.
 */
export function rehypePrefixRootPaths(base) {
  const needPrefix = base && base !== '/';
  const prefix = needPrefix ? base.replace(/\/$/, '') : '';

  return function rehypePrefixRootPathsPlugin() {
    return (tree) => {
      if (!needPrefix) return;
      walk(tree);
    };

    function walk(node) {
      if (!node || typeof node !== 'object') return;
      if (node.type === 'element') {
        const tag = node.tagName;
        if (tag === 'img' && node.properties?.src != null) {
          const src = String(node.properties.src);
          if (src.startsWith('/') && !src.startsWith('//')) {
            node.properties.src = prefix + src;
          }
        }
        if (tag === 'a' && node.properties?.href != null) {
          const href = String(node.properties.href);
          if (href.startsWith('/') && !href.startsWith('//')) {
            node.properties.href = prefix + href;
          }
        }
      }
      const ch = node.children;
      if (Array.isArray(ch)) for (const c of ch) walk(c);
    }
  };
}
