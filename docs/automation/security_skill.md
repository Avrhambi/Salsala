**Skill Name**: secure-implementation-standard
##### Instructions:

Fail-Fast Validation: Every function receiving external input must validate data types and boundary conditions at the very first line.

Secret Management: Never hardcode strings that look like keys, passwords, or tokens. Use the config/ manager to pull from environment variables.

Explicit Error Strategy: All errors must be caught, logged via the central logger, and never allowed to fail silently.

Least Privilege: If writing to the file system, ensure the path is restricted to the project’s /storage or /assets directories only