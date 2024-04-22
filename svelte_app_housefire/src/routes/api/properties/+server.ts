import { error, json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { createManyProperties } from '$lib/server/db/propertyQueries';
import { PropertyCreateManyInputSchema } from '$lib/utils/prismaGeneratedZod';
import { ZodError } from 'zod';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const body = await request.json();
    const propertiesCreateManyInput = PropertyCreateManyInputSchema.parse(body);
    const propertiesCreatePrismaResponse = await createManyProperties(propertiesCreateManyInput);
    return json(propertiesCreatePrismaResponse);
  } catch (e) {
    if (e instanceof ZodError) {
      const zodErrorMessages = e.errors.map((error) => error.message).join(', ');
      error(400, {
        message: zodErrorMessages,
      });
    }
    error(500, {
      message: 'Something went wrong',
    });
  }
};
