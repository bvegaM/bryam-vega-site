/**
 * Blog posts that appear on home, /blog, search, /series, and related feeds.
 * Drafts never get a URL. Unlisted posts have a URL but stay out of discovery.
 */
export const blogListingFilter = ({ data }: { data: { draft: boolean; unlisted?: boolean } }) =>
  !data.draft && !data.unlisted;
