// Links to user_info.sql db in temp branch

var mysql      = require('mysql');
// new variable (connection) - create the connection
var connection = mysql.createConnection({
host     : 'localhost',
user     : 'root', // insert username for db
password : '', // sql password
database : 'user_info' // database name
});

// create the connection
connection.connect();

// select all the data from the table (in the database)
connection.query('SELECT * from User_Info', function(err, rows, fields) {
// Print the rows
    if (!err)
    console.log(rows);
    // If there's an error, log this in the console
    else
    console.log('Error while performing Query.');
    });

// Close the connection
connection.end();
