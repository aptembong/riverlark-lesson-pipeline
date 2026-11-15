"""v2.1 sample batch, lessons 16-20 (grades 9-12): first drafts written by Claude (Opus 5.5)
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

save("RL-TX-E1-016", "Salt Grass",
'''The salt marsh behind Nana Ruth's house on the Bolivar Peninsula seemed limitless in the early morning. It was a gray-green sheet that ran all the way to the edge of the bay. Teresa had spent every summer of her childhood on that porch, shelling peas and counting pelicans as they skimmed the water in long, tidy lines. This summer felt different, because it was the first one since the hurricane had pushed six feet of water through the town.

Half the houses on her grandmother's road had vanished, and the ones that remained stood on new stilts like anxious herons. Teresa's parents wanted Nana Ruth to move inland to Houston, where the apartment had air conditioning, an elevator, and no flood insurance to worry about. They had driven down from the city to help her relocate, and Teresa had come along anticipating a final goodbye.

Nana Ruth, however, was not packing. She was on her knees in the mud beside the porch steps, pressing seedlings of salt grass into the soft ground with her bare hands. "The marsh is what saved the house," she said without looking up. "It slowed the water enough that we lost the furniture instead of the walls."

Teresa knelt beside her and took a handful of seedlings without being instructed. For the next hour, they worked in silence except for the cry of gulls and the slap of small waves against the reeds. Teresa observed how the new grass held the mud in place, and how fiddler crabs had already begun excavating tunnels between the roots. The land had been torn apart, yet it was patiently reassembling itself.

That evening, her parents laid out the apartment brochures on the kitchen table. Teresa watched her grandmother examine the glossy photographs of carpeted hallways and parking garages. Nana Ruth listened respectfully to every argument about safety and expense, because she knew they came from genuine affection. Then she folded the brochures neatly and set them aside. She said she would rather rebuild a home that the water could visit than live in one that had never known the tide.

Teresa did not know yet whether her grandmother was being courageous or merely stubborn. But as she fell asleep to the sound of the marsh breathing outside her window, she understood that some places are not just where people live. They are part of who people are, shaped by every storm they endure and every patch of ground they choose to plant again. In the morning, Teresa asked if she could stay for the rest of the summer and help.''',
[("This summer felt different, because it was the first one since the hurricane had pushed six feet of water through the town.", "The setting after the hurricane frames the story's central question about home."),
 ('"The marsh is what saved the house," she said without looking up.', "Nana Ruth sees the marsh as protection, which begins to shape the theme."),
 ("The land had been torn apart, yet it was patiently reassembling itself.", "The recovering marsh mirrors the theme of rebuilding after loss."),
 ("She said she would rather rebuild a home that the water could visit than live in one that had never known the tide.", "Nana Ruth's choice connects her identity to the coastal setting."),
 ("They are part of who people are, shaped by every storm they endure and every patch of ground they choose to plant again.", "Teresa states the theme the setting has been building toward.")],
"Teresa", "teenager visiting her grandmother after a hurricane", "the Bolivar Peninsula on the Texas Gulf Coast, the summer after a hurricane",
["Can a place become part of who you are?",
 "Model how the marsh reassembling itself mirrors the theme of rebuilding.",
 "Students explain how Nana Ruth's final choice ties her identity to the setting.",
 "Which sentence states the theme most directly?"])

save("RL-TX-E2-017", "Let Us Sleep",
'''At 7:20 in the morning, when the first bell rings at our high school, many students are physically present but mentally still asleep. Teachers in first period describe rows of slumped shoulders, half-finished breakfasts, and heads resting on desks before the lesson has even begun. Our district should move the high school start time to 8:30. That change is supported by medical research and by the experience of districts that have already made it.

The medical case is strong. The American Academy of Pediatrics recommends that middle and high schools start no earlier than 8:30. Its experts explain that the body clock shifts during adolescence, which makes it difficult for teenagers to fall asleep before eleven. Most teenagers need eight to ten hours of sleep, yet surveys consistently show that the majority of high school students get fewer than eight on school nights. Chronic sleep loss is linked to weaker concentration, lower grades, and a greater risk of car accidents among young drivers.

Opponents raise a serious concern about transportation. Our district staggers bus routes so that the same drivers can serve elementary, middle, and high schools in turn, and shifting one schedule could disrupt the others. I concede that this concern is fair, since a plan that strands younger children at dark bus stops would solve one problem by creating another. However, several districts have addressed this by flipping the order and sending elementary students first, since younger children naturally wake earlier.

A second counterargument focuses on after-school activities. Coaches worry that a later dismissal will push practices into the evening and force athletes to miss class for away games. Students who work part-time jobs to support their families have a similar worry about losing hours. These are real costs, and the district should not dismiss them, but they can be reduced through careful scheduling rather than accepted as reasons to do nothing.

The experience of other districts offers a useful rebuttal. When schools in Seattle moved their high school start times about an hour later in 2016, researchers found that students slept an average of thirty-four more minutes per night. Tardiness and absences dropped at one of the schools studied, and grades in the science classes researchers examined improved by about four and a half percent. Those results suggest that the costs opponents fear are manageable, while the benefits for students are measurable.

Changing a schedule that families have relied on for years will require patience, planning, and compromise. Still, the purpose of a school day is learning, and students cannot learn well when their bodies are fighting the clock. The district should form a committee of parents, teachers, coaches, and students to design a transition plan this year, so that the change can begin next fall.''',
[("Opponents raise a serious concern about transportation.", "The writer introduces a counterargument."),
 ("I concede that this concern is fair, since a plan that strands younger children at dark bus stops would solve one problem by creating another.", "A concession: the writer admits the other side has a valid point."),
 ("However, several districts have addressed this by flipping the order and sending elementary students first, since younger children naturally wake earlier.", "A rebuttal: the writer answers the counterargument with a solution."),
 ("A second counterargument focuses on after-school activities.", "The writer introduces a second opposing view."),
 ("These are real costs, and the district should not dismiss them, but they can be reduced through careful scheduling rather than accepted as reasons to do nothing.", "A concession followed by a rebuttal in a single sentence.")],
None, "high school student writer", "a Texas high school district",
["Should school start later? What would change for you?",
 "Model the concession in paragraph three, since 'I concede' signals it directly.",
 "Students find the rebuttal that answers the transportation concern.",
 "What evidence from Seattle does the writer use as a rebuttal?"])

save("RL-TX-E3-018", "The Ditches That Outlasted Empires",
'''In the dry country of South Texas and northern New Mexico, water has always determined where people could live and what they could grow. Centuries before modern pumps and pipelines, Spanish colonists and Indigenous communities built acequias, shallow earthen canals that carried river water across fields by gravity alone. These systems deserve far more attention than they receive, because they demonstrate that durable infrastructure depends as much on shared responsibility as on clever engineering.

The engineering itself is remarkably simple: a low dam, called a presa, raises a river just enough to send part of its flow into a main channel, the acequia madre. From the mother ditch, as it is often called, the water moves downhill through smaller ditches, and farmers open wooden gates in turn to flood their own fields. Because the entire network relies on a gentle, carefully surveyed slope, it requires no electricity and very little machinery to operate.

San Antonio offers the clearest example in Texas, where Franciscan missionaries and the Coahuiltecan people built the Espada Aqueduct between 1731 and 1745 to carry an acequia across Piedras Creek. Nearly three centuries later, the stone arches still carry water, making it one of the oldest working aqueducts in the United States. In 2015, the San Antonio Missions, including their acequias, were named a UNESCO World Heritage Site.

The technology, however, is only half of the story. In the villages of northern New Mexico, many acequias are still managed by elected officials called mayordomos, who schedule water turns, settle disputes, and organize the spring cleaning of the ditches. Every landowner who draws water is expected to send workers to that cleaning, and those who fail to contribute can lose their share. In this way, the canal becomes not merely a channel for water but a living agreement among neighbors.

This shared governance explains why acequias have lasted so long. A concrete pipe can be engineered to survive for decades, yet it will eventually crack if no one is responsible for inspecting it. An acequia, by contrast, is inspected every year by the very people whose crops depend on it, so small problems are repaired before they become disasters. The system's durability, in other words, is a social achievement as much as a physical one.

Acequias also face real threats today, as suburban development has paved over many fields and younger family members often move to cities rather than inherit the work of farming. When fewer people take part in the annual cleaning, the ditches silt up and the cooperative structure weakens. Several communities have responded by teaching students to maintain the channels and by recording the oral histories of longtime mayordomos.

In summary, acequias combine modest technology with a strong tradition of collective care. Their survival in San Antonio and New Mexico shows that the most lasting public works are often the ones that communities understand, maintain, and govern together. As Texas and the rest of the Southwest confront longer droughts and growing cities, planners would be wise to study these old ditches. They are not museum pieces but working models for managing scarce water fairly and sustainably.''',
[("These systems deserve far more attention than they receive, because they demonstrate that durable infrastructure depends as much on shared responsibility as on clever engineering.", "This is the thesis: a clear, arguable claim the essay supports."),
 ("Nearly three centuries later, the stone arches still carry water, making it one of the oldest working aqueducts in the United States.", "Strong supporting evidence from a specific Texas example."),
 ("Every landowner who draws water is expected to send workers to that cleaning, and those who fail to contribute can lose their share.", "A pertinent example of shared responsibility in practice."),
 ("The system's durability, in other words, is a social achievement as much as a physical one.", "Commentary: the writer explains what the evidence means."),
 ("In summary, acequias combine modest technology with a strong tradition of collective care.", "The summary begins the conclusion by restating the main points.")],
None, "informational essay, no protagonist", "acequias of San Antonio, Texas, and northern New Mexico",
["What makes something built by people last for centuries?",
 "Model finding the thesis at the end of the first paragraph.",
 "Students label one sentence in paragraph five as evidence or commentary.",
 "What year were the San Antonio Missions named a UNESCO World Heritage Site?"])

save("RL-TX-E3-019", "The Quotation",
'''Marisol Herrera had spent three years building the Del Mar High School debate team into a contender, recruiting freshmen in the cafeteria and coaching them through practice rounds after school. Now, the night before the state qualifying tournament, she sat at her kitchen table in Corpus Christi, rereading the evidence file her partner, Grace, had assembled for their final case. One quotation, attributed to an economist at a well-known university, made their argument almost impossible to defeat.

Marisol had tried to locate the original source so she could cite the page number, but the article Grace listed did not contain the sentence anywhere. She searched the economist's books, interviews, and lectures with growing unease, and each search confirmed what she had begun to suspect. When she finally texted Grace, the reply came almost instantly: she had paraphrased something she half remembered and put quotation marks around it because the deadline was midnight.

Marisol understood the temptation better than she wanted to admit. Grace was not lazy or dishonest by nature; she worked two evening shifts a week at her aunt's restaurant, and the team's success had become her best chance at a college scholarship. Reporting the fabricated quotation would almost certainly disqualify them both, ending Grace's season and erasing the record Marisol had worked so hard to build.

Yet Marisol also knew how the evidence would be used. Their opponents would have no way to verify the quotation in the middle of a round, and the judges would trust it because debaters were expected to be honest about their sources. Winning that way would mean that every trophy on the team's shelf, including the ones they had earned fairly, would carry a quiet doubt that only she and Grace would know about.

She considered a compromise that would spare them both. They could simply remove the quotation, rebuild the case overnight with legitimate evidence, and say nothing to their coach about what had happened. The solution was tempting precisely because it seemed responsible, but it would also teach Grace that a mistake could vanish if no one was watching. Marisol realized that the question was no longer only about the tournament; it was about what kind of teammate, and what kind of friend, she intended to be.

At six in the morning, she called Grace instead of texting, and the two of them talked until the sky over the bay turned pale. Marisol told her that she would not hide the problem, but she also would not let Grace face it alone. Together they drove to school early, sat down with Coach Alvarez before the bus left, and explained exactly what had happened and why.

The coach withdrew their final case from the tournament, and the team competed with only the arguments they could defend. They did not qualify for state that year. Months later, however, Grace rebuilt the case from scratch with verified sources. When the two of them won the spring invitational with it, Marisol understood that this victory belonged to them in a way that a win built on a false quotation never could have.''',
[("Grace was not lazy or dishonest by nature; she worked two evening shifts a week at her aunt's restaurant, and the team's success had become her best chance at a college scholarship.", "This explains Grace's motivation without excusing her choice."),
 ("Reporting the fabricated quotation would almost certainly disqualify them both, ending Grace's season and erasing the record Marisol had worked so hard to build.", "This sets out the stakes of Marisol's moral dilemma."),
 ("The solution was tempting precisely because it seemed responsible, but it would also teach Grace that a mistake could vanish if no one was watching.", "Marisol weighs a middle path and sees its hidden cost."),
 ("Marisol told her that she would not hide the problem, but she also would not let Grace face it alone.", "Her motivation, honesty and loyalty together, drives the plot forward."),
 ("They did not qualify for state that year.", "The consequence of her decision shapes the plot and the theme.")],
"Marisol Herrera", "high school debate captain who makes a hard choice herself", "Corpus Christi, Texas, the night before a state qualifying tournament",
["Is it ever right to keep a friend's mistake secret?",
 "Model how Grace's motivation is explained in paragraph three.",
 "Students explain why the compromise in paragraph five tempts Marisol and why she rejects it.",
 "What does Marisol decide to do about the fabricated quotation?"])

save("RL-TX-E4-020", "Keep the Doors Open",
'''Every city budget is a statement of values, and when money is tight, public libraries are often among the first services to lose hours, staff, and funding. Our city council is now considering a proposal to close the Eastside branch library on weekends and reduce its book budget by a third. I believe that decision would be a serious mistake, one that the council would come to regret. Libraries are not luxuries that a community can trim without consequence; they are essential infrastructure, as important to our civic life as roads, water lines, and parks.

I speak from experience, not only from principle, because this branch has been part of my life for years. For the past two years, I have volunteered at the Eastside branch every Saturday, shelving books, helping younger students with homework, and teaching older patrons how to fill out job applications online. In that time, I have learned more about my neighbors than any survey or spreadsheet could tell me. Above all, I have learned that the library quietly holds together much of the daily life of this side of town.

Consider who actually uses the branch on a typical Saturday, when the parking lot is full before the doors even open. Students line up early, because many of them do not have reliable internet at home, and the library's computers are the only place they can complete assignments that teachers increasingly post online. Parents bring toddlers to story time, retirees read the newspapers and magazines the branch subscribes to, and adults searching for work use the printers to produce resumes and cover letters.

The logical case is just as strong as the personal one, and it begins with a simple question about who pays. Closing the branch on weekends would save the city a modest sum, but the costs would simply shift to the families least able to absorb them. Those families would have to travel across town by bus to reach the central library, often with small children in tow. A student who cannot finish homework falls behind, and a job seeker who cannot submit an application stays unemployed longer. Over time, those losses cost the city far more in earnings and potential than the council could ever save by cutting hours.

There is also a moral dimension that numbers alone cannot capture, and it may matter most of all. A public library is one of the few places left where anyone may enter, stay as long as they wish, and leave with something valuable without being asked to pay. When we close its doors on the very days that working families are free to visit, we send a message about whose time and whose curiosity our city considers worth supporting.

Supporters of the proposal argue that the city faces a genuine shortfall and that every department must share the burden. That point deserves respect, and I do not pretend that the budget is easy to balance or that the council's choices are simple. However, the Eastside branch already operates with fewer staff and shorter hours than the central library. Asking it to absorb a deeper cut would place an unequal share of the burden on the neighborhood that depends on it most.

A fairer approach would spread any necessary reductions across all departments, protect weekend hours at every branch, and invite residents to propose savings before the final vote. Cities across Texas have found creative ways to support their libraries, from partnerships with local businesses to volunteer programs that extend hours without adding expense, and our city can learn from their example.

The council will hold a public hearing on the budget next Tuesday evening at City Hall, and residents are allowed to speak for three minutes each. I urge every student, parent, and neighbor who has ever borrowed a book, used a computer, or found a quiet place to think at the Eastside branch to attend. Sign up to speak, and remind our leaders that a library is not an expense to be minimized but an investment in everyone's future.''',
[("Libraries are not luxuries that a community can trim without consequence; they are essential infrastructure, as important to our civic life as roads, water lines, and parks.", "This is the arguable thesis. A reasonable person could disagree."),
 ("I speak from experience, not only from principle, because this branch has been part of my life for years.", "Ethos: the writer builds credibility through personal experience."),
 ("Closing the branch on weekends would save the city a modest sum, but the costs would simply shift to the families least able to absorb them.", "Logos: the writer reasons about who really pays."),
 ("When we close its doors on the very days that working families are free to visit, we send a message about whose time and whose curiosity our city considers worth supporting.", "Pathos: the writer appeals to the reader's sense of fairness."),
 ("Sign up to speak, and remind our leaders that a library is not an expense to be minimized but an investment in everyone's future.", "The call to action tells readers exactly what to do.")],
None, "high school senior who volunteers at the branch library", "a Texas city facing a library budget cut",
["What public place in your community would you fight to keep open?",
 "Model the ethos appeal in paragraph two, since the writer names her own experience.",
 "Students label the appeal used in the 'whose time and whose curiosity' sentence.",
 "What specific action does the writer ask readers to take?"])
