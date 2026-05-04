import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { rehypePrefixRootPaths } from './rehype-prefix-root-paths.mjs';

// Production domain (local builds & custom hosting).
const defaultSite = 'https://bryamvega.com';

// GitHub Actions → Pages: set site + base from GITHUB_REPOSITORY.
// - User site repo: <user>.github.io → base "/"
// - Project repo:    <user>/<repo>   → base "/<repo>/"
const repository = process.env.GITHUB_REPOSITORY || '';
const [ghOwner, ghRepo] = repository.split('/');
const isGithubPages = process.env.GITHUB_PAGES === 'true';
// Custom domain on Pages is served at the domain root → site + base below.
const siteUrlOverride = (process.env.SITE_URL || '').replace(/\/$/, '');

let site = defaultSite;
let base = '/';

if (isGithubPages && siteUrlOverride) {
  site = siteUrlOverride;
  base = '/';
} else if (isGithubPages && ghOwner && ghRepo) {
  const isUserPagesRepo = ghRepo === `${ghOwner}.github.io`;
  site = `https://${ghOwner}.github.io`;
  base = isUserPagesRepo ? '/' : `/${ghRepo}/`;
}

// https://astro.build/config
export default defineConfig({
  site,
  base,
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'vesper',
      wrap: true,
    },
    rehypePlugins: [...(base !== '/' ? [rehypePrefixRootPaths(base)] : [])],
  },
});
