import { PrismaClient } from '@prisma/client';
import type { PageServerLoad } from './$types';

const prisma = new PrismaClient();

export const load: PageServerLoad = async () => {
  // TODO: refactor into dao ??
  const reitTickers = await prisma.reit.findMany(
    {
      select: {
        ticker: true,
      }
    }
  );

  return {
    reitTickers: reitTickers.map((reit) => reit.ticker),
    metaTags: {
      title: 'Home of the Hottest REIT Data',
      description:
        'See fine-grained property data for your favorite REITs, updated monthly with more tickers added regularly.',
    },
  };
};
