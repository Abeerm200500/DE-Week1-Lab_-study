// Lab 3
// SOLUTIONS
// Open the shell: docker compose exec mongo mongosh -u root -p --authenticationDatabase admin market and enter teh password to log in

// One review (example)
db.website_reviews.findOne()

// Count all the reviews
db.website_reviews.countDocuments()                              // 3465

// Five-star reviews (example)
db.website_reviews.find({ overall_rating: 5 }).limit(3)

// Count the one-star reviews
db.website_reviews.countDocuments({ overall_rating: 1 })         // 145

// Count the late-delivery complaints
db.website_reviews.countDocuments({ topics: "late_delivery" })   // 498

// Bonus: reviews per rating, like GROUP BY
db.website_reviews.aggregate([{ $group: { _id: "$overall_rating", reviews: { $sum: 1 } } }, { $sort: { _id: 1 } }])
// 1: 145, 2: 333, 3: 811, 4: 1172, 5: 1004

