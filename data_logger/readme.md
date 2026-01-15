## Test Database (test_data.db)

The file `test_data.db` is a lightweight SQLite database used only for
testing and validation purposes.

It is not part of the production data pipeline. Instead, it provides:
- Verification of database schema
- Validation of insert and query operations
- Independent testing without MySQL dependency

The actual runtime system uses MySQL (`fleet_db`) for real-time data
storage.
