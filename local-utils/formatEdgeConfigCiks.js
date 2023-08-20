import fs from 'fs/promises';
import path from 'path';
// get reit file from https://stockmarketmba.com/listofreits.php if it still exists
const REIT_CSV_LOCATION = path.resolve('/Users/liammurphy/Downloads/reits.csv');
const CIK_ENDPOINT = 'https://sec.gov/files/company_tickers.json';
async function formatEdgeConfigCiks() {
	const reitSet = new Set();
	const reitCsv = await fs.readFile(REIT_CSV_LOCATION, 'utf-8');
	for (const line of reitCsv.split('\n').slice(1)) {
		const [ticker] = line.split(',');
		reitSet.add(ticker.substring(1, ticker.length - 1));
	}
	const res = await fetch(CIK_ENDPOINT);
	const data = await res.json();
	console.log('{');
	for (const key of Object.keys(data)) {
		const { cik_str, ticker } = data[key];
		if (!reitSet.has(ticker)) continue;
		console.log(`    "${ticker}": "${cik_str}",`);
	}
	console.log('}');
}
formatEdgeConfigCiks();
