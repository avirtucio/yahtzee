class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements;
        this.dice=myDice;
        this.score_elements=score_elements;
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){

    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){
        if (this.dice.photo_names.includes(category) === true){
            let category_int = this.dice.photo_names.indexOf(category);
            if (this.dice.get_counts()[category_int-1]*category_int === value){
                return true;
            } else {
                return false;
            }
        } else if (category === 'three_of_a_kind'){
            if (this.dice.get_counts().includes(3) === true){
                if (this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0) === value){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'four_of_a_kind'){
            if (this.dice.get_counts().includes(4) === true){
                let real_score = this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0);
                if (real_score === value){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'full_house'){
            if ((this.dice.get_counts().includes(3) === true)&&(this.dice.get_counts().includes(2) === true)){
                if (value === 25){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'small_straight'){
            let straight_counter = this.dice.get_counts().reduce(function(acc, el){
                return acc+el
            }, 0);
            if (straight_counter === 4){
                if (value === 30){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'large_straight'){
            let straight_counter = this.dice.get_counts().reduce(function(acc, el){
                return acc+el
            }, 0);
            if (straight_counter === 5){
                if (value === 40){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'yahtzee'){
            if (this.dice.get_counts().includes(5) === true){
                if (value === 50){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'chance'){
            if (value === this.dice.get_values().reduce(function(acc,el){
                return acc + el;
            }, 0)){
                return true;
            } else {
                return false;
            }
        }
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){

    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       
    }

    /**
     * Loads a scorecard from a JS object in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(score_info){
       
    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */
    to_object(){
      
    }
}

export default Gamecard;





