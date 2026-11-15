"""v2.1 sample batch, lessons 1-10 (K-5): first drafts written by Claude (Opus 5.5)
from prompt v2.1 (rendered prompts in prompts_rendered.jsonl), one per lesson brief,
saved exactly as written before any checks ran."""
import json, pathlib
OUT = pathlib.Path(__file__).parent / "outputs"; OUT.mkdir(exist_ok=True)

def save(lid, title, text, inst, name, notes, setting, hooks):
    json.dump({"title": title, "passage_text": text,
               "skill_instances": [{"quote": q, "explanation": e} for q, e in inst],
               "protagonist": {"name": name, "notes": notes}, "setting": setting,
               "lesson_hooks": dict(zip(["hook_question", "i_do", "we_do", "you_do_question"], hooks))},
              open(OUT / f"{lid}.json", "w"), indent=2, ensure_ascii=False)

save("RL-TX-K-001", "Mia's Kite",
'''Mia has a kite. It is blue and yellow. The wind blows hard. The kite gets stuck in a tree! She cannot reach it. Mia is sad.

Mia thinks. She tugs the string slowly. Tug, tug, tug. The kite wiggles free. Down it floats into her hands. She smiles big. Mia runs to the hill. Her kite flies high again.''',
[("The kite gets stuck in a tree!", "This is the problem. Mia's kite is stuck."),
 ("She tugs the string slowly.", "Mia starts to fix the problem."),
 ("The kite wiggles free.", "This is how the problem is solved.")],
"Mia", "young girl flying a kite", "a park with a hill",
["What would you do if your toy got stuck?",
 "Model the problem first: 'The kite gets stuck in a tree!' It is where the trouble starts.",
 "Students find the sentence where Mia starts to fix it: 'She tugs the string slowly.'",
 "How does Mia get her kite back?"])

save("RL-TX-1-002", "Drip, Drop, the Garden Wakes",
'''Drip, drop, the garden wakes.
Drip, drop, the green grass grows.
Bees buzz by the big blue pot.
Drip, drop, the garden wakes.

Sam and I dig in the dirt.
We plant six small seeds in a row.
Worms wiggle, wiggle, wiggle down.
Drip, drop, the garden wakes.

Red roses rise up to the sun.
Tall, tall sunflowers nod hello.
We water, wait, and watch them grow.
Drip, drop, the garden wakes.

Night comes soft and slow.
The moon says, "Rest now, seeds."
Tomorrow we will dig some more.
Drip, drop, the garden wakes.''',
[("Drip, drop, the garden wakes.", "This line repeats at the end of every stanza."),
 ("Bees buzz by the big blue pot.", "Alliteration: bees, buzz, by, big and blue all start with b."),
 ("Worms wiggle, wiggle, wiggle down.", "Wiggle repeats, and worms and wiggle both start with w."),
 ("Red roses rise", "Alliteration: red, roses and rise all start with r."),
 ("We water, wait, and watch them grow.", "Alliteration: water, wait and watch all start with w.")],
None, "child speaker gardening with a friend, Sam", "a backyard garden on a rainy spring day",
["What sounds does rain make in a garden?",
 "Model the repeated line 'Drip, drop, the garden wakes.' because it comes back four times.",
 "Students find the b sounds in 'Bees buzz by the big blue pot.'",
 "Which line repeats at the end of every stanza?"])

save("RL-TX-1-003", "From Egg to Frog",
'''A frog starts life as a tiny egg. First, a mother frog lays eggs in a pond. The eggs look like clear jelly with black dots.

Next, a tadpole hatches from each egg. A tadpole has a long tail. It swims and eats small plants.

Then the tadpole grows two back legs. After that, two front legs grow too. The tail gets shorter and shorter.

Last, the young frog hops out of the water. Now it can live on land. Someday it will lay eggs too.''',
[("First, a mother frog lays eggs in a pond.", "First tells us the first step."),
 ("Next, a tadpole hatches from each egg.", "Next tells us what happens second."),
 ("Then the tadpole grows two back legs.", "Then shows the next step in order."),
 ("After that, two front legs grow too.", "After that moves us forward in time."),
 ("Last, the young frog hops out of the water.", "Last tells us the final step.")],
None, "informational text, no protagonist", "a pond",
["How does a tiny egg become a frog?",
 "Model the signal word First, because it starts the order.",
 "Students find the word that comes after Next.",
 "What happens last in the frog's life cycle?"])

