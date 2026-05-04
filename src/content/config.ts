import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    series: z.string().optional(),
    heroImage: z.string().optional(),
    heroImageCaption: z.string().optional(),
    draft: z.boolean().default(false),
    canonical: z.string().url().optional(),
  }),
});

const talks = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    event: z.string(),
    location: z.string(),
    date: z.coerce.date(),
    status: z.enum(['upcoming', 'delivered', 'proposed']).default('delivered'),
    language: z.enum(['en', 'es']).default('en'),
    abstract: z.string(),
    slides: z.string().url().optional(),
    video: z.string().url().optional(),
    eventUrl: z.string().url().optional(),
  }),
});

export const collections = { blog, talks };
