import { z, defineCollection } from 'astro:content';

const projectsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    repo: z.string(),
    description: z.string(),
    license: z.string(),
    language: z.string(),
    version: z.string(),
    xAccount: z.string().optional(),
    codeSize: z.string().optional(),
    memorySystemType: z.string().optional(),
    features: z.object({
      multiChannel: z.boolean(),
      sandboxIsolation: z.boolean(),
      memorySystem: z.boolean(),
      scheduledTasks: z.boolean(),
      mcpSupport: z.boolean(),
      webSearch: z.boolean(),
      webUI: z.boolean(),
      agentSwarms: z.boolean(),
    }),
  })
});

export const collections = {
  'projects': projectsCollection,
};
