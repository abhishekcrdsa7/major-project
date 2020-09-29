const mongoose = require("mongoose");

const lugageSchema = new mongoose.Schema({
    lugageWeight: String,
    lugageDetails: String,
    lugageXRay: String,
    passport: {
        passportNo: String,
        passportScannedFile: String
    }
});

module.exports = mongoose.model("lugage", lugageSchema);