console.log("UI.js connected")
import Dice from './Dice.js';
import Gamecard from './Gamecard.js';

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
//console.log(category_elements)
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




//---------Event Handlers-------//
function reserve_die_handler(event){
    console.log("Trying to reserve "+event.target.id);
    dice.reserve(event.target)
}

function roll_dice_handler(){
    display_feedback("Rolling the dice...", "good");
    dice.roll()

    console.log("Dice values:", dice.get_values());
    console.log("Sum of all dice:", dice.get_sum());
    console.log("Count of all dice faces:", dice.get_counts());
}

function enter_score_handler(event){
    console.log("Score entry attempted for: ", event.target.id);

    let value = document.getElementById(event.target.id).value;
    if (value.trim() != ''){
        value = parseInt(document.getElementById(event.target.id).value)
    }
    let category = event.target.id.split("_")
    category.pop()
    category = category.join("_")
    if (gamecard.is_valid_score(category, value) === true){
        console.log("is valid")
        document.getElementById(event.target.id).disabled = true;
    } else {
        console.log("not valid")
        document.getElementById(event.target.id).disabled = false;
    }

    document.getElementById("grand_total").innerText = Array.from(document.getElementsByClassName("category")).reduce(function(total, element){
        if (element.hasAttribute("disabled") == true){
            return total += parseInt(element.value);
        } else {
            return total;
        }
    }, 0);

}

//------Feedback ---------//
function display_feedback(message, context){
    console.log(context, "Feedback: ", message);

}