// Series definitions. To add a new series, append here and tag posts
// with the matching `series:` field in their frontmatter.

export type SeriesMeta = {
  id: string;          // slug used in URL fragments
  name: string;        // canonical name (must match `series:` in post frontmatter)
  description: string;
};

export const SERIES: SeriesMeta[] = [
  {
    id: 'architecture-and-design',
    name: 'Architecture & Design',
    description:
      'Hexagonal architecture, design patterns, and the discipline of structuring software for change.',
  },
  {
    id: 'spring-boot',
    name: 'Spring Boot',
    description:
      'Patterns and antipatterns from Spring Boot in production — from caching and OpenFeign to the quirks of OPTIONS and HEAD requests.',
  },
  {
    id: 'design-patterns',
    name: 'Design Patterns',
    description:
      'A working tour through behavioral, structural, and creational design patterns — when to reach for them and when to leave them alone.',
  },
  {
    id: 'skill-driven-development',
    name: 'Skill-Driven Development',
    description:
      'Enterprise extension of SkDD — what specs gave us, what skills replaced, and what is worth recovering.',
  },
];

export const slugifySeries = (s: string) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

export const findSeries = (name?: string) =>
  name ? SERIES.find((s) => s.name === name) : undefined;

// Date formatting helpers
export const formatDate = (date: Date) =>
  date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

export const formatMonth = (date: Date) =>
  date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