save("RL-TX-2-004", "Why Puddles Disappear",
'''After a rain, our playground is full of puddles. By lunch, many of them are gone. Where does the water go? It does not just sink into the ground.

The sun warms the puddle. Because the water gets warm, tiny bits of it rise into the air. This is called evaporation. You cannot see it happen, but it is always going on.

Wind helps too. When the wind blows across a puddle, the water dries faster. That is why puddles shrink quickly on windy days.

Shade does the opposite. A puddle under a tree stays cool, so it lasts much longer. Next time it rains, watch two puddles. One in the sun and one in the shade will dry at different speeds.''',
[("Because the water gets warm, tiny bits of it rise into the air.", "Because tells the cause: warm water rises into the air."),
 ("When the wind blows across a puddle, the water dries faster.", "The wind is the cause. Drying faster is the effect."),
 ("That is why puddles shrink quickly on windy days.", "That is why points to an effect."),
 ("A puddle under a tree stays cool, so it lasts much longer.", "So tells the effect of staying cool.")],
None, "informational text, no protagonist", "a school playground after rain",
["Where do puddles go after it rains?",
 "Model the signal word because in the sun sentence, since it names the cause.",
 "Students find the cause and effect in the wind sentence.",
 "Why does a puddle in the shade last longer?"])

save("RL-TX-2-005", "Let's Keep Our Class Fish",
'''Our class has a goldfish named Bubbles. Some people want to give him away. I think we should keep him.

Here are some facts. Bubbles lives in a tank by the window. Bubbles is three years old. He eats one pinch of food each morning. Taking care of him takes about five minutes a day. Our class made a chart, and every student gets a turn.

Now here is my opinion. Bubbles is the best part of our room. Watching him swim makes me feel calm. I think caring for him teaches us to be kind and careful.

Some people say a fish is too much work. But the facts show it is only a few minutes. Please vote to keep Bubbles!''',
[("He eats one pinch of food each morning.", "This is a fact. You can check it."),
 ("Taking care of him takes about five minutes a day.", "This is a fact. You can time it."),
 ("Bubbles is the best part of our room.", "This is an opinion. Not everyone may agree."),
 ("Watching him swim makes me feel calm.", "This is an opinion about a feeling."),
 ("I think caring for him teaches us to be kind and careful.", "I think tells us this is an opinion.")],
None, "second-grade student speaker", "a second-grade classroom",
["How can you tell a fact from an opinion?",
 "Model a fact first: 'He eats one pinch of food each morning.' It can be checked.",
 "Students sort 'Bubbles is the best part of our room.' as fact or opinion.",
 "Which sentence is a fact: 'Bubbles is three years old' or 'Bubbles is the best part of our room'?"])

