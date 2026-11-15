"""Sample batch, lessons 1-10: first drafts written by Claude (Opus 5.5) from prompt v2.0,
one per lesson brief, saved exactly as written before any checks ran."""
import json, pathlib
OUT = pathlib.Path(__file__).parent / "outputs"; OUT.mkdir(exist_ok=True)

def save(lid, title, text, inst, name, notes, setting, hooks):
    json.dump({"title": title, "passage_text": text,
               "skill_instances": [{"quote": q, "explanation": e} for q, e in inst],
               "protagonist": {"name": name, "notes": notes}, "setting": setting,
               "lesson_hooks": dict(zip(["hook_question", "i_do", "we_do", "you_do_question"], hooks))},
              open(OUT / f"{lid}.json", "w"), indent=2, ensure_ascii=False)

save("RL-TX-K-001", "The Lost Red Ball",
'''Leo has a red ball. He kicks it high. The ball lands in a tall bush. Oh no! Leo cannot see it.

Leo looks under the slide. No ball. He looks by the gate. No ball.

Then Leo has an idea. He gets a long stick. He pokes the bush gently. Out rolls the red ball! Leo smiles and kicks it again.''',
[("The ball lands in a tall bush.", "This is the problem. Leo's ball is stuck."),
 ("He gets a long stick.", "Leo starts to solve the problem."),
 ("Out rolls the red ball!", "This is how the problem is solved.")],
"Leo", "young boy at a playground", "a neighborhood playground",
["What do you do when you lose something?", "Model the problem sentence: the ball lands in a bush.",
 "Find the sentence where Leo starts to fix the problem.", "How does Leo get his ball back?"])

save("RL-TX-1-002", "Rain on the Roof",
'''Pitter, patter, rain on the roof.
Pitter, patter, puddles grow.
Big brown boots go splish and splash.
Rain, rain, where did you go?

Soft gray clouds slide slowly by.
Sun peeks out to say hello.
Pitter, patter, rain on the roof.
Rain, rain, where did you go?

My mom and I make muddy pies.
We watch the worms wiggle below.
Pitter, patter, the rain is done.
Tomorrow, rain, come back slow!''',
[("Pitter, patter, rain on the roof.", "This line repeats in the poem."),
 ("Rain, rain, where did you go?", "This question repeats at the end of two stanzas."),
 ("Big brown boots", "Alliteration: big and brown start with the same sound."),
 ("clouds slide slowly", "Alliteration: slide and slowly both start with s."),
 ("watch the worms wiggle", "Alliteration: watch, worms and wiggle start with w.")],
None, "child speaker playing with mom after rain", "a home porch and yard on a rainy day",
["What sounds does rain make?", "Model the repeated line 'Pitter, patter, rain on the roof.'",
 "Find two words that start with the same sound in stanza two.", "Which line repeats in the poem?"])

save("RL-TX-1-003", "How a Bean Plant Grows",
'''A bean plant grows in steps. First, a farmer puts a bean seed in the soil. Next, the seed drinks up the rain water. Then a tiny root pushes down into the dirt.

After that, a green shoot pokes up into the sun. Soon the shoot grows big leaves. Last, the plant makes new pods with beans inside. Each pod holds seeds for next year. The steps happen again and again.''',
[("First, a farmer puts a bean seed in the soil.", "First tells us the first step."),
 ("Next, the seed drinks up the rain water.", "Next tells us what happens second."),
 ("Then a tiny root pushes down into the dirt.", "Then shows the next step in order."),
 ("After that, a green shoot pokes up into the sun.", "After that moves us forward in time."),
 ("Last, the plant makes new pods with beans inside.", "Last tells us the final step.")],
None, "informational text, no protagonist", "a farm field",
["How does a seed become a plant?", "Model the signal word First.",
 "Find the step that comes after the root grows.", "What happens last?"])

save("RL-TX-2-004", "Why Bluebonnets Bloom in Spring",
'''Every spring, the roadsides in Texas turn bright blue. This happens because bluebonnet seeds wait in the ground all winter long. When the cool fall rains soak the soil, the seeds start to sprout.

Because the plants grow slowly through the winter, their roots get deep and strong. When spring brings warm sunny days, the plants finally bloom. Bees visit the flowers, so pollen moves from bloom to bloom.

As a result, the plants make new seeds in their fuzzy pods. The pods dry out and pop open in early summer. That is why new bluebonnets appear in the same spots the next year.''',
[("This happens because bluebonnet seeds wait in the ground all winter long.", "Because tells the cause of the blue roadsides."),
 ("When the cool fall rains soak the soil, the seeds start to sprout.", "Rain is the cause; sprouting is the effect."),
 ("Because the plants grow slowly through the winter, their roots get deep and strong.", "Slow growth causes strong roots."),
 ("Bees visit the flowers, so pollen moves from bloom to bloom.", "So shows the effect of bees visiting."),
 ("As a result, the plants make new seeds in their fuzzy pods.", "As a result shows an effect.")],
None, "informational text, no protagonist", "Texas roadsides in spring",
["Have you seen fields of blue flowers in spring?", "Model the cause-and-effect signal word because.",
 "Find the sentence that uses so.", "What causes the seeds to sprout?"])

