# Node.js Budget API Script

This project provides a Node.js script to interact with the Actual Budget API. The script initializes the API, downloads budget data, and retrieves budget information for a specified month.

## Prerequisites

- **Node.js**: Make sure you have Node.js installed. You can download it from [Node.js official website](https://nodejs.org/).
- **npm**: Node Package Manager (comes with Node.js).

## Installation

1. Clone this repository or download the script file to your local machine.
2. Navigate to the project directory in your terminal.
3. Install required dependencies by running:

   ```bash
   npm install
   ```

## Configuration

1. **Create a `.env` file** in the project root with the following variables:

   ```plaintext
   DATA_DIR=/path/to/your/data
   SERVER_URL=https://your-server-url.com
   PASSWORD=yourpassword
   SYNC_ID=your-sync-id
   ```

   - `DATA_DIR`: Directory to store locally cached budget data.
   - `SERVER_URL`: URL of the Actual Budget API server.
   - `PASSWORD`: Your password for the Actual Budget server.
   - `SYNC_ID`: Sync ID for your budget, found in Actual Budget under **Settings → Show advanced settings → Sync ID**.

## Usage

To run the script, execute the following command, replacing `YYYY-MM` with the desired month (e.g., `2024-10`):

```bash
node script.js YYYY-MM
```

### Example

```bash
node script.js 2024-10
```

This command will initialize the API, download budget data, and retrieve budget information for October 2024.

## Notes

- Ensure that the `.env` file is located in the project’s root directory.
- The date parameter must be provided in `YYYY-MM` format.

## Error Handling

If any error occurs during initialization or data retrieval, an error message will be printed to the console.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
