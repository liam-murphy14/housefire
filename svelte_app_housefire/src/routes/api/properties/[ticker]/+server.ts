import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getPropertiesByTicker } from '$lib/server/db/propertyQueries';

export const GET: RequestHandler = async ({ params }) => {
  const ticker = params.ticker;
  const properties = await getPropertiesByTicker(ticker);
  if (!properties || !properties.length) {
    error(404, {
      message: 'No properties found',
    });
  }
  return json(properties);
};