save("RL-TX-2-005", "Our School Needs a Reading Garden",
'''Our school should build a reading garden by the library. Right now, the space by the library is an empty patch of dirt. I think a garden would be the best place in the whole school.

The library has more than two thousand books. Students could carry those books outside and read under a tree. Plants need sunlight and water to grow. The patch gets sun every morning, and there is a water hose nearby.

Reading outside is more fun than reading inside. A garden would also be beautiful to look at. Please vote yes for the reading garden at our next class meeting!''',
[("Right now, the space by the library is an empty patch of dirt.", "Fact: you can go look and check it."),
 ("I think a garden would be the best place in the whole school.", "Opinion: I think shows what the writer feels."),
 ("The library has more than two thousand books.", "Fact: someone could count the books."),
 ("The patch gets sun every morning, and there is a water hose nearby.", "Fact: this can be checked."),
 ("Reading outside is more fun than reading inside.", "Opinion: other people might feel differently.")],
None, "second-grade student writer", "an elementary school",
["What would make your school a better place?", "Model one fact and one opinion from paragraph one.",
 "Is 'The library has more than two thousand books' a fact or an opinion?", "Find one opinion in the last paragraph."])

save("RL-TX-3-006", "Saving Water at Westfield Elementary",
'''Last spring, students at Westfield Elementary noticed a problem with the school garden. The plants were drying out quickly, and the city had asked everyone to use less water during the long, hot summer. The garden club needed a way to keep the vegetables alive without wasting a single drop.

The students researched ideas at the library and asked a local farmer for advice. She explained that rain barrels can catch water from a roof when storms roll through. The club decided to try this solution. With help from parents, they placed two large barrels under the gutters by the cafeteria.

The next problem was moving the water to the garden. A fourth grader named Rosa suggested using an old hose with tiny holes poked along its side. This simple tool, called a soaker hose, drips water slowly right onto the roots.

By the end of the summer, the garden was green and full of tomatoes. The club had solved its problem by using rain instead of the city's water.''',
[("The plants were drying out quickly, and the city had asked everyone to use less water during the long, hot summer.", "This states the problem."),
 ("She explained that rain barrels can catch water from a roof when storms roll through.", "This gives the first solution."),
 ("The next problem was moving the water to the garden.", "A second problem appears."),
 ("This simple tool, called a soaker hose, drips water slowly right onto the roots.", "This solves the second problem."),
 ("The club had solved its problem by using rain instead of the city's water.", "This sums up how the problem was solved.")],
"Rosa", "fourth-grade garden club member", "a school garden in a Texas city",
["Have you ever had to fix a problem at school?", "Model the problem sentence in paragraph one.",
 "Find the solution to the second problem.", "How did the club get water for the garden?"])

save("RL-TX-3-007", "The Kite Contest",
'''Mateo had waited all month for the neighborhood kite contest at Cedar Park. On Saturday morning, he carried his blue kite to the big field with his older sister, Lina.

Mateo ran as fast as he could, but the kite bumped along the grass. It would not rise. Other kites danced high above the trees, and Mateo felt his face grow hot. The contest would start in ten minutes, and his kite was still on the ground.

Lina pointed to the trees. "Look at the leaves," she said. "Which way is the wind blowing?" Mateo watched the branches sway toward the pond. He turned around so the wind hit his back.

This time, Mateo let out the string slowly. A strong gust lifted the kite, and it climbed higher and higher. When the judges walked by, his blue kite was flying above the tallest oak.

Mateo did not win first place, but he earned a ribbon for the best launch. He decided to always check the wind first.''',
[("Mateo had waited all month for the neighborhood kite contest at Cedar Park.", "The beginning sets up the event."),
 ("It would not rise.", "This is the conflict: the kite won't fly."),
 ("He turned around so the wind hit his back.", "Mateo tries a new plan, the turning point."),
 ("A strong gust lifted the kite, and it climbed higher and higher.", "The plan works as events build."),
 ("Mateo did not win first place, but he earned a ribbon for the best launch.", "This is the resolution.")],
"Mateo", "third grader who solves his own problem after a hint", "a city park on a windy Saturday",
["Have you ever tried to fly a kite?", "Model the conflict: 'It would not rise.'",
 "Find the sentence where Mateo tries something new.", "How does the story end for Mateo?"])

