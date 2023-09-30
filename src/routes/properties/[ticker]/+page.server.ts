import { kv } from '@vercel/kv';
import type { PageServerLoad } from './$types';
import type { PropertyData } from '$lib/interfaces/PropertyData.interface';

export const load: PageServerLoad = async ({ params }) => {
  const { ticker } = params;
  const properties = (await kv.json.get(`properties:${ticker}`)) as PropertyData[];
  return {
    ticker,
    properties,
    metaTags: {
      title: `${ticker} Property Data`,
      description: `See fine-grained property data for ${ticker} holdings, including property type, location, square footage, and more.`,
    },
  };
};
