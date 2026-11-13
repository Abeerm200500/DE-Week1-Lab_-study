// The Market: loads website reviews into MongoDB on the first start of the mongo container.
// Run automatically by the official mongo image (mongosh) from /docker-entrypoint-initdb.d.
const fs = require('fs');
const zlib = require('zlib');
const path = '/docker-entrypoint-initdb.d/website_reviews.json.gz';
const text = zlib.gunzipSync(fs.readFileSync(path)).toString('utf8');
const docs = EJSON.parse(text);
const market = db.getSiblingDB('market');
market.website_reviews.insertMany(docs);
print(`Loaded ${market.website_reviews.countDocuments()} website reviews into market.website_reviews`);
