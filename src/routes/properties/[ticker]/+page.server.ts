import { kv } from '@vercel/kv';
import type { PageServerLoad } from './$types';
import type { PropertyData } from '$lib/interfaces/PropertyData.interface';

export const load: PageServerLoad = async ({ params }) => {
  const { ticker } = params;
  const properties = (await kv.json.get(`properties:${ticker}`)) as PropertyData[];
  return {
    ticker,
    properties,
  };
};
