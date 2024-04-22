import prisma from '$lib/server/db/prisma';
import { type Property, Prisma } from '@prisma/client';

export const getPropertiesByTicker: (ticker: string) => Promise<Property[]> = async (ticker) => {
  return await prisma.property.findMany({
    where: {
      reit: {
        ticker,
      },
    },
  });
};

export const createManyProperties = async (
  propertiesToCreate: Prisma.PropertyCreateManyInput | Prisma.PropertyCreateManyInput[],
) => {
  return await prisma.property.createMany({
    data: propertiesToCreate,
  });
};
