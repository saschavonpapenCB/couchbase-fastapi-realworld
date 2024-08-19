import { defineConfig } from 'cypress';

const API_ROOT = 'http://localhost:80';

export default defineConfig({
  env: {
    apiUrl: API_ROOT,
    user: {
      email: 'tester@test.com',
      password: 'password1234',
      username: 'testuser',
    },
  },
  viewportHeight: 1000,
  viewportWidth: 1000,
  video: true,
  projectId: 'bh5j1d',
  e2e: {
    setupNodeEvents(on, config) {
      on('task', {
        cleanDatabase() {
          // Add the code to clean your database here
          // For example, you might call an API endpoint that resets your database
          return null;
        }
      });
    },
    baseUrl: API_ROOT,
    specPattern: 'cypress/e2e/**/*.{js,jsx,ts,tsx}',
  },
});
