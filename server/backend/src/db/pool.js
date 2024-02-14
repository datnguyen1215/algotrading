import { Pool } from "pg";
import settings from "@src/settings";

const pool = new Pool({
  connectionString: settings.database.connectionString
});

export default pool;
