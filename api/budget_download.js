require('dotenv').config(); // Load environment variables from .env
let api = require('@actual-app/api');

// Get the month parameter from command-line arguments
const month = process.argv[2]; // Receives the date argument (e.g., "2024-10")

// Check if the month argument is provided
if (!month) {
  console.error('Please provide a month argument in the format YYYY-MM (e.g., "2024-10")');
  process.exit(1); // Exit if no month argument is provided
}

(async () => {
  try {
    // Initialize the API with environment variables
    await api.init({
      dataDir: process.env.DATA_DIR,
      serverURL: process.env.SERVER_URL,
      password: process.env.PASSWORD,
    });

    // Download the budget using the Sync ID from .env
    await api.downloadBudget(process.env.SYNC_ID);

    // Get budget data for the specified month
    let budget = await api.getBudgetMonth(month);
    console.log(budget);

  } catch (error) {
    console.error("An error occurred:", error);
  } finally {
    // Ensure the API is properly shutdown
    await api.shutdown();
  }
})();
