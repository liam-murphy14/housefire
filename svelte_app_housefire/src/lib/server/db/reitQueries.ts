import prisma from '$lib/server/db/prisma';
import type { Reit } from '@prisma/client';

export const getAllReits: () => Promise<Reit[]> = async () => {
    return await prisma.reit.findMany();
}

export const getAllTickers: () => Promise<string[]> = async () => {
    const reits = await getAllReits();
    return reits.map((reit) => reit.ticker);
}