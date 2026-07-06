import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import type { Loader } from 'astro/loaders';

interface JsonArrayLoaderOptions {
  /** Path to the JSON file, relative to the Astro project root. */
  filePath: string;
  /** Extract the array of entries from the file's parsed JSON. */
  unwrap: (raw: unknown) => Record<string, unknown>[];
}

/**
 * Loads a flat array of objects out of a JSON file that isn't shaped like a
 * standard Astro data collection (top-level wrapper key, no per-item id).
 * cv_files/*.json is also read directly by generate_cv.py, so the file itself
 * is left in its original human-edited shape and unwrapped here instead.
 */
export function jsonArrayLoader({ filePath, unwrap }: JsonArrayLoaderOptions): Loader {
  return {
    name: `json-array-loader:${filePath}`,
    load: async ({ store, config, parseData, logger }) => {
      const absPath = fileURLToPath(new URL(filePath, config.root));
      const raw = JSON.parse(readFileSync(absPath, 'utf-8'));
      const items = unwrap(raw);

      store.clear();
      for (const [index, item] of items.entries()) {
        const id = String(index);
        const data = await parseData({ id, data: item });
        store.set({ id, data });
      }
      logger.info(`Loaded ${items.length} entries from ${filePath}`);
    },
  };
}
