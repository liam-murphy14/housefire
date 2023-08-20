import type { VercelRequest, VercelResponse } from '@vercel/node';
import { get } from '@vercel/edge-config';

const EDGAR_ENDPOINT = 'https://data.sec.gov/api/xbrl/companyfacts/CIK';

export default async function handler(req: VercelRequest, res: VercelResponse) {
	const { ticker } = req.query;
	if (Array.isArray(ticker)) {
		return res.status(400).json({ error: 'Ticker must be a string' });
	}
	const cik = await get(ticker);
	const cikRes = await fetch(`${EDGAR_ENDPOINT}/${cik}.json`);
	const data = await cikRes.json();
	const coolFact = data.facts['us-gaap']['Assets'];
	return res.status(200).json({ coolFact });
}
