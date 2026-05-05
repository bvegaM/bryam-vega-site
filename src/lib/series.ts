// Series definitions. To add a new series, append here and tag posts
// with the matching `series:` field in their frontmatter.

export type SeriesMeta = {
  id: string;          // fragment on `/series/` (`#id`), stable short slug (e.g. ia, apis)
  name: string;        // canonical name (must match `series:` in post frontmatter)
  description: string;
};

export const SERIES: SeriesMeta[] = [
  {
    id: 'architecture-and-design',
    name: 'Architecture & Design',
    description:
      'Structuring systems so change stays affordable—boundaries, coupling, and the habits that keep big codebases honest when requirements shift.',
  },
  {
    id: 'spring-boot',
    name: 'Spring Boot',
    description:
      'Production-shaped Spring—what works under load, what fails quietly, and the sharp edges around HTTP clients, caching, resilience, and framework defaults.',
  },
  {
    id: 'design-patterns',
    name: 'Design Patterns',
    description:
      'Patterns as vocabulary, not decoration: when a name earns its complexity, when it hides a smell, and how to apply classics without ceremony.',
  },
  {
    id: 'ia',
    name: 'IA',
    description:
      '',
  },
  {
    id: 'apis',
    name: 'APIs',
    description:
      '',
  },
];

export const slugifySeries = (s: string) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

export const findSeries = (name?: string) =>
  name ? SERIES.find((s) => s.name === name) : undefined;

/** Hash target for `/series/#…` from post frontmatter `series:` name. */
export const seriesFragmentId = (seriesName?: string) =>
  seriesName ? (findSeries(seriesName)?.id ?? slugifySeries(seriesName)) : '';

// Date formatting helpers
export const formatDate = (date: Date) =>
  date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

export const formatMonth = (date: Date) =>
  date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
