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

export const deletePropertiesByTicker = async (ticker: string) => {
  return await prisma.property.deleteMany({
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
  return await prisma.property.createManyAndReturn({
    data: propertiesToCreate,
  });
};
