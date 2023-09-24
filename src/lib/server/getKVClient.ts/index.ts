import { VercelKV, createClient } from '@vercel/kv';
import { KV_URL, KV_REST_API_TOKEN } from '$env/static/private';

let client: VercelKV;

export function getKVClient() {
	if (!client) {
		client = createClient({
			url: KV_URL,
			token: KV_REST_API_TOKEN
		});
	}

	return client;
}