save("RL-TX-3-006", "The Lunchroom Noise Problem",
'''At Pecan Grove Elementary, the lunchroom used to be very loud. Two hundred students ate there at the same time. Kids had to shout to hear their friends. It was hard to think, too. Some students said the noise gave them headaches.

The fourth graders decided to solve the problem. First, they used a sound meter to measure the noise. A sound meter is a tool that shows how loud a room is. The meter showed that the room was loudest when trays banged on the tables.

The students came up with three ideas. They put soft felt pads under every tray. They hung cloth banners on the bare walls, because cloth soaks up sound. They also made a hand signal that means "use quiet voices." Each idea cost very little money.

After two weeks, they measured again. The room was much quieter. The noise meter showed the sound had dropped by almost half. Now friends can talk without shouting, and lunch feels calm again.''',
[("Kids had to shout to hear their friends.", "This shows the problem: the room was too loud."),
 ("They put soft felt pads under every tray.", "This is one solution to the banging trays."),
 ("They hung cloth banners on the bare walls, because cloth soaks up sound.", "This is a second solution, and it tells why it works."),
 ("The room was much quieter.", "This shows the solutions worked.")],
None, "informational text about a group of fourth graders", "an elementary school lunchroom in Texas",
["What makes a room too loud?",
 "Model the problem sentence: 'Kids had to shout to hear their friends.'",
 "Students find one solution in the third paragraph.",
 "What did the students use to measure the noise?"])

save("RL-TX-3-007", "The Missing Library Book",
'''On Monday, Rosa checked out a book about sea turtles. It had bright pictures of baby turtles racing to the ocean. She read it every night that week. On Friday, the book was due back at the library.

Friday morning, Rosa looked in her backpack. The book was not there. She checked under her bed and behind the couch. Her heart beat fast. She did not want to tell the librarian that she had lost it.

Rosa sat down and thought hard. Where had she read the book last? She remembered reading on the porch swing after dinner, so she ran outside to look.

There was the book, tucked between two cushions. The cover was a little damp from the morning dew, but it was fine. Rosa let out a long, happy breath. Rosa dried it with a towel and put it in her backpack.

At school, she told the librarian what had happened. The librarian smiled and said that thinking back was a smart plan. Rosa checked out a new book that day.''',
[("On Monday, Rosa checked out a book about sea turtles.", "This is the first event in the sequence."),
 ("The book was not there.", "This is the conflict: Rosa's book is missing."),
 ("She did not want to tell the librarian that she had lost it.", "This shows why the conflict matters to Rosa."),
 ("There was the book, tucked between two cushions.", "This is the resolution: Rosa finds the book."),
 ("At school, she told the librarian what had happened.", "This is one of the last events in the sequence.")],
"Rosa", "third grader who loves animal books", "Rosa's home and school library",
["Have you ever lost something you needed?",
 "Model the conflict: 'The book was not there.' This is where the problem starts.",
 "Students find the sentence where the conflict is resolved.",
 "Where does Rosa find the book?"])

save("RL-TX-4-008", "Thunderstorm Over the Plains",
'''The sky is a gray blanket pulled over the town.
The wind whistles through the fence like a tired train.
Our old oak tree shakes its arms and groans.
Even the grass bends low to hide.

Then thunder is a drum the clouds are playing.
Boom, it rolls across the wide, flat fields.
Lightning dances on the edge of the world,
quick as a cat that jumps and is gone.

Rain comes running down the street.
It taps on every window, asking to come in.
The gutters gulp and gurgle,
hungry mouths that cannot drink enough.

My little brother hides under a quilt,
a turtle in a soft, warm shell.
I sit by the window with my cocoa
and count the seconds between flash and boom.

At last the storm grows sleepy.
It yawns one long, low rumble
and tiptoes off toward Oklahoma.
The sun peeks out like a shy friend,
and the puddles shine like coins.

I step outside in my boots.
The air smells clean and new,
like the whole world just took a bath,
and the oak tree stands up tall again.
Tomorrow the fields will be greener than green.''',
[("The sky is a gray blanket pulled over the town.", "Metaphor: the sky is compared to a blanket without using like or as."),
 ("The wind whistles through the fence like a tired train.", "Simile: the wind's sound is compared to a train using like."),
 ("Our old oak tree shakes its arms and groans.", "Personification: the tree has arms and groans like a person."),
 ("It taps on every window, asking to come in.", "Personification: the rain asks to come in like a visitor."),
 ("The sun peeks out like a shy friend", "Simile: the sun is compared to a shy friend using like.")],
None, "child speaker watching a storm with a younger brother", "a small town on the Texas plains",
["What does a storm sound like to you?",
 "Model the metaphor 'The sky is a gray blanket' because it is the first image in the poem.",
 "Students explain the personification in 'Our old oak tree shakes its arms and groans.'",
 "In 'The sun peeks out like a shy friend,' what is the sun compared to?"])

