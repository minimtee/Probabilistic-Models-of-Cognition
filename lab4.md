## Exercise 1: Causal and statistical dependency.

For each of the following programs:

* Draw the dependency diagram (Bayes net). If you don't have software on your computer for doing this, Google Docs has a decent interface for creating drawings.

* Use informal evaluation order reasoning and the intervention method to determine causal dependency between A and B.

* Use conditioning to determine whether A and B are statistically dependent.

a)

~~~~
var a = flip()
var b = flip()
var c = flip(a && b ? .8 : .5)
~~~~

b)

~~~~
var a = flip()
var b = flip(a ? .9 : .2)
var c = flip(b ? .7 : .1)
~~~~

c)

~~~~
var a = flip()
var b = flip(a ? .9 : .2)
var c = flip(a ? .7 : .1)
~~~~

d)

~~~~
var a = flip(.6)
var c = flip(.1)
var z = flip() ? a : c;
var b = z ? 'foo' : 'bar'
~~~~

e)

~~~~
var examFairPrior = Bernoulli({p: .8})
var doesHomeworkPrior = Bernoulli({p: .8})
var examFair = mem(function(exam) {return sample(examFairPrior)})
var doesHomework = mem(function(student) {return sample(doesHomeworkPrior)});

var pass = function(student, exam) {
  return flip(examFair(exam) ?
              (doesHomework(student) ? .9 : .5) :
              (doesHomework(student) ? .2 : .1));
}
var a = pass('alice', 'historyExam');
var b = pass('bob', 'historyExam');
~~~~

## Exercise 2: Epidemiology

Imagine that you are an epidemiologist and you are determining people's cause of death. In this simplified world, there are two main diseases, cancer and the common cold. People rarely have cancer, $$p( \text{cancer}) = 0.00001$$, but when they do have cancer, it is often fatal, $$p( \text{death} \mid \text{cancer} ) = 0.9$$. People are much more likely to have a common cold, $$p( \text{cold} ) = 0.2$$, but it is rarely fatal, $$p( \text{death} \mid \text{cold} ) = 0.00006$$. Very rarely, people also die of other causes $$p(\text{death} \mid \text{other}) = 0.000000001$$.

Write this model in WebPPL and use `Infer` to answer these questions (Be sure to include your code in your answer):

~~~~
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  return {cancer: cancer, cold: cold, death: death};
}));
~~~~

a) Compute $$p( \text{cancer} \mid \text{death} , \text{cold} )$$ and $$p( \text{cancer} \mid \text{death} , \text{no cold} )$$. How do these probabilities compare to $$p( \text{cancer} \mid \text{death} )$$ and $$p( \text{cancer} )$$? Using these probabilities, give an example of explaining away.

~~~~
display("death with cold")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death&&cold)
  return {cancer: cancer};
}));

display("death without cold")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death && !cold)
  return {cancer: cancer};
}));

display("cancer death")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death)
  return {cancer: cancer};
}));

display("cancer")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  return {cancer: cancer};
}));

~~~~



b) Compute $$p( \text{cold} \mid \text{death} , \text{cancer} )$$ and $$p( \text{cold} \mid \text{death} , \text{no cancer} )$$. How do these probabilities compare to $$p( \text{cold} \mid \text{death} )$$ and $$p( \text{cold} )$$? Using these probabilities, give an example of explaining away.

~~~~
display("death by cold")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death)
  return {cold: cold};
}));

display("death with cancer")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death && cancer)
  return {cold: cold};
}));

display("death without cancer")
viz.table(Infer({method: 'enumerate'}, function() {
  var cancer = flip(0.00001)
  var cold = flip(0.2)
  var death = (cancer && flip(0.9)) || (cold && flip(0.00006)) || flip(0.000000001)
  condition(death && !cancer)
  return {cold: cold};
}));
~~~~
