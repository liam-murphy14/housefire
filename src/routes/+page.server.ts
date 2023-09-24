import { kv } from '@vercel/kv';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const [cursor, keys] = await kv.scan(0, { match: 'properties:*' });
	// for now i know that i won't have more than 1000 keys, may change in the future
	const tickersWithProperties = keys
		.map((key) => key.split(':')?.pop())
		.filter((ticker) => !!ticker) as string[];
	return {
		tickersWithProperties
	};
};
