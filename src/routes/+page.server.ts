import { kv } from '@vercel/kv';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
  const [cursor, keys] = await kv.scan(0, { match: 'properties:*' });
  // for now i know that i won't have more than 1000 keys, may change in the future
  const tickersWithProperties = keys
    .map((key) => key.split(':')?.pop())
    .filter((ticker) => !!ticker) as string[];
  return {
    tickersWithProperties,
    metaTags: {
      title: 'Home of the Hottest REIT Data',
      description:
        'See fine-grained property data for your favorite REITs, updated monthly with more tickers added regularly.',
    },
  };
};
