console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element;
        this.dice_elements= dice_elements; //array of images//
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]

        this.dice_values = [0,0,0,0,0]
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return parseInt(document.getElementById("rolls_remaining").innerText)
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values(){
        return this.dice_values
    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer represenitng the sum of all five dice
    */
    get_sum(){
        let sum = 0
        for (let i=0; i<this.dice_values.length; i++){
            sum += this.dice_values[i];
        }
        return sum
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){
        let counts = [0,0,0,0,0,0]
        for (let i=0; i<this.dice_values.length; i++){
            counts[this.dice_values[i]-1] += 1
        }
        return counts
    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){
        if (this.rolls_remaining_element > 0){
            let randomValues = []
            for (let i=0; i<5; i++){
                if(Array.from(this.dice_elements[i].classList).includes("reserved") === false){
                    randomValues.push(Math.floor((Math.random()*6)+1));
                } else {
                    randomValues.push(-1)
                }
            }
            this.rolls_remaining_element -= 1
            this.set(randomValues, this.rolls_remaining_element)
        }
        return this.dice_values
    } //start with array of five 0's. when roll, add value to it. if reserved, dont change value. if not reserved, set equal to 0 THEN add values

    /**
     * Resets all dice_element pictures to blank, and unreserved.
     * Also resets rolls remaining to 3
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        for (let i=0; i<5; i++){
            if(Array.from(this.dice_elements[i].classList).includes("reserved") === true){
                //console.log(i.toString() + "is reserved, will unrserve it")
                this.reserve(this.dice_elements[i]);
            }
        }
        this.set([0,0,0,0,0], 3);
    }

    /**
     * Performs all necessary actions to reserve/unreserve a particular die
     * <br> Adds "reserved" as a class label to indicate a die is reserved
     * <br> Removes "reserved" a class label if a die is already reserved
     * <br> Hint: use the classlist.toggle method
     *
     * @param {Object} element the <img> element representing the die to reserve
    */
    reserve(die_element){
        const classList = die_element.classList;
        if (this.dice_values.includes(0) === false){
            //console.log("no blank dice here, will reserve")
            classList.toggle("reserved")
        } else {
            //console.log("there are blank dice here, will not reserve")
        }
    }

    /**
     * A useful testing method to conveniently change dice / rolls remaining
     * <br> A value of 0 indicates that the die should be blank
     * <br> A value of -1 indicates that the die should not be updated
     *
     * @param {Array} new_dice_values an array of five integers, one for each die value
     * @param {Number} new_rolls_remaining an integer representing the new value for rolls remaining
     *
    */
    set(new_dice_values, new_rolls_remaining){
        document.getElementById("rolls_remaining").innerText = new_rolls_remaining
        this.rolls_remaining_element = new_rolls_remaining;

        for (let i=0; i<new_dice_values.length; i++){
            if (new_dice_values[i] > -1){
                this.dice_values[i] = new_dice_values[i];
            }
        }
        // console.log(this.dice_values)
        // console.log(this.rolls_remaining_element)

        for (let i=0; i<this.dice_elements.length; i++){
            if (this.dice_values[i] === 0){
                let source = "/img/blank.svg";
                this.dice_elements[i].setAttribute('src', source);
            } else if (this.dice_values[i] > 0) {
                let diceValue = this.photo_names[this.dice_values[i]];
                let source = "/img/" + diceValue + ".svg";
                this.dice_elements[i].setAttribute('src', source);
            }
        }
    }
}

export default Dice;