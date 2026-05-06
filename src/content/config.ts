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
    signature: z.string().optional(),
    /** Omit from build entirely—no URL. Use while writing until you publish. */
    draft: z.boolean().default(false),
    /** URL exists, but hidden from listings/search/series + `noindex` until you flip to false. */
    unlisted: z.boolean().default(false),
    canonical: z.string().url().optional(),
    /** Lower sorts first on the home “building now” strip; omit for normal draft essays (sorted by date). */
    buildingOrder: z.number().optional(),
    /** Eyebrow label on that strip (e.g. “Agents · Delivery”). If omitted, uses “Draft essay · series”. */
    buildingEyebrow: z.string().optional(),
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