save("RL-TX-4-009", "The Ice Storm Project",
'''In February, an ice storm hit our town near Waco. Ice covered every road, and the power lines sagged under the weight. On the second morning, our lights flickered and went dark.

Without power, our heater stopped working. The house grew colder every hour, and I could see my breath in the kitchen. We wore our coats inside and drank warm soup from a thermos. My plan to finish my science project on the computer was ruined, and it was due on Monday.

I had to think differently. I gathered my notes, a flashlight, and a box of colored pencils. Then I sat near the window, where the gray light was brightest. I drew my diagram of the water cycle by hand instead of printing it. It took me most of Saturday. My little sister held the flashlight when the afternoon got dark.

By Sunday night, the ice began to melt, and the power came back on. My poster was finished. On Monday, my teacher said the hand-drawn diagram was the clearest one in the class. The storm had changed my plan, but it did not stop me.''',
[("Ice covered every road, and the power lines sagged under the weight.", "The icy setting sets up the problem that comes next."),
 ("Without power, our heater stopped working.", "The setting causes a new problem in the plot."),
 ("My plan to finish my science project on the computer was ruined, and it was due on Monday.", "The storm changes the narrator's plan."),
 ("Then I sat near the window, where the gray light was brightest.", "The narrator acts because of the dark setting."),
 ("The storm had changed my plan, but it did not stop me.", "The narrator sums up how the setting shaped the story.")],
None, "fourth-grade narrator, unnamed, with a little sister", "a home near Waco, Texas, during a February ice storm",
["How can the weather change your plans?",
 "Model how 'Without power, our heater stopped working.' links the setting to the plot.",
 "Students explain how the setting changes the science project plan.",
 "Why did the narrator draw the diagram by hand?"])

save("RL-TX-5-010", "Our Town Should Plant More Shade Trees",
'''Summer in our town is hot, and last July the temperature topped 100 degrees on twelve days. Our playground has almost no shade, so recess is often moved inside. I believe our town should plant shade trees at every school.

Facts support this idea, and some of them are easy to measure. On a sunny day, the ground under a tree can be about 20 degrees cooler than bare blacktop. Trees also soak up rain, which helps stop flooding on our street. A city report says one young tree costs about $150 to plant.

Some people argue against the plan because trees need water, and our town has had dry years. That fact is true and important, and I do not want to ignore it. But many native trees, like live oaks and cedar elms, need little water once they grow roots.

Other people say the trees will take years to grow. That is also a fact, and it is a fair point. Still, a tree planted this fall will give shade to students who start kindergarten next year, and waiting will only push that day back.

The facts on both sides matter, so I tried to weigh them carefully. When I put them side by side, the reasons to plant trees are stronger. Let's ask the school board to plant ten trees this fall.''',
[("On a sunny day, the ground under a tree can be about 20 degrees cooler than bare blacktop.", "The author uses this fact for the argument: trees cool the playground."),
 ("Trees also soak up rain, which helps stop flooding on our street.", "This fact supports the argument with a second benefit."),
 ("Some people argue against the plan because trees need water, and our town has had dry years.", "This fact is used against the argument."),
 ("Other people say the trees will take years to grow.", "This is another fact used against the plan."),
 ("A city report says one young tree costs about $150 to plant.", "The author gives a cost fact so readers can judge the plan.")],
None, "fifth-grade student writer", "a hot Texas town and its school playground",
["Why do people use facts when they want to change someone's mind?",
 "Model the fact about the ground being 20 degrees cooler, since it clearly supports the argument.",
 "Students find one fact the author uses against the argument.",
 "What fact does the author give about the cost of a tree?"])
