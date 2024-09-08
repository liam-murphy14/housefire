import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getGeocodeByAddressInput } from '$lib/server/db/geocodeQueries';

export const GET: RequestHandler = async ({ params }) => {
  const addressInput = params.addressInput;
  const geocode = await getGeocodeByAddressInput(addressInput);
  if (!geocode) {
    error(404, {
      message: 'No properties found',
    });
  }
  return json(geocode);
};
