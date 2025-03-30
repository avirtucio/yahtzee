let express = require('express');
let app = express();

//npm install node-fetch
//Socket Conection
let server = require('http').Server(app);
let io = require('socket.io')(server);

//Middleware
const ejs = require('ejs');
app.use(express.static('static')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

io.on('connection', function(socket){  
  io.emit('connection', {
    num_total_connections: io.engine.clientsCount
  }); 

  socket.on('game_connection', function(data) {  
    socket.join(data.game_name);
    console.log('Socket game connection event:', data.username, io.sockets.adapter.rooms.get(data.game_name).size);

    io.to(data.game_name).emit('game_connection', {
        username:data.username,
        num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size
    });
  }); 

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });

  socket.on('valid_score_entry', async function(data){
    // console.log("valid score entry for "+ data.username)
    // console.log(data.username+"'s categories", data.user_categories)
    // console.log(data.game_name)

    scorecard_name = data.game_name+"|"+data.username

    try {
      const response = await fetch(`http://127.0.0.1:8080/scorecards/${scorecard_name}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              categories: data.user_categories
          })
      });

      if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
      }
      
    } catch (error) {
        console.error(error.message);
    }
    
    console.log("server.js, valid_score_entry, after scorecard update")
    let all_game_scorecards;
    
    try {
      const response = await fetch(`http://127.0.0.1:8080/gameDataToNodeServer/${data.game_name}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              game_name: data.game_name
          })
      });

      if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
      }

      const json = await response.json();
      console.log("server.js, valid_score_entry, all_games_scorecards", json)
      all_game_scorecards = json;
      
    } catch (error) {
        console.error(error.message);
    }

    io.to(data.game_name).emit('valid_score_entry', {
      message: data.username+" has submitted a new score",
      all_game_scorecards: all_game_scorecards
    });

  });

});

app.get('/games/:game_name/:username', async function(request, response) {
  // console.log("top of async function")
  let username = request.params.username;
  let game_name = request.params.game_name;
  let all_game_scorecards;
  // console.log("username and game_name from request params", username, game_name)
  
    try {
      const response = await fetch(`http://127.0.0.1:8080/gameDataToNodeServer/${game_name}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              game_name: game_name
          })
      });

      if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
      }

      const json = await response.json();
      // console.log("server.js, all_games_scorecards", json)
      all_game_scorecards = json;
      
    } catch (error) {
        console.error(error.message);
    }

    // console.log("json out of try stuff", all_game_scorecards)
    // for (const [key, value] of Object.entries(all_game_scorecards)) {
    //   console.log("for loop")
    //   console.log(key);
    //   console.log(value)
    // }
  
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("index", {
    username: username,
    game_name: game_name, 
    all_game_scorecards: all_game_scorecards
  });
});

//start the server
const port = process.env.PORT || 3000;
app.set('port', port); //let heroku pick the port if needed

server.listen(port, function() {
  console.log('Server started at http://localhost:'+port+'.')
});
