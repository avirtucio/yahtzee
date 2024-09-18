console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element;
        this.dice_elements= dice_elements; //array of images//
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]

        this.dice_values = []
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        return this.rolls_remaining_element
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
            for (let i=0; i<5; i++){
                if (this.dice_values[i] != 0){
                    console.log(this.dice_elements[i])
                    console.log(this.dice_elements[i].classList)
                    if (Array.from(this.dice_elements[i].classList).includes("reserved") === false){
                        this.dice_values[i]=(Math.floor((Math.random()*6)+1));
                    }
                } else {
                    this.dice_values.push(Math.floor((Math.random()*6)+1));
                }
            }
        }
        this.rolls_remaining_element = this.rolls_remaining_element -1
        return this.dice_values
    } //start with array of five 0's. when roll, add value to it. if reserved, dont change value. if not reserved, set equal to 0 THEN add values

    /**
     * Resets all dice_element pictures to blank, and unreserved.
     * Also resets rolls remaining to 3
     * <br> Uses this.#setDice to update dice
    */
    reset(){

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
        classList.toggle("reserved")
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

    }
}

export default Dice;