import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { get } from '@vercel/edge-config';

const EDGAR_ENDPOINT = 'https://data.sec.gov/api/xbrl/companyfacts/CIK';

export const GET: RequestHandler = async ({ url, fetch }) => {
	const ticker = url.searchParams.get('ticker');
	if (typeof ticker !== 'string') {
		throw error(400, 'Ticker must be a string');
	}
	const cik = await get(ticker);
	const cikRes = await fetch(`${EDGAR_ENDPOINT}${cik}.json`);
	const data = await cikRes.json();
	const coolFact = data.facts['us-gaap']['Assets'];
	return json({ coolFact });
};
