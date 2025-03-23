console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';
let socket = io.connect('/');//the default namespace

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

let dice_elements =[];
for (let i = 0; i<5; i++){
    let die = document.getElementById("die_"+i); //each image of dice//
    die.addEventListener('dblclick', reserve_die_handler); //each die object listening for dbclick, will call reserve_die_handler//
    dice_elements.push(die); //array of dice images//
}
let rolls_remainging_element = parseInt(document.getElementById("rolls_remaining").textContent); //gets object from game.html with that id, gets the text from that object, parseInt into integer//

let dice = new Dice(dice_elements, rolls_remainging_element);
window.dice = dice; //useful for testing to add a reference to global window object



//-----Gamecard Setup---------//
let category_elements = Array.from(document.getElementsByClassName("category"));
for (let category of category_elements){
    category.addEventListener('keypress', function(event){
        if (event.key === 'Enter') {
            enter_score_handler(event);
        }
    });
}
let score_elements = Array.from(document.getElementsByClassName("score"));
console.log(score_elements)
let gamecard = new Gamecard(category_elements, score_elements, dice);
window.gamecard = gamecard; //useful for testing to add a reference to global window object

display_feedback("good", "new game loaded")

//------Save and Load Button Setup------//
let save_button = document.getElementById("save_game")
let load_button = document.getElementById("load_game")

save_button.addEventListener('click', save_game_handler);
load_button.addEventListener('click', load_game_handler);



//---------Event Handlers-------//
function save_game_handler(event){
    localStorage.setItem('yahtzee', JSON.stringify(gamecard.to_object()));
    display_feedback("good", "game saved successful")
}

function load_game_handler(event){
    console.log('load button pressed');
    if (localStorage.getItem("yahtzee")){
        gamecard.load_scorecard(JSON.parse(localStorage.getItem("yahtzee")))
        display_feedback("good", "successfully loaded game")
    } else {
        display_feedback("bad", "no saved game exists")
    }
    
}

function reserve_die_handler(event){
    console.log("Trying to reserve "+event.target.id);
    dice.reserve(event.target)
}

function roll_dice_handler(){
    dice.roll()

    let feedback_el = document.getElementById("feedback")
    feedback_el.innerHTML = ""
    feedback_el.classList.remove("good")
    feedback_el.classList.remove("bad")

    if (dice.get_rolls_remaining() === 0){
        display_feedback("bad", "Rolling the dice...");
    } 
    

    // console.log("Dice values:", dice.get_values());
    // console.log("Sum of all dice:", dice.get_sum());
    // console.log("Count of all dice faces:", dice.get_counts());
}

function enter_score_handler(event){
    console.log("Score entry attempted for: ", event.target.id);

    let value = document.getElementById(event.target.id).value;
    if (value.trim() != ''){
        value = parseInt(document.getElementById(event.target.id).value)
    }
    let category = event.target.id.split("_")
    let username = category[category.length-1]
    category.pop()
    category.pop()
    // console.log(category)
    category = category.join("_")
    // category = category.slice(0,(category.length-1))
    console.log("UI.js, enter_score_handler, category and username,", category, username)
    if (gamecard.is_valid_score(category, value) === true){
        display_feedback("good", "score input valid")
        document.getElementById(event.target.id).disabled = true;
        dice.reset();

        socket.emit('valid_score_entry', {
            username: username,

        })
    } else {
        display_feedback('bad', 'score input invalid')
        document.getElementById(event.target.id).disabled = false;
    }

    gamecard.update_scores(username)
    if (gamecard.is_finished() === true){
        display_feedback("good", "game is finished")
    }
}

//------Feedback ---------//
function display_feedback(message, context){
    console.log(context, "Feedback: ", message);
    let feedback_el = document.getElementById("feedback")
    feedback_el.innerHTML = context
    feedback_el.classList.remove("good")
    feedback_el.classList.remove("bad")
    feedback_el.classList.add(message)
}