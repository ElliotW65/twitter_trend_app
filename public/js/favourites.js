$(document).ready(function () {
    var socket = io();

    // Get HTML collection of all 'cards'.
    var cards = document.getElementsByClassName('card');

    // Initialise variable that will hold JSON received from server.
    var pieDataJSON;
    
    // Function returns true if any of the cards are currently
    // clicked/active and false is not.
    function activeCheck(c) {
        var check = false;
        Array.from(document.getElementsByClassName("card")).forEach(function(item) {
            if(item.classList.contains('active')) {
                check = true;
            }        
        });
        return check;
    };
    
    // Returns the HTML elemtent/card that is currently clicked
    // AKA active.
    function getActive() {
        var card;
        Array.from(document.getElementsByClassName("card")).forEach(function(item) {
            if(item.classList.contains('active')) {
                card = item
            }        
        });
        return card;
    };
    
    // Function takes as a paremeter an HTML element 'card' and
    // make it active. If the card is already active, it reverts 
    // the colours of the card, deactivating it.
    function makeActive(c) {
        var cardOne = c;
        var cardTwo = getActive();
        if(activeCheck(cards)) {
            if(cardOne != cardTwo) {
                cardTwo.classList.remove('active');
                cardOne.classList.add('active');
            }
            else {
                if(cardOne.classList.contains('active')) {
                    cardOne.classList.remove('active');
                }
                else {
                    cardOne.classList.add('active');
                }
            }
        }
        else {
            cardOne.classList.add('active');
        }
    };
    
    // For each iterates over each HTML element returned with class
    // name 'card' and adds a 'click' event listener to each.
    Array.from(document.getElementsByClassName("card")).forEach(function(item) {
        item.addEventListener('click', () => {
            var active = getActive();
            if(item != active) {
                makeActive(item);

                // Location to be sent to server is taken from the card via DOM.
                var location = item.childNodes.item(1).childNodes.item(1).childNodes.item(0).textContent;
    
                // h1 of container that will show result is set to the name of the locaiton
                // the user has selected.
                document.getElementById('results-header').childNodes.item(1).innerHTML = location
    
                // Location name is sent to server to be an input to pieChart.py file.
                socket.emit('favCall', location);
    
                // Makes results container visible.
                document.getElementById('result-container').style.visibility = 'visible';
    
                // Event handler receives data from server and creates a pie chart using
                // the data. The pie chart is then put into the reuslts container on the
                // left of the screen.
                socket.on('pieData', (data) => {
                    console.log("data received");
                    pieDataJSON = data;
    
                    var pieLabels = pieDataJSON.map(function(e) {
                        return e.tag;
                    });
                
                    var pieData = pieDataJSON.map(function(e) {
                        return e.count;
                    });
    
                    // Create pie chart. Pie chart creation code created with the help of online
                    // resource: https://www.js-tutorials.com/jquery-tutorials/simple-example-pie-chart-using-chartjs-html5-canvas/
                    var chartDiv = $("#pieChart");
                    var myChart = new Chart(chartDiv, {
                        type: 'pie',
                        data: {
                            labels: pieLabels,
                            datasets: [
                            {
                                data: pieData,
                                backgroundColor: [
                                    "#FF6384",
                                "#4BC0C0",
                                "#FFCE56",
                                "#E7E9ED",
                                "#36A2EB"
                                ]
                            }]
                        },
                        options: {
                            title: {
                                display: true,
                                text: 'Porportion of Hashtags'
                            },
                            legend: {
                                display: true,
                                position: 'left'
                            },
                            responsive: false,
                            maintainAspectRatio: true,
                        },
                    });
                });
            }
            else {
                item.classList.remove('active');
                document.getElementById('result-container').style.visibility = 'hidden';
            }
        });
    });

    // Code for Kebab menu based on code from: 
    // https://codepen.io/mildrenben/pen/MwezWG example
    // written by Ben Mildren.
    var kebab = document.querySelector('.kebab'),
        middle = document.querySelector('.middle'),
        cross = document.querySelector('.cross'),
        dropdown = document.querySelector('.dropdown');
    
    kebab.addEventListener('click', function() {
      middle.classList.toggle('active');
      cross.classList.toggle('active');
      dropdown.classList.toggle('active');
    })    
})


