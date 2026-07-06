import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { bibtexLoader } from './lib/loaders/bibtexLoader';
import { jsonArrayLoader } from './lib/loaders/jsonArrayLoader';

// All data lives in cv_files/ at the repo root, shared with generate_cv.py
// (the LaTeX CV generator) — see the repo's top-level CLAUDE.md.

const publications = defineCollection({
  loader: bibtexLoader({ filePath: '../cv_files/publications.bib' }),
  schema: z.object({
    citekey: z.string(),
    entryType: z.string(),
    title: z.string(),
    authors: z.array(
      z.object({
        firstName: z.string(),
        lastName: z.string(),
        isOrLitany: z.boolean(),
      }),
    ),
    year: z.string(),
    venue: z.string(),
    image: z.string().optional(),
    paper: z.string().optional(),
    page: z.string().optional(),
    code: z.string().optional(),
    dataset: z.string().optional(),
    slides: z.string().optional(),
    poster: z.string().optional(),
    talk: z.string().optional(),
    video: z.string().optional(),
    tweet: z.string().optional(),
    award: z.string().optional(),
    raw: z.string(),
  }),
});

const news = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/news.json',
    unwrap: (raw) => (raw as { news: Record<string, unknown>[] }).news,
  }),
  schema: z.object({
    date: z.string(),
    text: z.string(),
  }),
});

const talks = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/talks.json',
    unwrap: (raw) => (raw as { talks: Record<string, unknown>[] }).talks,
  }),
  schema: z.object({
    title: z.string(),
    venue: z.string(),
    year: z.string().optional(),
    slides: z.string().optional(),
    video: z.string().optional(),
  }),
});

const workshops = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/workshops.json',
    unwrap: (raw) => (raw as { events: Record<string, unknown>[] }).events,
  }),
  schema: z.object({
    name: z.string(),
    venue: z.string(),
    year: z.string(),
    type: z.string(),
    link: z.string().optional(),
  }),
});

const press = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/press.json',
    unwrap: (raw) => (raw as { press: Record<string, unknown>[] }).press,
  }),
  schema: z.object({
    date: z.string(),
    title: z.string(),
    link: z.string(),
  }),
});

const courses = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/courses.json',
    unwrap: (raw) => (raw as { courses: Record<string, unknown>[] }).courses,
  }),
  schema: z.object({
    title: z.string(),
    courseNumber: z.string(),
    link: z.string().optional(),
    description: z.string(),
  }),
});

const students = defineCollection({
  loader: jsonArrayLoader({
    filePath: '../cv_files/students.json',
    // students.json keeps its original { current: [...], alumni: [...] }
    // shape (also read directly by generate_cv.py) — flatten it here with a
    // status tag rather than reshaping the shared source file.
    unwrap: (raw) => {
      const data = raw as { current: Record<string, unknown>[]; alumni: Record<string, unknown>[] };
      return [
        ...data.current.map((s) => ({ ...s, status: 'current' })),
        ...data.alumni.map((s) => ({ ...s, status: 'alumni' })),
      ];
    },
  }),
  schema: z.object({
    name: z.string(),
    type: z.enum(['PhD', 'MSc', 'Postdoc', 'Intern']),
    status: z.enum(['current', 'alumni']),
    startYear: z.string().optional(),
    graduationYear: z.string().optional(),
    currentPosition: z.string().optional(),
    website: z.string().optional(),
    note: z.string().optional(),
  }),
});

export const collections = { publications, news, talks, workshops, press, courses, students };
