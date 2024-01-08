// Importing the modules required for express.js
const express = require("express")
const app = express()

// Importing a module used to specify path of a file
const path = require("path")

// Importing a module used to execute py files from node.js
const { PythonShell } = require("python-shell")

// Python files path
var options = {
    scriptPath: __dirname
}

// To display index.html as starting page on screen when server starts to run (Get request of index.html)
app.get("/", function (req, res) {

    // Sending index.html page to be displayed on screen 
    res.sendFile(__dirname + "/index.html")  

})

// Processing main.py file on clicking button of index.html (Post request of index.html)
app.post("/", function (req, res) {
    PythonShell.run("main.py", options, function (err, result) {
        res.sendFile(__dirname + "/thankyou.html");
    });
})

// Making server to run on port 5000
app.listen(5000, function () {
    console.log("Server is running on port 5000")
})