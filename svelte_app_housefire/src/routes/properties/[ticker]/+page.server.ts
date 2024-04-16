import { PrismaClient } from '@prisma/client';
import type { PageServerLoad } from './$types';

const prisma = new PrismaClient();

export const load: PageServerLoad = async ({ params }) => {
  const { ticker } = params;
  const properties = await prisma.property.findMany({
    where: {
      reit: {
        ticker,
      },
    },
  });

  return {
    ticker,
    properties,
    metaTags: {
      title: `${ticker} Property Data`,
      description: `See fine-grained property data for ${ticker} holdings, including property type, location, square footage, and more.`,
    },
  };
};
