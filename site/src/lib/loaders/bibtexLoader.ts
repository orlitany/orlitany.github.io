import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import type { Loader } from 'astro/loaders';
import { parse as parseBibtex } from '@retorquere/bibtex-parser';

interface BibtexLoaderOptions {
  /** Path to the .bib file, relative to the Astro project root. */
  filePath: string;
}

/**
 * Loads cv_files/publications.bib. Each entry's custom fields (image, code,
 * page, poster, slides, talk, video, dataset, tweet, award, venue) are the
 * ONLY thing an author needs to add alongside a new BibTeX entry to publish
 * a paper on the site.
 */
export function bibtexLoader({ filePath }: BibtexLoaderOptions): Loader {
  return {
    name: `bibtex-loader:${filePath}`,
    load: async ({ store, config, parseData, logger }) => {
      const absPath = fileURLToPath(new URL(filePath, config.root));
      const raw = readFileSync(absPath, 'utf-8');
      // sentenceCase: false — `venue` and `title` are hand-written display
      // strings (e.g. "CVPR 2026"); the parser's default English
      // sentence-casing would otherwise mangle their casing.
      const result = parseBibtex(raw, { sentenceCase: false });

      if (result.errors.length > 0) {
        throw new Error(
          `Failed to parse ${filePath}:\n${result.errors.map((e) => JSON.stringify(e)).join('\n')}`,
        );
      }

      store.clear();
      for (const entry of result.entries) {
        const authorField = entry.fields.author;
        const authorList = Array.isArray(authorField) ? authorField : [];
        const authors = authorList.map((a) => {
          const firstName = typeof a === 'object' && a !== null ? (a.firstName ?? '') : '';
          const lastName = typeof a === 'object' && a !== null ? (a.lastName ?? '') : '';
          return {
            firstName,
            lastName,
            isOrLitany: firstName.trim() === 'Or' && lastName.trim() === 'Litany',
          };
        });

        const data = await parseData({
          id: entry.key,
          data: {
            citekey: entry.key,
            entryType: entry.type,
            title: String(entry.fields.title ?? ''),
            authors,
            year: String(entry.fields.year ?? ''),
            venue: String(entry.fields.venue ?? ''),
            image: entry.fields.image as string | undefined,
            paper: entry.fields.paper as string | undefined,
            page: entry.fields.page as string | undefined,
            code: entry.fields.code as string | undefined,
            dataset: entry.fields.dataset as string | undefined,
            slides: entry.fields.slides as string | undefined,
            poster: entry.fields.poster as string | undefined,
            talk: entry.fields.talk as string | undefined,
            video: entry.fields.video as string | undefined,
            tweet: entry.fields.tweet as string | undefined,
            award: entry.fields.award as string | undefined,
            raw: entry.input,
          },
        });
        store.set({ id: entry.key, data });
      }
      logger.info(`Loaded ${result.entries.length} publications from ${filePath}`);
    },
  };
}
