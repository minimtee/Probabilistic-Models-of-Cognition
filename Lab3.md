## Exercise 1: Fair coins and biased coins

### a)

I flip a fair coin. What is the probability that it lands heads?
P(H) = 0.5
~~~~
var model = function() {
  flip()? "H":"T";
}
var log_prob = Infer({method:'enumerate'}, model).score('H')
Math.exp(log_prob)
~~~~

### b)

I also have a biased coin, with $$P(\text{heads})=0.9$$.
I hand you one of the coins (either biased or fair) without telling you which.
You flip it three times.

Given that first two coin flips landed on heads, what is the posterior distribution for the next flip?

~~~~
var trial = function(state) {
  return state=="F" ? flip() : flip(0.9);
}

var model = function() {
  var state = flip() ? "F" : "B";
  var f1 = trial(state);
  var f2 = trial(state);
  var f3 = trial(state);
  condition(f1 && f2);
  return f3;
}
viz.table(Infer({method:'enumerate'}, model))
~~~~
Through running the function, we can get P(H) = 0.8056603773584906.

### c)

Given that all three flips landed on heads, what is the probability that the coin was biased?
~~~~
var trial = function(state) {
  return state=="F" ? flip() : flip(0.9);
}

var model = function() {
  var state = flip() ? "F" : "B";
  var f1 = trial(state);
  var f2 = trial(state);
  var f3 = trial(state);
  condition(f1 && f2 &&f3);
  return state;
}
viz.table(Infer({method:'enumerate'}, model))
~~~~
Through running the program above, we can get P(B)= 0.8536299765807963.

### d)

Given that the first two flips were different, what is the probability that the third flip will be heads?
~~~~
var trial = function(state) {
  return state=="F" ? flip() : flip(0.9);
}

var model = function() {
  var state = flip() ? "F" : "B";
  var f1 = trial(state);
  var f2 = trial(state);
  var f3 = trial(state);
  condition(f1 != f2);
  return f3;
}
viz.table(Infer({method:'enumerate'}, model))
~~~~
Through running the program above, we can get P(H) = 0.6058823529411763.

## Exercise 2: Conditioning and Intervention

