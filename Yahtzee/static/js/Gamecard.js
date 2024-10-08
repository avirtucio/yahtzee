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
        for (let i=0; i<this.category_elements.length; i++){
            if (this.category_elements[i].hasAttribute("disabled") == false){
                return false
            } else {
                return true
            }
        }
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
        if (this.dice.dice_values.includes(0) === true){
            return false;
        }
        let dice_counts = Object.assign([], this.dice.get_counts())
        let straight_counter = this.dice.get_counts().reduce(function(acc, el, index){
            if (el == 0){
                if (acc==5){
                    return acc
                } else if (acc==4){
                    if ((index < 5) && (dice_counts[index+1] == 1)){
                        return 3
                    } else {
                        return acc
                    }
                } else {
                    return 0
                }
            } else if ((el==1) || (el==2)){
                return acc+1
            } else {
                return 0
            }
        }, 0);
        console.log(typeof value)
        if (typeof value === 'string'){
            return false;
        } else if (value === 0){
            return true;
        } else if (value < 0){
            return false;
        } else if (this.dice.photo_names.includes(category) === true){
            let category_int = this.dice.photo_names.indexOf(category);
            if (this.dice.get_counts()[category_int-1]*category_int == value){
                return true;
            } else {
                return false;
            }
        } else if (category === 'full_house'){
            if ((this.dice.get_counts().includes(3) === true)&&(this.dice.get_counts().includes(2) === true)){
                if (value == 25){
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } else if (category === 'chance'){
            if (value == this.dice.get_values().reduce(function(acc,el){
                return acc + el;
            }, 0)){
                return true;
            } else {
                return false;
            }
        } else if (this.dice.get_counts().includes(5) === true){
            if (category === 'yahtzee'){
                if (value == 50){
                    return true;
                } else {
                    return false;
                }
            } else if (category === 'four_of_a_kind'){
                let real_score = this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0);
                if (real_score == value){
                    return true;
                } else {
                    return false;
                }
            } else if (category === 'three_of_a_kind'){
                if (this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0) == value){
                    return true;
                } else {
                    return false;
                }
            }
        } else if (this.dice.get_counts().includes(4) === true){
            if (category === 'four_of_a_kind'){
                let real_score = this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0);
                if (real_score == value){
                    return true;
                } else {
                    return false;
                }
            } else if (category === 'three_of_a_kind'){
                if (this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0) == value){
                    return true;
                } else {
                    return false;
                }
            }
        } else if (this.dice.get_counts().includes(3) === true){
            if (category === 'three_of_a_kind'){
                if (this.dice.get_counts().reduce(function(acc, el, index){
                    return acc+((index+1)*el);
                }, 0) == value){
                    return true;
                } else {
                    return false;
                }
            } 
        } 
        if (straight_counter == 5){
            if (category === 'large_straight'){
                if (value == 40){
                    return true;
                } else {
                    return false;
                }
            } else if (category === 'small_straight'){
                if (value == 30){
                    return true;
                } else {
                    return false;
                }
            }
        } else if (straight_counter == 4){
            if (category === 'small_straight'){
                if (value == 30){
                    return true;
                } else {
                    return false;
                }
            }
        } else {
            return false;
        }
    } 

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){
        return parseInt(document.getElementById("grand_total").textContent);
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       document.getElementById("upper_score").value = Array.from(document.getElementsByClassName("upper")).reduce(function(acc, el, index){
        if (index <= 6){
            return acc + parseInt(el.value)
        } else {
            return acc
        }
       }, 0);

       if (document.getElementById("upper_score").value > 63){
        document.getElementById("upper_bonus").value = 35;
       } else {
        document.getElementById("upper_bonus").value = 0;
       }

       document.getElementById("upper_total").value = document.getElementById("upper_score").value + document.getElementById("upper_bonus").value;

       document.getElementById("lower_score").value = Array.from(document.getElementsByClassName("lower")).reduce(function(acc, el, index){
        if (index <= 6){
            return acc + parseInt(el.value)
        } else {
            return acc
        }
       }, 0);

       document.getElementById("upper_total_lower").value = document.getElementById("upper_total").value;

       document.getElementById("grand_total").value = parseInt(document.getElementById("grand_total").innerText);
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
       let scorecard = JSON.parse(score_info);
       this.dice.rolls_remaining_element = scorecard["rolls_remaining"];
       scorecard["upper"].forEach(function(key){
        let category_id = key+"_input"
    
       });

       return scorecard
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
      let scorecard = {};
      scorecard["rolls_remaining"] = this.dice.get_rolls_remaining();
      scorecard["upper"] = {};
      scorecard["lower"] = {};
      let upper = Array.from(document.getElementsByClassName("upper"));
      for (let i=0; i<6; i++){
        let category = upper[i].id.split("_");
        category.pop();
        category = category.join("_");
        if (upper[i].value){
            scorecard["upper"][category] = parseInt(upper[i].value);
        } else {
            scorecard["upper"][category] = -1
        }
      }
      let lower = Array.from(document.getElementsByClassName("lower"));
      for (let i=0; i<6; i++){
        let category = lower[i].id.split("_");
        category.pop();
        category = category.join("_");
        if (lower[i].value){
            scorecard["lower"][category] = parseInt(lower[i].value);
        } else {
            scorecard["lower"][category] = -1
        }
      }
      return scorecard
    }
}

export default Gamecard;





