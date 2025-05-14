const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const IMAGES_FOLDER = './images';
const UFO_IMAGES_FOLDER = './UFO_images';
const CSV_FILE = './ufo_scrubbed.csv';

// Function to import CSV into MongoDB
const importCSV = (csvFile, dbName, collectionName) => {

    const mongoImportCmd = `mongoimport --db ${dbName} --collection ${collectionName} --type csv --headerline --file ${csvFile}`;
    exec(mongoImportCmd, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error importing CSV: ${error}`);
            return;
        }
        console.log(`CSV Import Output: ${stdout}`);
        if (stderr) {
            console.error(`CSV Import Error Output: ${stderr}`);
        }
    });
};

// Function to insert image files into MongoDB using mongofiles
const insertImages = (folderPath, dbName) => {
    fs.readdir(folderPath, (err, files) => {
        if (err) {
            console.error(`Error reading directory: ${err}`);
            return;
        }

        files.forEach(file => {
            const filePath = path.join(folderPath, file);
            const mongoFilesCmd = `mongofiles --db ${dbName} put ${file} --local ${filePath}`;

            exec(mongoFilesCmd, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error inserting file ${file}: ${error}`);
                    return;
                }
                console.log(`File Insert Output (${file}): ${stdout}`);
                if (stderr) {
                    console.error(`File Insert Error Output (${file}): ${stderr}`);
                }
            });
        });
    });
};

// Check if CSV file exists and import it
if (fs.existsSync(CSV_FILE)) {
    importCSV(CSV_FILE, 'MongoProject', 'UFOSightings');
} else {
    console.error(`CSV file not found: ${CSV_FILE}`);
}

// Insert images from IMAGES_FOLDER into MongoDB
insertImages(IMAGES_FOLDER, 'MongoProject');

// Insert images from UFO_IMAGES_FOLDER into MongoDB
insertImages(UFO_IMAGES_FOLDER, 'MongoProject');