In the earlier [Medical Diagnosis]({{site.baseurl}}/chapters/02-generative-models.html#example-causal-models-in-medical-diagnosis) section we suggested understanding the patterns of symptoms for a particular disease by changing the prior probability of the disease such that it is always true (also called the *do* operator).

~~~~
var lungCancer = flip(0.01);
var cold = flip(0.2);
var cough = (
  (cold && flip(0.5)) ||
  (lungCancer && flip(0.3))
)
cough;
~~~~
Condition:
~~~~
condition(lungCancer == true)
~~~~
intervention:
~~~~
var lungCancer = true;
~~~~

### a)

For this example, does intervening on the program in this way (e.g. by setting the value of `lungCancer`) have the same effect as *conditioning* on the disease being true? What about the casual dependency makes this case?
They have the same effect.

### b)

Why would intervening have a different effect than conditioning for more general hypotheticals? Construct an example where they differ. Then translate this into a WebPPL model and show that manipulating the prior gives different answers than manipulating the observation. *Hint:* think about the effect that intervening vs. conditioning on a variable that has a **causal parent** would have on that parent.

~~~~
//  intervening
display(" intervening")
viz.table(Infer({method: "enumerate"}, function() {
  var lungCancer = flip();
  var cold = flip(0.2);
  var cough = (
    (cold && flip(0.5)) ||
    (lungCancer && flip(0.3))
  )
  var cough=true;
  return lungCancer;
}));

// conditioning
display("conditioning")
viz.table(Infer({method: "enumerate"}, function() {
  var lungCancer = flip();
  var cold = flip(0.2);
  var cough = (
    (cold && flip(0.5)) ||
    (lungCancer && flip(0.3))
  )
  condition(cough == true)
  return lungCancer;
}));
~~~~

## Exercise 3: Computing marginals

Use the rules for computing probabilities to compute the marginal distribution on return values from these programs by hand (use `viz()` to check your answers):

### a)

~~~~
viz.table（Infer({method: "enumerate"}, function() {
  var a = flip();
  var b = flip();
  condition(a || b);
  return a;
})）
~~~~
P(A|A ∪ B) = P(A ∩ (A ∪ B)) / P (A ∪ B)
           = 0.5 / 1 - 0.5*0.5 = 0.75  

### b)

~~~~
var smilesModel = function() {
  var nice = mem(function(person) {return flip(.7)});
  var smiles = function(person) {return nice(person) ? flip(.8) : flip(.5);}
  condition(smiles('alice') && smiles('bob') && smiles('alice'));
  return nice('alice');
}

viz.table(Infer({method: "enumerate"}, smilesModel))
~~~~

## Exercise 4: Extending the smiles model

### a)

70% percent of people are nice. Nice person prefer to smile more than others.
In the condition of that Alice smiles twice and Bob smiles once, determine
whether Alice is nice or not.

### b)

Extend `smilesModel` to create a version of the model that also captures these two intuitions:

1. people are more likely to smile if they want something and
2. *nice* people are less likely to want something.

Note: Do not lose the fact that niceness is also a risk factor for smiling.

*Hint:* Which variables change at different times for the same person?
Which values *depend* on other values?

~~~~
var extendedSmilesModel = function() {
  var nice = mem(function(person) {return flip(.7)});

  var greedy = function(person){return nice(person) ? flip(.4) : flip(.8);}

  var smiles = function(person, desire) {
    return (nice(person) ? flip(.8) : flip(.5)|| desire ? flip(.8):flip(.5))
  }
  var aliceSmiles = greedy('alice');
  return smiles('alice','aliceSmiles')
}

viz.table(Infer({method: "enumerate"}, extendedSmilesModel))
~~~~

### c)

Suppose you've seen Bob five times this week and each time, he was not smiling. But today, you see Bob and he *is* smiling.
Use this `extendedSmilesModel` model to compute the posterior belief that Bob wants something from you today.

*Hint:* How will you represent the same person (Bob) smiling *multiple times*?
What features of Bob will stay the same each time he smiles (or doesn't) and what features will change?

In your answer, show the WebPPL inference and a histogram of the answers -- in what ways do these answers make intuitive sense or fail to?

~~~~
var extendedSmilesModel = function() {
  var nice = mem(function(person) {return flip(.7)});

  var greedy = function(person){ return nice(person) ? flip(.4) : flip(.8);}

  var smiles = function(person, desire) {
    return (nice(person) ? flip(.8) : flip(.5)|| desire ? flip(.8):flip(.5))
  }
  var bobSmiles = greedy('bob');
  condition(smiles('bob',aliceSmiles)&&!smiles('bob',greedy('bob'))&&!smiles('bob',greedy('bob'))&&!smiles('bob',greedy('bob'))&&!smiles('bob',greedy('bob'))&&!smiles('bob',greedy('bob')))
  return bobSmiles
}

viz.table(Infer({method: "enumerate"}, extendedSmilesModel))
~~~~


Question 5: Sprinklers, Rain and mem

### a)

I have a particularly bad model of the sprinkler in my garden.
It is supposed to water my grass every morning, but is turns on only half the time (at random, as far as I can tell).
Fortunately, I live in a city where it also rains 30% of days.

One day I check my lawn and see that it is wet, meaning that either it rained that morning or my sprinkler turned on (or both).

Answer the following questions, either using the Rules of Probability or by writing your own sprinkler model in webppl.

* What is the probability that it rained?
* What is the probability that my sprinkler turned on?

~~~~
* P(R) = 0.46153846153846156
* P(S) = 0.7692307692307692

viz.table(Infer({method: "enumerate"}, function(){
  var s = flip();
  var r = flip(0.3);
  var lawnIsWet = s || r;
  condition(lawnIsWet);
  return r; }))

viz.table(Infer({method: "enumerate"}, function() {
  var s = flip();
  var r = flip(0.3);
  var lawnIsWet = s || r;
  condition(lawnIsWet);
  return s;
}))
~~~~

### c)

My neighbour Kelsey, who has the same kind of sprinkler, tells me that her lawn was also wet that same morning.
What is the new posterior probability that it rained?

~~~~
viz.table(Infer({method: "enumerate"}, function() {
  var r = flip(0.3);
  var sprinkler = flip();
  var kelseySprinkler = flip();
  var lawn = spr|| r;
  var kelseyLawn = kelseySprinkler || r;
  condition(lawn && kelseyLawn);
  return r;
}))
~~~~

### d)

To investigate further we poll a selection of our friends who live nearby, and ask if their grass was wet this morning.
Kevin and Manu and Josh, each with the same sprinkler, all agree that their lawns were wet too.
Using `mem`, write a model to reason about arbitrary numbers of people, and then use it to find the new probability that it rained.

~~~~
P(R) = 0.9320388349514566
~~~~


## Exercise 5: Casino game

Consider the following game.
A machine randomly gives Bob a letter of the word "game"; it gives a, e (the vowels) with probability 0.45 each and the remaining letters (the consonants g, m) with probability 0.05 each.
The probability that Bob wins depends on which letter he got.
Letting $$h$$ denote the letter and letting $$Q(h)$$ denote the numeric position of that letter in the word "game" (e.g., $$Q(\text{g}) = 1, Q(\text{a}) = 2$$, and so on), the probability of winning is $$1/Q(h)^2$$.

Suppose that we observe Bob winning but we don't know what letter he got.
How can we use the observation that he won to update our beliefs about which letter he got?
Let's express this formally.
Before we begin, a bit of terminology: the set of letters that Bob could have gotten, $$\{g, a, m, e\}$$, is called the *hypothesis space* -- it's our set of hypotheses about the letter.

### a)

In English, what does the posterior probability $$p(h \mid \text{win})$$ represent?

In the conditon of win, what letter will Bob get?

### b)

Manually compute $$p(h \mid \text{win})$$ for each hypothesis.
Remember to normalize --- make sure that summing all your $$p(h \mid \text{win})$$ values gives you 1.

| $$h$$ | $$p(h)$$ | $$p(\text{win}\mid h)$$ | $$p(h \mid \text{win})$$ |
| ----- | -------- | ------------------------|------------------------- |
| g     | 0.05     |       1                 |         .255                 |
| a     | 0.45     |     .25                 |        .573                  |
| m     | 0.05     |     .11                 |         .028                 |
| e     | 0.45     |     .0625               |            .143              |

### d)


Now, we're going to write this model in WebPPL using `Infer`. Here is some starter code for you:

~~~~
// define some variables and utility functions
var checkVowel = function(letter) {return _.includes(['a', 'e', 'i', 'o', 'u'], letter);}
var letterVals = ['g', 'a', 'm', 'e'];
var letterProbs = map(function(letter) {return checkVowel(letter) ? 0.45 : 0.05;}, letterVals);
var letters = Categorical({vs: letterVals, ps: letterProbs})

// Compute p(h | win)
var distribution = Infer({method: 'enumerate'}, function() {
  var letter = sample(letters);
  var position = letterVals.indexOf(letter) + 1;
  var winProb = 1 / Math.pow(position, 2);
  condition(win)
  return letter;
});
viz.auto(distribution);
~~~~

Fill in the `...`'s in the code to compute $$p(h \mid \text{win})$$.
Include a screenshot of the resulting graph.
What letter has the highest posterior probability?
In English, what does it mean that this letter has the highest posterior?
It might be interesting to comment out the `condition` statement so you can compare visually the prior (no `condition` statement) to the posterior (with `condition`).

Make sure that your WebPPL answers and hand-computed answers agree -- note that this demonstrates the equivalence between the program view of conditional probability and the distributional view.

### e)

Which is higher, $$p(\text{vowel} \mid \text{win})$$ or $$p(\text{consonant} \mid \text{win})$$?
Answer this using the WebPPL code you wrote *Hint:* use the `checkVowel` function.

~~~~
// define some variables and utility functions
var checkVowel = function(letter) {return _.includes(['a', 'e', 'i', 'o', 'u'], letter);}
var letterVals = ['g', 'a', 'm', 'e'];
var letterProbs = map(function(letter) {return checkVowel(letter) ? 0.45 : 0.05;}, letterVals);
var letters = Categorical({vs: letterVals, ps: letterProbs})

// Compute p(h | win)
var distribution = Infer({method: 'enumerate'}, function() {
  var letter = sample(letters);
  var position = letterVals.indexOf(letter) + 1;
  var winProb = 1 / Math.pow(position, 2);
  condition(flip(winProb))
  return checkVowel(letter)
});
viz.auto(distribution);
~~~~

p(vowel∣win) = 	0.7168141592920354
p(consonant∣win) = 0.28318584070796465

### f)

What difference do you see between your code and the mathematical notation?
What are the advantages and disadvantages of each?
Which do you prefer?
My code can deal with data and math notation are mostly used for calculation.
