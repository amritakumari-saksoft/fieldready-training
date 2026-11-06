Day 8 – pgvector Access-Control Test Results
Environment
PostgreSQL: 18.6
pgvector: 0.8.1
Database: fieldready_db
Table: document_chunks
Implementation
Created PostgreSQL database.
Installed and enabled pgvector.
Created document_chunks table.
Added tenant ID and allowed roles metadata.
Inserted three sample document chunks.
Implemented cosine similarity search.
Enabled Row-Level Security.
Created document_chunks_access_policy.
Test Results
Test	Expected result	Actual result	Status
Tenant A employee	Employee guide only	Employee guide returned	PASS
Tenant A manager	HR policy only	HR policy returned	PASS
Tenant B admin	Finance document only	Finance document returned	PASS
RLS default deny	No rows without policy	Zero rows returned before policy creation	PASS
Security Finding

The current RLS policy uses custom session settings:

app.tenant_id
app.user_role

These settings can be changed by the restricted database user.

Therefore, the current implementation demonstrates tenant and role filtering functionality but does not provide production-grade trusted identity enforcement.

Learning
PostgreSQL RLS provides row-level filtering.
pgvector supports similarity search using vector embeddings.
Tenant and role conditions restrict document retrieval.
Trusted identity enforcement is essential for multi-tenant security.
Remaining Work
Implement trusted identity enforcement.
Test protection against tenant and role impersonation.
Complete discovery call.
Prepare discovery notes and clarifying email.
