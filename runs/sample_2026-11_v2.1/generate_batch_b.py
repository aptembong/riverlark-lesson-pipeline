"""v2.1 sample batch, lessons 11-15 (grades 6-8): first drafts written by Claude (Opus 5.5)
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

save("RL-TX-6-011", "Ellie and the Dust",
'''In the spring of 1935, the wind near Dalhart, Texas, seemed to blow every single day. It carried dirt from fields that had once been green with wheat. Twelve-year-old Ellie Brandt kept damp cloths over the windows, but fine brown dust still settled on the table, the beds, and even the water bucket. Her father said the rain would come back soon, but nobody believed him anymore.

Ellie had a plan of her own. She wanted to raise chickens and sell the eggs in town, because eggs were one of the few things people still bought. But the dust made the hens sick, and two of them had already died. Every time a storm rolled in, the sky turned black at noon, and the birds panicked in their open pen. Ellie knew that if she lost the rest, her plan would be gone too.

So she studied the land around her. The old root cellar stayed cool and still, even during the worst storms. Ellie dragged wooden crates down the steps and lined them with straw. She hung a wet sheet across the doorway to catch the dust. Each time the horizon darkened, she carried the hens down one by one, even when the wind stung her face. It was hard, slow work, but the cellar kept the air clear enough for the birds to breathe.

By June, Ellie had nine healthy hens and a basket of eggs to sell each Saturday. The money was small, but it bought flour and coffee when her family needed them most. Living through the dust storms had taught her to read the sky and to plan for the worst. Years later, Ellie would say that the hard land had made her stubborn, and that stubbornness had made her strong.''',
[("fine brown dust still settled on the table, the beds, and even the water bucket", "The historical setting, the Dust Bowl, shapes Ellie's daily life."),
 ("But the dust made the hens sick, and two of them had already died.", "The setting creates the conflict in the plot."),
 ("The old root cellar stayed cool and still, even during the worst storms.", "Ellie uses the setting itself to solve her problem."),
 ("Living through the dust storms had taught her to read the sky and to plan for the worst.", "The setting changes Ellie as a character."),
 ("Years later, Ellie would say that the hard land had made her stubborn, and that stubbornness had made her strong.", "This shows the lasting effect of the setting on her character.")],
"Ellie Brandt", "twelve-year-old on a family farm who plans and acts for herself", "a farm near Dalhart, Texas, during the Dust Bowl, 1935",
["How can the place and time you live in shape who you become?",
 "Model how the dust settling on everything shows the setting shaping Ellie's daily life.",
 "Students explain how the root cellar connects the setting to Ellie's solution.",
 "What problem does the dust cause for Ellie's plan?"])

save("RL-TX-6-012", "Join the Green Team",
'''Dear sixth graders, welcome to your first year at Cedar Ridge Middle School. You have new lockers, new teachers, and a schedule that changes every hour. I remember how strange that felt last year, and right now you might be wondering where you fit in. I want to make the case that you should join the Green Team, our school's recycling club.

First, the Green Team is a simple way to meet people. We meet on Tuesdays after school, and nobody cares what elementary school you came from. Last year, half of our members were sixth graders, and many of them are now my closest friends. You do not need any special skills to join, just a willingness to show up and sort some cans.

Second, the work makes a real difference. Our school throws away about forty bags of trash every week. Last spring, the Green Team cut that number almost in half by placing blue bins in every hallway. We also collected enough cans to raise three hundred dollars, which paid for new books in the library. You will be able to see the results of your work in your own building.

Some of you might think you are too busy. Middle school does bring more homework, and many of you have sports or music, so that worry is fair. But Green Team meetings last only forty minutes, and you can come when your schedule allows. Several members also play on the volleyball team or sing in the choir.

So when you see our table at the club fair next Friday, stop by and sign up. Bring a friend from your homeroom, or come alone and leave with a new one. Your first year of middle school only happens once, and this is a good way to make it count.''',
[("Dear sixth graders, welcome to your first year at Cedar Ridge Middle School.", "The greeting names the intended audience directly: new sixth graders."),
 ("You have new lockers, new teachers, and a schedule that changes every hour.", "The writer describes things only new middle schoolers are dealing with."),
 ("We meet on Tuesdays after school, and nobody cares what elementary school you came from.", "This speaks to readers who just left elementary school."),
 ("Some of you might think you are too busy.", "The writer answers a worry this audience is likely to have."),
 ("Bring a friend from your homeroom, or come alone and leave with a new one.", "The call to action fits students, not parents or teachers.")],
None, "seventh-grade club member writing to new sixth graders", "Cedar Ridge Middle School",
["How would you write differently to a friend than to a principal?",
 "Model the greeting 'Dear sixth graders,' because it names the audience outright.",
 "Students find a detail that only makes sense for students new to middle school.",
 "Who is the intended audience of this letter?"])

save("RL-TX-7-013", "Texas's Night Shift",
'''Every summer evening near San Antonio, a dark ribbon rises out of Bracken Cave and twists into the sky. It is made of millions of Mexican free-tailed bats heading out to hunt. Many people fear bats or think of them as pests. In fact, these small mammals are among the most useful animals in Texas, because they protect crops, control insects, and even support the state's economy.

The first piece of evidence is how much bats eat. A single free-tailed bat can eat hundreds of insects in one night. The colony at Bracken Cave is thought to be the largest bat colony in the world, with more than fifteen million bats. Together, those bats can eat many tons of insects before sunrise, including moths whose young feed on corn and cotton.

That appetite matters to farmers. When bats eat the moths, fewer eggs are laid, and fewer caterpillars hatch to damage the crops. Farmers can then spray less pesticide, which saves money and keeps more chemicals out of the soil and water. Scientists who studied this effect estimated that bats save farmers in the United States billions of dollars every year. For a state that grows as much cotton as Texas does, that help is hard to replace.

Bats also bring visitors and money to Texas cities. In Austin, about one and a half million bats live under the Congress Avenue Bridge from spring to fall. Each night, crowds gather on the bridge and along the river to watch them fly out. Tour boats, restaurants, and hotels all benefit from the people who come to see the show.

Bats are not perfect neighbors, and people should never touch one, since a few carry diseases such as rabies. Still, the evidence shows that their benefits far outweigh the risks. Protecting caves and bridges where bats live is not only good for wildlife but also good for farms, towns, and families across Texas. The next time you see bats at dusk, think of them as the state's hardworking night shift.''',
[("In fact, these small mammals are among the most useful animals in Texas, because they protect crops, control insects, and even support the state's economy.", "This is the controlling idea that the rest of the text supports."),
 ("A single free-tailed bat can eat hundreds of insects in one night.", "This evidence shows how much pest control one bat provides."),
 ("Scientists who studied this effect estimated that bats save farmers in the United States billions of dollars every year.", "This evidence supports the claim that bats help the economy."),
 ("In Austin, about one and a half million bats live under the Congress Avenue Bridge from spring to fall.", "This evidence supports the point that bats draw visitors."),
 ("Still, the evidence shows that their benefits far outweigh the risks.", "The author returns to the controlling idea after admitting a risk.")],
None, "informational text, no protagonist", "Bracken Cave near San Antonio and the Congress Avenue Bridge in Austin",
["What do you think of when you hear the word bat?",
 "Model finding the controlling idea in the last sentence of the first paragraph.",
 "Students match one piece of evidence in paragraph three to the controlling idea.",
 "Which bridge in Austin is home to about one and a half million bats?"])

save("RL-TX-7-014", "Give Us Time to Eat",
'''At Lakeview Middle School, students get twenty-two minutes for lunch. That sounds like enough time until you subtract the minutes spent walking to the cafeteria and waiting in line. Most of us end up with about ten minutes to actually eat. The school should extend lunch to thirty-five minutes, and the evidence for that change comes from several directions.

The first kind of evidence is numbers, and they are hard to ignore. Our student council surveyed 412 students last month, and 81 percent said they often throw away food because they run out of time. The cafeteria staff confirmed the problem when they weighed the trash for one week. On average, they found almost sixty pounds of uneaten food every day.

The second kind of evidence comes from experts. Our school nurse, Ruth Delgado, explained that students who skip lunch often visit her office in the afternoon with headaches or stomachaches. She also pointed out that hungry students have a harder time paying attention in class. National health groups recommend that students have at least twenty minutes to eat after they sit down, which our current schedule does not allow.

Personal experience points the same way, and it is not just mine. Last year, during a week of state testing, the school tried a longer lunch for a few days. Teachers noticed that afternoon classes were calmer, and fewer students asked to go to the nurse. My friends and I could finally finish our food and still talk for a few minutes.

There are alternatives worth considering, and one is to keep lunch the same and open a second serving line so students wait less. That would help, but it would cost money for more staff, and it would not fix the long walk from the far wing. Another idea is to let students eat in class, but teachers worry about spills and lost teaching time. A longer lunch solves the problem more directly than either option.

Adding thirteen minutes would mean shortening each class by about two minutes. That is a small trade for students who are fed, focused, and ready to learn. The numbers, the experts, and our own experience all lead to the same conclusion.''',
[("Our student council surveyed 412 students last month, and 81 percent said they often throw away food because they run out of time.", "Statistical evidence: survey numbers support the argument."),
 ("Our school nurse, Ruth Delgado, explained that students who skip lunch often visit her office in the afternoon with headaches or stomachaches.", "Expert evidence: a school nurse speaks from experience."),
 ("Teachers noticed that afternoon classes were calmer, and fewer students asked to go to the nurse.", "Observational evidence from a past trial of a longer lunch."),
 ("There are alternatives worth considering, and one is to keep lunch the same and open a second serving line so students wait less.", "The author considers an alternative to the proposal."),
 ("Another idea is to let students eat in class, but teachers worry about spills and lost teaching time.", "The author considers a second alternative and explains its weakness.")],
None, "seventh-grade student writer", "Lakeview Middle School",
["Is your lunch period long enough? How do you know?",
 "Model the survey sentence as statistical evidence, since numbers are the easiest type to spot.",
 "Students identify the type of evidence in the school nurse sentence.",
 "Name one alternative the author considers and the reason the author rejects it."])

save("RL-TX-8-015", "Fixed Fast",
'''The gym at Harlingen High smelled like floor wax and nervous sweat as Jalen set his team's robot on the practice table. In twenty minutes, the Rio Valley Regional finals would begin, and the robot would have to stack six blocks in under a minute. Jalen ran his thumb along the arm one last time and felt a wire shift slightly under the tape. He told himself it was nothing, but the tiny wobble stayed in the back of his mind.

Three years earlier, Jalen had sat on an overturned bucket in his grandfather's garage, watching him repair a broken radio. The workbench was covered with screws, solder, and parts from machines that no longer worked. "Anything you build will fail sometime," his grandfather said, tapping the radio's case with a screwdriver. "What matters is whether you know it well enough to fix it fast," he added. Jalen had been eleven and more interested in the snacks on the shelf, but he had remembered every word.

Back in the gym, the announcer called Team 14 to the arena. Jalen and his partner, Priya, carried the robot to the starting square while the crowd clapped from the bleachers. When the buzzer sounded, the robot rolled forward smoothly and lifted the first block, then the second and the third. On the fourth block, the arm jerked sideways and froze in midair, exactly where the loose wire was hidden.

The rules allowed one thirty-second repair, and Priya looked at Jalen with wide eyes. He did not panic, because he had built that arm himself and knew every connection inside it. In a few quick moves he peeled back the tape, pressed the wire firmly into its socket, and wrapped it again. The arm twitched, rose, and set the fourth block in place with twenty seconds left on the clock.

They finished with five blocks instead of six, which was enough for second place. On the bus ride home, Jalen texted his grandfather a photo of the silver medal. The reply came back a minute later, just two words long, but Jalen grinned at it the whole way down the highway: "Fixed fast."''',
[("Jalen ran his thumb along the arm one last time and felt a wire shift slightly under the tape.", "Foreshadowing: this hints at the problem that comes later."),
 ("He told himself it was nothing, but the tiny wobble stayed in the back of his mind.", "Foreshadowing: the author signals that the wire will matter."),
 ("Three years earlier, Jalen had sat on an overturned bucket in his grandfather's garage, watching him repair a broken radio.", "Flashback: the story jumps back in time."),
 ('"Anything you build will fail sometime," his grandfather said, tapping the radio\'s case with a screwdriver.', "The flashback gives advice that foreshadows how Jalen will act."),
 ("Back in the gym, the announcer called Team 14 to the arena.", "This returns the plot from the flashback to the present.")],
"Jalen", "eighth-grade robotics team member", "a regional robotics competition in Harlingen, Texas, and his grandfather's garage",
["Why might an author tell part of a story out of order?",
 "Model the foreshadowing in the loose-wire sentence, since it is the first hint of trouble.",
 "Students find where the flashback begins and where it ends.",
 "What words signal that the story is jumping back in time?"])
