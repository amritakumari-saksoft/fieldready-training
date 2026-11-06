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
Added tenant ID, allowed roles, source, updated time, content and embedding columns.
Inserted three sample document chunks across two tenants.
Implemented cosine similarity search.
Enabled Row-Level Security (RLS).
Created document_chunks_access_policy.
Created restricted database role fieldready_employee.
Test Results
Test	Expected result	Actual result	Status
Tenant A employee	Employee guide only	Employee guide returned	PASS
Tenant A manager	HR policy only	HR policy returned	PASS
Tenant B admin	Finance document only	Finance document returned	PASS
RLS without identity settings	No rows	Zero rows returned	PASS
Employee login	Restricted account connects	Successfully connected	PASS
Employee SELECT privilege	SELECT permitted	Permission granted	PASS
Tenant impersonation	Employee cannot access another tenant	Finance document returned	FAIL
Security Finding

The current RLS policy uses custom PostgreSQL session settings:

app.tenant_id
app.user_role

These settings can be changed by the restricted database user.

During testing, the employee changed their tenant to tenant_B and role to admin. The restricted Finance.pdf document was then returned.

Therefore, the current implementation demonstrates tenant and role filtering functionality but does not provide production-grade trusted identity enforcement.

Learning
PostgreSQL RLS provides row-level filtering.
pgvector supports similarity search using vector embeddings.
Tenant and role conditions restrict document retrieval.
Database privileges and RLS policies work together.
Custom session variables are not sufficient as a trusted identity mechanism.
Negative security testing helps identify authorization vulnerabilities.
Remaining Work
Implement trusted identity enforcement.
Test protection against tenant and role impersonation.
Verify vector similarity searches respect access restrictions.
Complete discovery call.
Prepare discovery notes and clarifying email.
Conclusion

Successfully created a PostgreSQL database with pgvector and implemented basic tenant and role filtering using RLS.

Testing identified an authorization weakness involving user-controlled session settings. Trusted identity enforcement remains necessary before the implementation can be considered secure.
## Vector Similarity Access-Control Test

Executed pgvector cosine distance search using:

embedding <=> '[0.1, 0.2, 0.3]'

The query was executed as fieldready_employee.

Expected:
Only authorized document chunks should be returned.

Actual:
Employee_guide.pdf returned.
HR_policy.pdf not returned.
Finance.pdf not returned.

Status: PASS

Conclusion:
PostgreSQL Row-Level Security restricted
the vector similarity search results to
authorized document chunks.
