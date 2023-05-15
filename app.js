// Initialise the required packages
var express = require("express");
var app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);
const {spawn} =  require('child_process');
const cookieParser = require("cookie-parser");
//include default path node.js package
const path = require('path');
const ejs = require('hbs');

app.set('view engine', 'hbs');

//This parses the JSON, buffer, string and url encoded data submit
app.use(express.urlencoded({extended : false}));
app.use(express.json());
//running cookies
app.use(cookieParser());


//define routes
//redirecting to other files
// app.use('/auth', require('./Trendy/routes/auth'));
// app.use('/register', require('./Trendy/routes/auth'));
app.use("/Trendy", express.static(__dirname + "/Trendy"));
app.use(express.static('./public'));
app.set("views", path.join(__dirname + '/public/views'));

// Listen for user connections
http.listen(3000, () => {
    console.log('Listening on *:3000');
});

// When user accesses server, they are sent index.html
app.get('/index', (req, res) => {
    res.render('pages/index');
});

app.get('/map', (req, res) => {
    res.render('pages/map');
});

app.get('/contactus', (req, res) => {
    res.render('pages/contactus');
});

app.get('/index', (req, res) => {
    res.render('pages/index');
});

app.get('/favourites', (req, res) => {
    res.render('pages/favourites');
});

app.get('/account', (req, res) => {
    res.render('pages/account');
});

// Socket.io listens for events and handles I/O
// in a non-blocking way allowing multiple users
// to make requests simultaneously. 
io.on('connection', (socket) => {
    console.log('User connected');

    // Even handler takes in coordinates received
    // from the browser and uses them as inputs to 
    // the topTrends.py file.
    socket.on('location', (loc) => {
        var resp;
        const py = spawn('python', ['topTrends.py', loc.lat, loc.lng])
        py.stdout.on('data', function (data) {
            console.log('Retrieving data from script');
            resp = data.toString();
        });

        // Once the python file has closed, the result printed
        // to the screen is parsed to JSON and sent back to
        // the client.
        // Data is only processed and sent if the result from
        // the python file is not 'undefined'.
        py.on('close', (code) => {
            if(typeof resp !== 'undefined') {
                console.log('Exit code: '+code);
                console.log("Top Trends: " + resp);
                var returnData = JSON.parse(resp);
                socket.emit('data', returnData);
            }
        });

    });

    // Event handler takes in a loation name received
    // from the browser and uses it as  an input to 
    // the pieChart.py file, in order to return the
    // data used by the pie chart.
    socket.on('favCall', (loc) => {
        console.log(loc);
        var resp;
        const py = spawn('python', ['pieChart.py', loc])
        py.stdout.on('data', function (data) {
            console.log('Retrieving data from script');
            resp = data.toString();
        });

        // Once the python file has closed, the result printed
        // to the screen is parsed to JSON and sent back to
        // the client.
        // Data is only processed and sent if the result from
        // the python file is not 'undefined'.
        py.on('close', (code) => {
            if(typeof resp !== 'undefined') {
                console.log('Exit code: '+code);
                console.log("Top Trends: " + resp);
                var returnData = JSON.parse(resp);
                socket.emit('pieData', returnData);
            }
        });

    });
});

