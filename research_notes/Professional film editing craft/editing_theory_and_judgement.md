# Theory and Grammar of Professional Film/Video Editing, and How Editors Judge Their Cut

Scope note: Sources are a mix of primary texts quoted second-hand (Murch, Dmytryk, Eisenstein), one peer-reviewed perception study (Hecht & Kalkofen 2009), editor interviews (Frame.io Art of the Cut, No Film School), and practitioner/education guides. Where a claim came only via a search-engine summary and was not fetched directly, it is marked "(search summary)". Many classic books (Grammar of the Edit, Reisz & Millar, Dancyger, O'Steen) could not be read directly in this session; see Gaps.

---

## 1. Walter Murch's Rule of Six, blinks, and choosing a cut point

### Takeaway
Murch ranks six criteria for a cut, weighted Emotion 51%, Story 23%, Rhythm 10%, Eye-trace 7%, 2D plane 5%, 3D space 4%. The ideal cut meets all six. When it can't, give up criteria from the bottom of the list first, because a cut that is emotionally right hides errors further down. He treats a cut as a "blink" that ends one thought and starts the next. He finds cut points by feel, in real time. A cut point is "true" if he lands on the same frame on repeated passes.

### Cited Findings
- **The ideal:** "The ideal cut is one that satisfies all the following six criteria at once." The order is emotion, story, rhythm, eye trace, 2D plane of screen, 3D space. — [No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch)
- **Priority chain:** "If you have to give up something, don't ever give up emotion before story… don't give up planarity before spatial continuity." Emotion is the criterion to "try to preserve at all costs." — [No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch)
- **Weights:** Emotion 51%, Story 23%, Rhythm 10%, Eye-trace 7%, 2D plane of screen 5%, 3D space of action 4%. Emotion alone is worth more than the other five together. — [UT Austin RTF318 wiki](https://cloud.wikis.utexas.edu/wiki/spaces/rtf318/pages/80022510/Murch+s+Rule+of+Six); [No Film School](https://nofilmschool.com/2016/11/6-rules-good-cutting-according-oscar-winning-editor-walter-murch) (51% figure)
- **Meaning of each criterion** (search summary of the [UT Austin wiki](https://cloud.wikis.utexas.edu/wiki/spaces/rtf318/pages/80022510/Murch+s+Rule+of+Six) and [FilmDaft](https://filmdaft.com/walter-murchs-rule-of-six-the-editors-formula-for-choosing-the-right-cut/)):
  - **Emotion:** the cut is true to the feeling of the moment.
  - **Story:** the cut moves the story forward.
  - **Rhythm:** the cut lands at a moment that is "rhythmically interesting and right."
  - **Eye-trace:** "the location and movement of the audience's focus of interest within the frame."
  - **2D plane of screen:** screen direction and 180°-line grammar ("planarity").
  - **3D space of action:** physical continuity of people and objects in the real space, e.g. matching action and positions.
- **Masking:** "Each item in general will help obscure problems with items lower on the list, but not vice versa." If the emotion is right, it covers other weaknesses. — (search summary) [FilmDaft](https://filmdaft.com/walter-murchs-rule-of-six-the-editors-formula-for-choosing-the-right-cut/); [UT Austin wiki](https://cloud.wikis.utexas.edu/wiki/spaces/rtf318/pages/80022510/Murch+s+Rule+of+Six)
- **Blink theory:** "a shot presents us with an idea, or a sequence of ideas, and the cut is a 'blink' that separates and punctuates those ideas." Murch saw it while editing *The Conversation*, when his cuts kept matching Gene Hackman's blinks. A listener blinks at the moment they "get" an idea. — [Musicbed](https://www.musicbed.com/articles/?p=937)
- **What a cut means:** when you decide to cut, you are saying you will end this idea and start something new. — (search summary) [Musicbed](https://www.musicbed.com/articles/?p=937)
- **Rhythm and trust:** the editor's job is to "establish an interesting, coherent rhythm of emotion and thought." "A poorly edited film will cause the audience to hold back." — [Musicbed](https://www.musicbed.com/articles/?p=937)
- **Finding the frame:** Murch cuts in real time and "never goes frame by frame." Play the clip, stop where the cut feels right, and note the timecode. Rewind and repeat. Landing on the same frame three times means you have it. If you land on different frames, you haven't found the scene's rhythm yet. — [No Film School](https://nofilmschool.com/2016/03/intriguing-editing-tips-oscar-winning-editor-walter-murch); [Musicbed](https://www.musicbed.com/articles/?p=937)
- **Walking shots ("step, step, cut"):** give the subject two steps and cut on the uplift of the third. Cut on the third footfall itself if you want the cut to be noticed. — [No Film School](https://nofilmschool.com/2016/03/intriguing-editing-tips-oscar-winning-editor-walter-murch)
- **Cutting silent:** Murch cuts and refines picture with the sound off. When sound goes back on, about 70% "will be fine," about 10% needs fixing, and about 15% turns out interesting by happy accident. — [No Film School](https://nofilmschool.com/2016/03/intriguing-editing-tips-oscar-winning-editor-walter-murch)
- **Standing:** Murch stands about half the time he edits. He says it gives a better sense of time: "Cooking, surgery, conducting — you have to *feel* time." — [No Film School](https://nofilmschool.com/2016/03/intriguing-editing-tips-oscar-winning-editor-walter-murch); [Ondaatje/Murch](https://www.webdelsol.com/SolPix/sp-murch.htm) (search summary)
- **Guiding attention:** Murch describes the editor's job as gently prodding the audience's attention toward parts of the frame. — (search summary) [NPR](https://www.npr.org/transcripts/4994411)
- **Cut rates:** "A convincing action sequence might have around twenty-five cuts a minute." "A dialogue scene would still feel 'normal' (in an American film) averaging six cuts per minute." It is unclear whether these figures are Murch's own words. — [Musicbed](https://www.musicbed.com/articles/?p=937)
- **Blink research:** the same article cites a Japanese study on synchronized audience blinking, and Radiolab's figure that viewers lose about 6 seconds of vision per minute to blinks. The article's "70 others blink along" figure is garbled and should not be relied on. — [Musicbed](https://www.musicbed.com/articles/?p=937)

### Inferences
- **Scoring heuristic for an AI agent.** Score each candidate cut frame on all six criteria and weight them 51/23/10/7/5/4. Never accept a gain in a lower criterion (e.g., perfect action match) that costs emotion or story. In practice this means the agent may break the 180° rule or a continuity match if the more emotionally truthful take or moment requires it.
- **Operational "blink point."** Cut when a thought completes:
  - after a line's meaning lands;
  - when a speaker or listener blinks, looks away, or shifts expression;
  - when an action resolves.
  Do not cut mid-thought. A detectable eye blink in the outgoing shot, at or just after the end of a line, is a strong candidate cut point. Cut on it or just before it.
- **Stability test.** For a machine, the "same frame three times" check can be imitated by re-evaluating a cut point with slightly perturbed context (different pre-roll) and requiring a stable result.
- **Two-pass workflow.** Cut picture first with audio muted or ignored, judging from faces and eyes. Then do a second pass with sound to catch the roughly 10% of cuts that sound breaks.

### Gaps
- Murch's exact book wording for each criterion, and the full blink chapter, could not be fetched. Quotes are second-hand.
- The following Murch ideas are known from *In the Blink of an Eye* but were **not verified** in this session:
  - writing down your reactions on first viewing of dailies because "the first time" reaction is closest to the audience's;
  - the "little paper people" at the screen edge to remember the projected scale;
  - shooting-ratio figures for *Apocalypse Now*.
- No numbers were found on how many frames before or after a blink to cut.

---

## 2. Continuity editing grammar: 180°, 30°, eyeline, match on action, screen direction, shot-reverse-shot, coverage, inserts, cutaways, B-roll

### Takeaway
Continuity editing hides the cut by keeping the axis of action (180°), changing angle enough between consecutive shots of the same subject (at least 30°), matching eyelines and screen direction, and cutting while the subject is moving. The common practitioner rule for match on action is to overlap the action by 2–5 frames. One controlled perception study contradicts this. Viewers preferred a small gap (about 4 frames at 24 fps dropped). The gap was larger, up to about 350 ms, when cutting close→wide, and smaller or even an overlap when cutting wide→close.

### Cited Findings
- **180° rule:** keep the camera on one side of an imaginary axis between characters. Crossing it ("jumping the line") confuses the audience. Its practical payoff is consistent screen direction: a figure moving left-to-right keeps doing so, and eyelines stay believable. — (search summary) [FilmDaft](https://filmdaft.com/understanding-the-180-degree-rule-in-media/); [Wolfcrow](https://wolfcrow.com/the-15-essential-rules-of-film-continuity/)
- **Crossing the line legitimately:** introduce a neutral (on-axis) shot, a cutaway, B-roll, an insert, a new character or motion vector, or a shot where the camera moves across the line on screen. If the edit already has a violation, use a different shot that respects the line. — (search summary) [Indiana Univ. C229 lecture](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx)
- **30° rule:** move the camera at least 30° between consecutive shots of the same subject. Smaller changes make the subject appear to leap: a jump cut. — (search summary) [Wolfcrow](https://wolfcrow.com/the-15-essential-rules-of-film-continuity/); [IU lecture](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx)
- **Eyeline match:** a shot of a character looking, then a shot of what they see. It depends on the 180° rule, because the glance must point the right way. — (search summary) [IU lecture](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx)
- **Cut in movement:** "Whenever possible, cut 'in movement'" (Dmytryk 1984, p. 27). Dmytryk also argued that a change in image size is not required for a smooth cut. — [Hecht & Kalkofen 2009](https://experimental.psychologie.uni-mainz.de/files/2024/06/2009hecht-kalkofen.pdf)
- **Overlap rules in the literature:**
  - Dmytryk: overlap the action by 3–5 frames (125–208 ms at 24 fps).
  - Anderson (1996): overlap by about 2 frames (about 83 ms). This is one of his "four rules of continuity editing."
  - Reisz & Millar (1968): the moving object must be in the exact same world position immediately before and after the cut. Leaving out or repeating movement gives "an impression of jumpiness."
  - Mehnert (1963): a mid-action cut must be physically discontinuous, with a gap, to look continuous.
  - Levin & Simons (2000): viewers are so insensitive that gap vs overlap doesn't matter.
  — [Hecht & Kalkofen 2009](https://experimental.psychologie.uni-mainz.de/files/2024/06/2009hecht-kalkofen.pdf)
- **Madsen (1973):**
  - Wide→close ("contraction"): delete several frames at the head of the incoming shot.
  - Close→wide ("enlargement"): overlap several frames.
  — [Hecht & Kalkofen 2009](https://experimental.psychologie.uni-mainz.de/files/2024/06/2009hecht-kalkofen.pdf)
- **Experiment 1 (camera-angle changes 10°–130°):**
  - Observers preferred a gap, not an overlap: a mean of 182 ms.
  - Expressed in frames: "a temporal gap equivalent to leaving 4 frames on the cutting floor of a movie presented at 24 frames per second."
  - The preferred gap was the same whether the angle changed by 10° or 130°.
  - Tolerance for mismatch was very high (SD ≈ 797 ms).
  — [Hecht & Kalkofen 2009](https://experimental.psychologie.uni-mainz.de/files/2024/06/2009hecht-kalkofen.pdf)
- **Experiment 2 (shot-size changes):**
  - Enlargement (close→wide) gave the largest preferred gaps, up to about 350 ms (≈8 frames at 24 fps).
  - Contraction (wide→close) gave smaller gaps, and for large contractions, an overlap.
  - Most practising cutters and camera operators interviewed at IWF Göttingen also said that "a smooth transition can be achieved by dropping a few frames (ellipsis)."
  — [Hecht & Kalkofen 2009](https://experimental.psychologie.uni-mainz.de/files/2024/06/2009hecht-kalkofen.pdf)
- **Jump cut:** a cut between two shots of the same subject from nearly the same position. The subject seems to jump. It is a continuity violation, but useful to show time passing. — (search summary) [IU lecture](https://jkmedia.sitehost.iu.edu/C229/Lecture9_sp25.docx); [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques)
- **Cutting on action:** switching shots while the subject is still moving keeps the flow seamless. — (search summary) [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques)
- **Holding vs covering:** Joe Walker (*Dune*) lets moments play in long holds rather than interrupting them with reaction shots, e.g. a 17-second desert plate and a long pause before Stilgar spits. He wants almost every shot narratively driven, not a "beauty shot." — [Frame.io, Art of the Cut: Dune](https://blog.frame.io/2021/10/27/art-of-the-cut-dune-joe-walker/)
- **Building a scene backward:** Walker finds the close-up that delivers the scene's key emotional beat, then builds the surrounding shots toward it: "I sort of cut backward sometimes." — [Frame.io](https://blog.frame.io/2021/10/27/art-of-the-cut-dune-joe-walker/)

### Inferences
- **Default match-on-action recipe for the agent:**
  1. Find the frame where the action is mid-motion and most visible in both shots, e.g. a hand halfway to the door, or a body halfway through sitting. That is the "straight match."
  2. Then try trimming 2–4 frames off the head of the incoming shot (a gap). This follows both the empirical study and Murch's "cut on the uplift."
  3. Close→wide: lean toward a larger gap, 4–8 frames at 24 fps.
  4. Wide→close: use a straight match or a 0–2 frame overlap.
  5. Only use the classic 2–5 frame overlap when the incoming shot reads as a "stutter" at the straight match.
  Because tolerance is high, story, emotion, and eye-trace should decide close calls, not frame-exact matching.
- **Eye-trace at the cut:** place the subject of interest in the incoming shot near where the viewer's eye was at the end of the outgoing shot. The viewer then doesn't have to search, so the cut feels invisible. This is Murch's eye-trace criterion applied to the frame.
- **Coverage pattern.** Standard narrative coverage runs master/wide → medium → over-the-shoulder/singles → close-ups → inserts.
  - Typical scene grammar: establish geography early with a wide; move closer as emotional intensity rises; save the tightest close-up for the key beat (per Walker); go back to wide to release tension or show a geography change.
  - This is a standard convention. No directly fetched source quantified it.
- **Shot-reverse-shot.** Alternating over-the-shoulder shots or singles of two speakers, on the same side of the 180° line, with matched shot sizes for equal-status characters.
  - Asymmetric sizes (tighter on one character) signal whose scene it is.
  - The reaction shot is often more important than the speaker's shot (inference consistent with Kuleshov, section 3).
- **Inserts and cutaways.** Inserts are close detail of something in the scene's space. Cutaways show something outside the main action. Use both to:
  - compress time;
  - hide a jump in a continuous interview;
  - bridge a continuity error;
  - legitimately cross the 180° line (per the IU lecture).
- **B-roll in documentary.** Its main structural job is covering edits inside interview soundbites (see section 5 sources on documentary).
- **Differences by format:**
  - **Narrative:** strict continuity is the default.
  - **Documentary and interviews:** jump cuts within one talking head are commonly covered with B-roll or a cutaway, or softened with a short dissolve (see section 4).
  - **Short-form social:** jump cuts on a talking head are accepted grammar, used for energy and to remove dead air (see section 3).

### Gaps
- No primary-source numbers were found for how long an establishing shot should be held, or for typical coverage proportions.
- *Grammar of the Edit*'s specific continuity guidance could not be fetched. Its O'Reilly and university-hosted copies require authentication.
- The Hecht & Kalkofen study used computer-animated objects, not human actors. Real-footage cues such as motion blur and facial expression may shift the preferred gap.

---

## 3. Cut types and montage theory: J/L cuts, match cuts, jump cuts, smash cuts, cross-cutting, Eisenstein's five methods, Kuleshov effect, invisible vs expressive editing

### Takeaway
Most cut types fall into two families:
- **Invisible (continuity) cuts:** J/L cuts and match on action. They hide the edit.
- **Expressive cuts:** smash cuts, jump cuts, graphic match cuts, intellectual montage. They make the audience feel the cut, or build meaning out of collision.

The Kuleshov effect, replicated with fMRI and in a 2016 study, is why reaction shots and juxtaposition carry meaning. Eisenstein's five montage methods go from purely mechanical to purely conceptual:
- **Metric:** cut by frame count.
- **Rhythmic:** cut by movement inside the shot.
- **Tonal:** cut by mood (light, shape, sound).
- **Overtonal:** all three combined.
- **Intellectual:** an idea produced by colliding images.

### Cited Findings
- **J-cut:** the next shot's audio starts before its picture. The audience hears it before seeing it. The name comes from the J shape on the timeline. — (search summary) [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques); [Envato Tuts+](https://photography.tutsplus.com/articles/types-of-cuts-in-film-video--cms-108596)
- **L-cut:** the previous shot's audio carries over the next picture. It is often used for emotional effect, e.g. a line of dialogue echoing over the next scene. — (search summary) [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques); [Envato Tuts+](https://photography.tutsplus.com/articles/types-of-cuts-in-film-video--cms-108596)
- **Match cut:** links two shots through similar shape, colour, or movement, often across a jump in scene or time. Canonical example: the bone-to-spacecraft cut in *2001: A Space Odyssey*. Technically it is a hard cut; the matched content is what makes it a match cut. — (search summary) [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques); [Filmsupply](https://wpengine.fm.co/filmsupply/?p=3626)
- **Smash cut:** an abrupt cut between unrelated or contrasting shots. It is used for drama, comedy (deflation), and horror jump scares. — (search summary) [Envato Tuts+](https://photography.tutsplus.com/articles/types-of-cuts-in-film-video--cms-108596)
- **Cross-cutting:** alternating between locations so the actions seem simultaneous. — (search summary) [Storyblocks](https://www.storyblocks.com/resources/tutorials/film-editing-techniques)
- **Kuleshov effect, the original experiment:** the same neutral close-up of actor Ivan Mozzhukhin was cut with a bowl of soup, a girl in a coffin, and a woman on a divan. Audiences read hunger, grief, and desire, though the face was identical. Kuleshov argued that montage is the basis of cinema. The date (1910s–20s) is uncertain, and no footage survives. — [Wikipedia: Kuleshov effect](https://en.wikipedia.org/wiki/Kuleshov_effect)
- **Kuleshov replications:**
  - Prince & Hensley (1992) failed to replicate: 137 participants, single-trial, between-subjects.
  - Mobbs et al. (2006, fMRI) found the effect for negative, positive, and neutral valence.
  - Barratt et al. (2016) supported it: 36 participants, 24 sequences.
  - Baranowski & Hecht (2017) showed music alone can shift how a face is read.
  — [Wikipedia: Kuleshov effect](https://en.wikipedia.org/wiki/Kuleshov_effect)
- **Hitchcock's illustration:** his squinting face cut with a woman and baby reads as a kind old man. The same face cut with a woman in a bikini reads as a "dirty old man." — [Wikipedia: Kuleshov effect](https://en.wikipedia.org/wiki/Kuleshov_effect)
- **Eisenstein's five methods:** — [StudioBinder](https://www.studiobinder.com/blog/soviet-montage-theory/); [PremiumBeat](https://www.premiumbeat.com/blog/soviet-montage-theory-types); [Media-Studies.com](https://media-studies.com/eisenstein-montage/) (search summary)
  - **Metric:** shots cut to fixed lengths in frames, like a musical measure, regardless of content.
  - **Rhythmic:** shot length departs from the metric formula and follows movement within the shot.
  - **Tonal:** cut for mood and atmosphere: changes in light, shallow vs deep focus, sound, contrasting shapes.
  - **Overtonal:** combines metric, rhythmic, and tonal for a deeper response. Eisenstein called it the furthest development of the line.
  - **Intellectual:** juxtaposes images that aren't overtly related to trigger an abstract idea. It rests on collision or conflict (thesis/antithesis).
- **Primary source:** Eisenstein's own wording is in his 1929 essay "Methods of Montage." — (search summary) [Media-Studies.com](https://media-studies.com/eisenstein-montage/)
- **Jump cuts in short-form:** a well-timed jump cut adds energy, but too many feel choppy. Editors remove dead air, especially in the opening seconds. — (search summary) [Virlo](https://virlo.ai/blog/how-do-influencers-edit-their-videos); [SocialKit](https://socialk.it/en/blog/short-form-video-strategy)

### Inferences
- **Choosing invisible vs expressive.** Default to invisible for narrative dialogue and documentary interview. Choose expressive when the brief calls for energy, comedy, shock, or a thematic point. An expressive cut should be deliberate, motivated, and rare enough to keep its impact.
- **J/L cuts are the main tool for natural dialogue.** In real conversation we hear a reply before we turn to look, and we keep watching a speaker after they finish.
  - **L-cut:** stay on the speaker, or cut to the listener, as a line finishes. Showing the listener's reaction is the Kuleshov principle.
  - **J-cut:** bring in the next scene's sound to pull the viewer forward across a scene change.
  - No fetched source gives standard offsets. A common practitioner starting point is a few frames to about 1 s of split, adjusted by eye. Treat this as unverified.
- **Kuleshov for the agent:** the meaning of a reaction shot depends on what precedes it. A neutral reaction can be "steered" by the preceding shot and by music (per Baranowski & Hecht 2017). So reaction-shot selection should be judged in sequence, never in isolation.
- **Match-cut subtypes** (definitions consistent with the sources above):
  - **Graphic match:** shape, colour, or composition.
  - **Action match:** movement continues across the cut.
  - **Sound match:** a similar sound bridges two scenes, e.g. a scream into a train whistle.
  Look for these at scene transitions. They justify a hard cut where a dissolve would otherwise be used.
- **Montage sequences in practice:**
  - **Metric/rhythmic:** cut to the music's beat or bar (metric), or to movement inside each shot (rhythmic).
  - **Tonal:** sequence shots by brightness, colour, or energy curve.
  - **Intellectual:** juxtapose to make an argument. Common in documentary and commercials.

### Gaps
- No authoritative frame counts were found for J/L-cut offsets.
- No StudioBinder, Grammar of the Edit, or Dancyger text on these cut types was fetched directly. The definitions come from secondary guides via search summaries.
- Eisenstein's original essay was not fetched.

---

## 4. Transitions: cut vs dissolve vs fade/dip to black or white vs wipe; meaning and duration

### Takeaway
The cut is the default and most common transition. Every other transition carries meaning:
- **Dissolve:** time passing, a change of location, or a flashback. Typically 1–2 s (24–48 frames). A 6–12-frame dissolve is a "soft cut" to smooth a jump cut.
- **Fade to/from black:** closure, the end of a scene, act, or film, or a long time gap.
- **Fade to white:** memory, transcendence, or ambiguity.
- **Wipe:** a stylised, visible transition. Little authoritative guidance was found on it.

### Cited Findings
- **Grammar of the Edit's four transitions:** cut, dissolve, wipe, and fade. Audiences have expectations about their traditional use, and "each transition carries with it its own meaning." The cut is the most common. — (search summary) [Grammar of the Edit, O'Reilly ch.4](https://oreilly.com/library/view/grammar-of-the/9780240521206/06_Chapter4.html)
- **Typical length:** "Fades and dissolves typically have a duration of 1 to 2 seconds (24–48 frames)." — [Wikipedia: Dissolve](https://en.wikipedia.org/wiki/Dissolve_(filmmaking))
- **Short dissolves:** "Short dissolves (6–12 frames) may be used to soften obvious hard cuts which may startle the viewer, or jump cuts." — [Wikipedia: Dissolve](https://en.wikipedia.org/wiki/Dissolve_(filmmaking))
- **Meaning of a dissolve:** "Generally, but not always, the use of a dissolve is held to indicate that a time has passed between the two scenes." It may also signal a change of location or the start of a flashback. — [Wikipedia: Dissolve](https://en.wikipedia.org/wiki/Dissolve_(filmmaking))
- **Fade to black, when:** it "is commonly used to mark the end of a scene, sequence, act, or entire film" and "is most effective when reserved for moments that truly warrant emphasis."
  - It suggests "closure, finality, or separation" and "does not imply overlap or continuation," unlike a dissolve.
  - "The duration of the fade affects its impact… a longer fade can feel deliberate, emotional, or reflective."
  — [HowToFilmSchool](https://howtofilmschool.com/dictionary/fade-to-black/)
- **Fade to white:** "often suggests memory, transcendence, or ambiguity." — [HowToFilmSchool](https://howtofilmschool.com/dictionary/fade-to-black/)
- **Institutional house style (Boston University video standards):**
  - Fades of 2 or 8 frames at 24 fps (3 or 10 frames at 30 fps).
  - 12 or 18 frames at 24 fps (15 or 20 at 30 fps) for slower-paced edits.
  - Deviate only if the dissolve looks "sticky."
  - A hard cut to black is acceptable when appropriate.
  - Deliverables need 2 s of black at head and tail.
  — (search summary) [BU video branding standards](https://www.bu.edu/brand/files/2019/06/bu-video-branding-standards.pdf)
- **Dissolve vs fade-out/fade-in pair:** a dissolve blends directly, implying continuity. A fade to black then from black marks a longer passage of time, while dissolves traditionally signal smaller changes. — (search summary) [Imagineer/Boris FX blog](https://borisfx.com/blog/how-does-a-dissolve-differ-from-a-fade-transition/)

### Inferences
- **Transition decision table for the agent:**

  | Situation | Transition |
  |---|---|
  | Same scene, continuous time | Hard cut (always) |
  | New scene, implied continuity of time or energy | Hard cut, J/L cut, or match cut. Modern narrative and social video rarely use dissolves for ordinary scene changes. |
  | Time passing or change of place, contemplative tone | Dissolve, 24–48 frames |
  | Montage of moments in a reflective sequence | Dissolves of about 12–36 frames, or hard cuts on the beat |
  | Jump cut inside an interview or talking head | Cover with B-roll or cutaway, or a 4–12-frame "soft cut" dissolve (doc and corporate). Leave as a hard jump cut in social video or vlogs. |
  | End of an act or film, or a major tonal reset | Fade to black. Use about 1–2 s as a starting point; longer is more reflective. Optionally hold black, then fade up. |
  | Quick functional "dip" between segments | Dip to black of about 8–12 frames at 24 fps. Inference from BU's 8-frame and Wikipedia's 6–12-frame figures. |
  | Memory, dream, or transcendence | Fade or dip to white |
  | Wipe | Reserve for deliberate stylisation (genre homage, playful tone, sports or TV graphics). Avoid in serious drama unless the style is established. |

- **Restraint:** overuse dilutes meaning. A fade to black should be rare, about one per major structural break. Avoid NLE "fancy" transitions (page peels, 3D spins) unless the brief explicitly asks for them.
- **Frame rates:** at 25 fps (PAL) or 30/29.97 fps, scale frame counts in proportion. 1 s is 25 or 30 frames.

### Gaps
- No authoritative source was found giving durations for wipes or dips to white.
- No source was found giving a quantitative rule on dissolve frequency in modern film.
- Grammar of the Edit's detailed when-to-use guidance for each transition was not accessible.

---

## 5. How editors evaluate a cut and handle feedback

### Takeaway
Editors regain objectivity by stepping away (a day off, weekends) and watching the whole cut straight through without stopping. They change the viewing conditions (sound off; Walker flips the image and goes black-and-white late in the process). They screen early to small mixed audiences, about 4–10 people, and act on notes that repeat or confirm their own suspicions. A note is a symptom: treat the problem it names as real and the fix it proposes as optional. Cutting is mostly subtraction. Shave everything before removing scenes, but be willing to lose loved material.

### Cited Findings
- **When to screen:** perspective typically goes about 3–5 weeks into an edit, so bring in fresh eyes then. — [Frame.io: Test Screening Tips](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Self-review protocol:**
  - Take a day off, then watch the whole cut without pausing, re-cutting, or taking notes.
  - Level the sound so cuts are smooth and dialogue is audible: "Bad sound is so distracting that it often can ruin a regular screening."
  - Add slates for missing graphics, scenes, or temp music.
  — [Frame.io](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Audience:**
  - 4–10 people is enough, with no theatre needed.
  - Diversify the group, but weight it toward the target demographic. If they don't like the cut, "you've got a serious problem."
  - Limit industry people, who nitpick minor issues.
  — [Frame.io](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Questions:**
  - A written questionnaire before the screening: Did you like the main character? Was the conflict clear? Where were you lost or confused, and why?
  - Ask questions about specific scenes or performances only afterward, so you don't steer opinions.
  — [Frame.io](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Interpreting feedback words:**
  - "Bored" can mean pacing, or missing stakes or motivation. Viewers who care about the characters will tolerate slow moments.
  - "Confused" means the story or performances aren't conveying stakes. Trace each plot thread and revisit takes.
  - "It didn't hook me" usually means a weak first act.
  — [Frame.io](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Acting on notes:**
  - Take a note seriously if it confirms a scene you already worried about.
  - When several people raise the same issue, treat it as real, "even if their proposed fix is wrong."
  - Check your ego and be willing to cut loved scenes, jokes, or characters. The author compares the film to a bonsai tree that gets healthier with pruning.
  — [Frame.io](https://blog.frame.io/2017/07/06/successful-test-screening-tips/)
- **Joe Walker's objectivity tricks:**
  - He values weekends and stepping away.
  - Late in the process he flips the image and makes it black-and-white so the footage feels newly seen. Doing this too early "blow[s] it."
  - He keeps an imaginary audience in mind and asks what they are wondering and whether the film has answered it.
  - He reviews scenes with the sound off, so faces and eyes drive the cut.
  — [Frame.io, Art of the Cut: Dune](https://blog.frame.io/2021/10/27/art-of-the-cut-dune-joe-walker/)
- **Walker on versions and iteration:**
  - He builds "detail by detail" with temp sound and visual placeholders.
  - He avoids heavy music in early passes.
  - *Dune* reached at least a "25th fine cut," with bin comments updated at every change.
  - Scenes that already work are left alone. One knife fight stayed frame-accurate to a cut made two days after the shoot.
  — [Frame.io](https://blog.frame.io/2021/10/27/art-of-the-cut-dune-joe-walker/)
- **Walker on what to cut:** "you could easily find low-hanging fruit to cut if you wanted to shorten the film, but you would have lost a lot." He protects world-building texture while requiring shots to be narratively driven. — [Frame.io](https://blog.frame.io/2021/10/27/art-of-the-cut-dune-joe-walker/)
- **Thelma Schoonmaker on *The Wolf of Wall Street*:** the cut ran about four hours. Rather than removing whole scenes, which would have been "devastating," they "shaved things down" over three or four screenings to reach the target length. A two-part release was considered and rejected because the film "needs a certain arc." — (search summary) [The Playlist](https://theplaylist.net/thelma-schoonmaker-says-2-part-4-hour-wolf-of-wall-street-was-considered-plus-watch-1-hour-charlie-rose-talk-20131223/)
- **How notes arrive:** in person in the suite, by video call, at screenings, as timecoded written comments, or by email. Notes can be vague, political, contradictory, or clueless. Typical example: "a scene is dragging and needs to be shorter." — [HowToFilmSchool: Notes Session](https://howtofilmschool.com/dictionary/notes-session/)
- **Who notes are for:** notes are addressed to the director but are ultimately for the editor, who implements whatever is workable. Writer screenings often come too late for notes to be incorporated. — (search summary) [John August](https://johnaugust.com/qanda/directors/page/22)
- **Note overload:** practitioners warn that a long laundry list of notes can make an editor stop thinking critically. — (search summary, informal forum opinion) [Creative COW](https://creativecow.net/forums/thread/the-part-of-post-production-i-think-ai-actually-helps/)
- **Giving notes:** start with what worked, so it is kept, then ask why the creator made particular decisions. — (search summary) [Digital Promise feedback guide](https://digitalpromise.org/wp-content/uploads/2020/11/360productionguide-feedbackonroughcut.pdf)
- **Documentary workflow:**
  - Transcribe with timecode at each "thought" or paragraph.
  - Over-select soundbites.
  - Build a paper edit (printed strips or index cards arranged into beginning, middle, and end; or a text document or tool), which reveals gaps and over-length.
  - Make the assembly fast without finessing.
  - Tighten by asking, "How many sentences or words can I take out, and still tell the same story?"
  - Cover the resulting jump cuts with B-roll.
  — (search summary) [NYFA](https://bk.nyfa.edu/student-resources/how-to-edit-an-interview-for-a-documentary); [Todd Boruff](https://toddboruff.substack.com/p/my-interview-editing-process); [Doc Film Academy](https://www.docfilmacademy.com/blog/how-to-edit-a-documentary-film); [Frame.io text-based editing](https://blog.frame.io/2023/10/16/premiere-pro-text-based-editing/)
- **Pacing trend (context for "is it too slow"):**
  - Cutting reports that the average shot length of English-language films fell from about 12 s (1930) to about 2.5 s today, using Barry Salt's data on 15,000+ films.
  - A Cornell release gives about 5 s (silent era), up to about 10 s (early sound), declining to about 4 s.
  - Secondary reporting gives 8–10 s in the 1960s and 3–4 s by 2005.
  - Cutting rejects MTV as the cause: the decline shows no 1982 inflection.
  - The figures vary by sample and should be treated as approximate.
  — (search summary) [Cornell Chronicle](https://news.cornell.edu/node/271563); [FlowingData](https://flowingdata.com/2014/09/22/evolution-of-movies/); [Cutting et al., PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)
- **Short-form social:**
  - The first ~3 s decide retention, and the retention curve drops fastest at the very start.
  - One vendor claims most loss happens in the first 1.5 s. This is unverified.
  - Best practice is to "reset attention every few seconds" with pattern interrupts (cut, text, zoom, sound), and often a loopable ending.
  - Structure: hook → value → payoff → CTA.
  - Edit for mute viewing with captions.
  — (search summary; practitioner and vendor sources, not platform data) [SocialKit hooks](https://socialk.it/en/blog/video-hooks-first-three-seconds); [skills.sh short-form](https://skills.sh/iart-ai/tiktok-video-skills/short-form-video); [Contra](https://contra.com/s/2PZXAokB-short-form-video-editing-hooks-pacing-and-ai-enhanced-cuts)

### Inferences
- **Self-evaluation loop for an AI editor:**
  1. **Fresh-eyes approximation.** After a cutting pass, re-evaluate the whole timeline in one linear "watch-down" without editing, logging every moment of confusion, boredom, or a cut that "bumps."
  2. **Change modality.** Do one pass picture-only (silent) for faces and eye-trace. Do one pass audio-only for dialogue rhythm and sound bumps.
  3. **"Earns its place" test.** For every shot or scene, state its story and emotion function. If it does neither, and isn't deliberate texture or breathing room (Walker's caveat), it is a candidate for removal.
  4. **Trim heads and tails.** Start a shot as late as possible and leave as early as possible, once its idea, the "blink," has landed. Shave first (the Schoonmaker approach). Remove whole scenes only when shaving can't fix structure or length.
  5. **Map notes.** Classify each note into a symptom: bored, confused, not hooked, or emotion not landing. Then fix the cause the note points to (structure, stakes, clarity, performance choice, pacing) rather than literally applying the suggested fix. Prioritise notes that repeat across reviewers.
  6. **Versioning.** Keep every cut as a named, dated version, e.g. `Assembly_v1`, `RoughCut_v3`, `FineCut_v25`, with a change log of what changed and why (cf. Walker's bin comments). That way an alternate can be compared or a removed darling restored.
- **Format differences:**
  - **Narrative:** emotion- and performance-led. Continuity is the default. Test with a target-demographic audience.
  - **Documentary:** structure is found in the edit via transcripts and a paper edit. Tightening is word-level. B-roll covers jump cuts. Story clarity notes dominate.
  - **Short-form social:** hook in the first 1–3 s; visible change every few seconds; jump cuts accepted; captions mandatory; judged by retention curves rather than audience questionnaires.
- **Cut-rate sanity bands** (from the sources above; not hard rules):
  - Narrative dialogue: about 6 cuts/min.
  - Action: about 25 cuts/min.
  - Modern feature average shot length: about 2.5–4 s.
  - Short-form: faster still, with a change every few seconds.

### Gaps
- No sourced editor quotes were found that literally use "kill your darlings." The principle is supported by Frame.io's "check your ego… cut scenes, jokes or characters you love."
- Murch's documented practice of taking notes on emotional first impressions of dailies, and his views on screenings, were not retrieved. The Cinephilia Beyond interview was blocked by a bot check.
- Sam and Bobbie O'Steen's (*Cut to the Chase*, *The Invisible Cut*), Michael Kahn's, and Reisz & Millar's specific guidance on evaluation and notes could not be accessed.
- No professional standard was found for version naming. The scheme above is an inference.
- The Team Deakins podcast covers Walker's views on the pros and cons of test screenings, but its contents weren't retrievable.
- Short-form numbers come from vendor or creator blogs, not platform-published data. No reliable source gives a specific cut interval in seconds.