save("RL-TX-4-008", "Summer Storm",
'''The afternoon sky is a bruise of purple and gray,
and the heat sits on the city like a heavy wool blanket.
The trees hold their breath and wait.

Then the wind arrives, a runner late for a race,
rushing down the street and rattling every window.
Thunder grumbles low, like a grandfather clearing his throat
before he tells his longest story.

The first drops tap the porch roof one by one,
as careful as fingers on a piano.
Soon the rain is a marching band,
drumming on cars and splashing in the gutters,
playing its loud song for anyone who will listen.

I press my nose against the cool glass
and count the seconds between flash and boom.
My little brother hides under a quilt,
a turtle tucked inside its shell.

When the storm finally tiptoes away,
the street shines like a fresh new penny.
The trees shake out their wet green hair
and the whole world smells like clean stone.
The sun peeks out from behind a cloud,
shy as a kitten, and the birds begin to sing.''',
[("The afternoon sky is a bruise of purple and gray", "Metaphor: the sky is compared to a bruise without like or as."),
 ("the heat sits on the city like a heavy wool blanket", "Simile: heat is compared to a blanket using like."),
 ("Thunder grumbles low, like a grandfather clearing his throat", "Personification and simile: thunder acts like a person."),
 ("Soon the rain is a marching band", "Metaphor: the rain is called a marching band."),
 ("The trees shake out their wet green hair", "Personification: trees act like people drying their hair.")],
None, "child speaker watching a storm with a younger brother", "a city home during a summer storm",
["What does a thunderstorm sound like to you?", "Model the simile about the heat and the blanket.",
 "Find a line where something that isn't human acts like a person.", "What is the rain compared to in stanza three?"])

save("RL-TX-4-009", "The Day the Bridge Flooded",
'''In the small Hill Country town of Paloma Springs, the low-water bridge was the only quick way to reach Grandma Ruth's ranch across the creek. Every Sunday, Imani and her father drove over it with a cooler of peaches and a stack of library books.

One Sunday in May, heavy storms had rolled through the night before, and the creek had risen high and fast. When they reached the bridge, brown water was rushing over the road, and a bright orange sign warned drivers to turn around.

Imani knew that floodwater can sweep a car away, even when it looks shallow. "We can't cross here," she said, pointing at the sign. Her father agreed, but Grandma Ruth was expecting them, and her phone had no signal on the ranch.

Imani pulled out the paper county map from the glove box. She traced a long gravel road that curved north around the creek to a higher bridge. The trip took an extra forty minutes, but they arrived safely just before lunch.

Grandma Ruth hugged them both and laughed when she saw the map. "That old road kept you dry," she said.''',
[("the low-water bridge was the only quick way to reach Grandma Ruth's ranch across the creek", "The setting creates the route the family depends on."),
 ("heavy storms had rolled through the night before, and the creek had risen high and fast", "A change in the setting causes the problem."),
 ("brown water was rushing over the road, and a bright orange sign warned drivers to turn around", "The flooded setting blocks the plot."),
 ("She traced a long gravel road that curved north around the creek to a higher bridge.", "Imani uses the land itself to find a solution."),
 ("The trip took an extra forty minutes, but they arrived safely just before lunch.", "The setting shapes how the story ends.")],
"Imani", "fourth grader who knows flood safety and leads the solution", "a Texas Hill Country town after a storm",
["Why do you think Texas roads have 'Turn Around, Don't Drown' signs?", "Model how the flooded creek causes the problem.",
 "Find how Imani uses the land to solve the problem.", "How would the story change if there had been no storm?"])

save("RL-TX-5-010", "Should Our School Start Later?",
'''Our school day begins at 7:35 in the morning, and many fifth graders arrive feeling tired and grumpy. As a member of the student council, I believe our school board should move the start time to 8:30 so that students can learn at their best.

Scientists who study sleep report that children between six and twelve years old need nine to twelve hours of sleep each night. A student who must wake up at 6:15 would need to fall asleep by 8:15 the night before to get even nine hours, which is hard for families with busy evenings.

Our own school survey supports this idea. Last fall, 64 percent of fifth graders said they felt sleepy during their first class, and teachers reported that morning quizzes had lower scores than afternoon quizzes.

Some parents worry that a later start would make it harder to get to work on time. That is a fair concern, so the council suggests opening the cafeteria at 7:30 for students who need to arrive early, with quiet reading and breakfast available.

When students sleep enough, they listen better, remember more, and treat one another with more kindness. Please support a later start time at the next school board meeting.''',
[("children between six and twelve years old need nine to twelve hours of sleep each night", "A fact from sleep scientists that supports the argument."),
 ("64 percent of fifth graders said they felt sleepy during their first class", "A survey fact the writer uses for the argument."),
 ("teachers reported that morning quizzes had lower scores than afternoon quizzes", "Another fact used to support a later start."),
 ("Some parents worry that a later start would make it harder to get to work on time.", "A point against the argument that the writer addresses.")],
None, "fifth-grade student council member", "an elementary school",
["Do you feel ready to learn first thing in the morning?", "Model how the sleep fact supports the writer's argument.",
 "Find a fact that comes from the school survey.", "Which sentence gives a reason against a later start?"])
