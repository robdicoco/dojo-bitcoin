-- Create the 'documents' table
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_hash TEXT UNIQUE NOT NULL,
    wallet_address TEXT NOT NULL,
    status TEXT DEFAULT 'Pending Payment',
    tx_id TEXT
);

-- Create the 'wallets' table
CREATE TABLE wallets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT UNIQUE NOT NULL,
    document_hash TEXT NOT NULL,
    FOREIGN KEY (document_hash) REFERENCES documents(document_hash)
);