# COMP0147 — Syllabus and exam preparation guide

**Discrete Mathematics for Computer Scientists · 2026/27 · Moodle checked 17 November 2026**

This guide maps all ten teaching weeks to the current slides, problem sheets and reading. It is a study checklist based on published teaching, not a prediction of the exam questions. Use it alongside later lecturer announcements and the eventual exam instructions.

## Assessment and scope

- **Weighting:** the [UCL 2026/27 catalogue](https://www.ucl.ac.uk/module-catalogue/modules/discrete-mathematics-for-computer-scientists-COMP0147) lists **100% Exam**.
- **Target:** May 2027, as you requested. The exact date, duration, format and permitted materials were not given in the Moodle material inspected; check your exam timetable when available.
- **Working scope:** prepare all ten weeks below. No topic-by-topic mark allocation or final list of examinable theorems was visible.
- **Explicit exclusion:** the **2 November Announcements post** says the supplementary **Foundations of Mathematics video** will not be part of the exam. This excludes that video; it does not exclude the taught sets, cardinality, diagonalisation or proof material.
- **Practice:** weekly exercises are described as formative. No assignment or quiz activities were returned, despite generic overview text mentioning quizzes. Week 10 mentions a mock test, but no separate mock file/activity was visible.
- **Past-exam questions:** nine questions labelled **2025/26 exam** occur in the sheets. See the [exam question index](Past%20Papers/Exam%20Question%20Index.md).

The archive contains **29 original PDFs**: 12 slide decks, 11 problem sheets and six released solution sheets. The [Week 4 recording is linked](Lecture%20Recordings/README.md); its MP4 download was blocked by a browser challenge. See the [Assessment Guide](00%20Module%20and%20Assessment/Assessment%20Guide.md) for evidence and outstanding details.

## How to use this guide

Read a slide section, work through its examples, then attempt the sheet without solutions. Tick an objective when you can explain it and solve a fresh problem unaided. The objectives and milestones are study aids written for you; topic coverage and reading references come from Moodle and the PDFs.

Practise definitions, proofs and counterexamples from the start. Following the dependency order below is useful for catching up; it is not a prediction of exam weightings. Page references are PDF pages, counting the title page as page 1.

## Week 1 — Numbers and logic

**Slides:** [Numbers, 25 pages](Lecture%20Slides/01%20Numbers%20and%20Logic/Lecture1-Numbers.pdf); [Logic, 130 pages](Lecture%20Slides/01%20Numbers%20and%20Logic/Lecture1-Logic.pdf).

**Practice:** [List 0: warm-up](Practice%20Resources/Problem%20Sheets/List0.pdf), [solutions](Practice%20Resources/Solutions/List0-sol.pdf); [List 1: logic](Practice%20Resources/Problem%20Sheets/List1.pdf), [solutions](Practice%20Resources/Solutions/List1-sol.pdf).

**Assigned Rosen, 8th edition:** §§1.1–1.5. Rules of inference are also explicitly named on Moodle and taught in the slides.

- [ ] Distinguish naturals, integers, rationals, irrationals and reals; use the module's convention that naturals include zero.
- [ ] Convert positional representations, including binary integers/fractions; relate rational numbers to eventually periodic expansions.
- [ ] Explain the square-root-of-two irrationality proof and distinguish exact numbers from approximations.
- [ ] Identify propositions/predicates and their domains; use connectives, truth tables, bitwise operators, tautologies and contradictions.
- [ ] Translate necessary/sufficient conditions and biconditionals; distinguish converse, inverse and contrapositive.
- [ ] Simplify formulas using equivalence laws, including De Morgan's laws.
- [ ] Construct disjunctive normal form from a truth table and explain functional completeness (List 1, questions 11–12).
- [ ] Translate and negate quantified statements, track quantifier order, and express uniqueness or “exactly two”.
- [ ] Explain vacuous truth; check argument validity, apply inference rules and recognise fallacies.

**Slide map:** Numbers pp. 3–14: representations; pp. 15–25: reals/rationals/irrationals. Logic pp. 5–30: connectives; pp. 31–54: equivalences; pp. 55–92: quantifiers; pp. 93–120: inference; pp. 121–130: fallacies.

**Readiness check:** translate and negate “every student solved some problem”; distinguish it from “some problem was solved by every student”. Attempt past-exam **List 1, question 20**.

## Week 2 — Proofs and number theory

**Slides:** [Proofs, 58 pages](Lecture%20Slides/02%20Proofs%20and%20Number%20Theory/Lecture2-Proofs.pdf).

**Practice:** [List 2](Practice%20Resources/Problem%20Sheets/List2.pdf), [solutions](Practice%20Resources/Solutions/List2-sol.pdf).

**Assigned Rosen:** §§1.7, 1.8, 4.1, 4.3.

- [ ] Choose and write direct, contrapositive, contradiction and case proofs from definitions.
- [ ] Prove existence constructively or explain a non-constructive argument; prove both directions of an equivalence.
- [ ] Refute a universal statement with a counterexample; detect circular reasoning and unjustified assumptions.
- [ ] Reason about parity, rationality/irrationality, divisibility and the division algorithm.
- [ ] Use congruence/residue classes; justify modular calculations and proofs about possible remainders.
- [ ] Work with primes, composite numbers and factorisation; explain the infinitely-many-primes argument and sieve of Eratosthenes.
- [ ] Compute gcds using Euclid's algorithm and find Bézout coefficients.
- [ ] Apply definitions introduced by a problem, including perfect numbers and the phi-function examples in List 2.

**Slide map:** pp. 3–33: proofs and errors; pp. 35–46: divisibility/congruence; pp. 47–58: primes/gcd/algorithms.

**Readiness check:** prove a parity claim in two ways, express a gcd as an integer linear combination, then attempt past-exam **List 2, question 19**.

## Week 3 — Sets and functions

**Slides:** [Sets and functions, 52 pages](Lecture%20Slides/03%20Sets%20and%20Functions/Lecture3-sets-functions.pdf).

**Practice:** [List 3](Practice%20Resources/Problem%20Sheets/List3.pdf), [solutions](Practice%20Resources/Solutions/List3-sol.pdf).

**Assigned Rosen:** §§2.1–2.3.

- [ ] Distinguish membership/inclusion and the empty set/a set containing it.
- [ ] Construct power sets, Cartesian products and ordered pairs; work with partitions.
- [ ] Calculate set operations and indexed unions/intersections; prove inclusions/identities using arbitrary elements or membership tables.
- [ ] Explain the issue illustrated by Russell's paradox in the taught sets material.
- [ ] Specify a function's domain, codomain and image; check whether it is well-defined.
- [ ] Prove/refute injectivity, surjectivity and bijectivity under the stated domain and codomain.
- [ ] Compose functions, find inverses when they exist and prove properties of compositions.
- [ ] Compute images and **preimages of sets**. Preimages exist even when an inverse function does not; distinguish the two uses of the notation.
- [ ] Calculate and prove floor/ceiling statements; recognise partial functions.

**Slide map:** pp. 4–19: constructions; pp. 21–33: operations/partitions/paradox; pp. 35–52: functions. List 3 supplements the deck with image/preimage proofs.

**Readiness check:** classify squaring under different domains/codomains, then attempt the image/preimage proofs in past-exam **List 3, question 23**.

## Week 4 — Sequences, sums, products and cardinality

**Slides:** [Sequences, 24 pages](Lecture%20Slides/04%20Cardinality%20and%20Sequences/Lecture4-sequences.pdf); [Cardinality, 21 pages](Lecture%20Slides/04%20Cardinality%20and%20Sequences/Lecture4-cardinality.pdf).

**Practice:** [List 4](Practice%20Resources/Problem%20Sheets/List4.pdf), [solutions](Practice%20Resources/Solutions/List4-sol.pdf). [Recording link](Lecture%20Recordings/README.md).

**Assigned Rosen:** §§2.4–2.5.

- [ ] Read sequence indexing; move between explicit formulas, recurrences and generating rules.
- [ ] Use arithmetic/geometric sequences, finite sums and finite products.
- [ ] Reindex sums correctly; distinguish bound/free variables and apply sum/product laws.
- [ ] Model a process with a recurrence, including List 4's loan-balance example.
- [ ] Compare cardinalities using bijections; distinguish finite, countably infinite and uncountable sets.
- [ ] Give enumeration rules, including for integer pairs and finite bit strings.
- [ ] Reason about subsets, differences, intersections and power sets using cardinality arguments.
- [ ] Explain why rationals are countable and how diagonalisation proves uncountability; follow the deck's non-computable-function example.

**Slide map:** Sequences pp. 3–15: rules/recurrences; pp. 17–24: sums/products. Cardinality pp. 5–14: bijections/enumerations; pp. 15–21: diagonalisation.

**Readiness check:** reindex and evaluate a sum; enumerate a countable product; explain precisely why a diagonal construction escapes the proposed list.

## Week 5 — Induction and well-ordering

**Slides:** [Induction, 42 pages](Lecture%20Slides/05%20Induction/Lecture5-induction.pdf).

**Practice:** [List 5](Practice%20Resources/Problem%20Sheets/List5.pdf), [solutions](Practice%20Resources/Solutions/List5-sol.pdf).

**Assigned Rosen:** §§5.1–5.2.

- [ ] State the proposition and integer range, and prove every necessary base case.
- [ ] State an induction hypothesis for an arbitrary permitted index and use it explicitly in the step.
- [ ] Prove sum identities, inequalities and divisibility statements by induction.
- [ ] Choose weak/strong induction and identify the earlier cases the step requires.
- [ ] Handle deck applications to factorisation, stamps, tiling and games, plus binary/Fibonacci arguments from the sheet.
- [ ] Explain well-ordering and diagnose invalid induction proofs.
- [ ] Combine an induction result with number-theoretic reasoning, as in the Fibonacci coprimality question.

**Slide map:** pp. 4–29: weak induction; pp. 31–42: strong induction/applications/well-ordering.

**Readiness check:** write a complete proof from a blank page, then attempt past-exam **List 5, question 17**, on Fibonacci numbers and coprimality.

## Week 6 — Recursion and structural induction

**Slides:** [Recursion, 32 pages](Lecture%20Slides/06%20Recursion/Lecture6-recursion.pdf).

**Practice:** [List 6](Practice%20Resources/Problem%20Sheets/List6.pdf). Solutions are not yet visible.

**Assigned Rosen:** §§5.3–5.4. The general overview additionally names program correctness; see the scope notes below.

- [ ] Define functions recursively with base values and recursive rules; evaluate factorial, power, Fibonacci and nested-recursion examples.
- [ ] Convert suitable explicit sequence formulas into recursive definitions.
- [ ] Define sets recursively and explain which elements the constructors generate.
- [ ] Work with recursively defined strings, string functions, logical formulas and binary trees.
- [ ] Prove properties by structural induction, covering every base object and **every constructor**.
- [ ] Show that a recursive definition generates the intended set, including both containment directions when required.
- [ ] Design recursive algorithms for arithmetic, maxima and modular powers (List 6, questions 11–13).
- [ ] Work through the Ackermann-function exercises and quicksort comparison-count questions (List 6, questions 10 and 14).

**Slide map:** pp. 3–14: functions; pp. 15–21: sets/strings/formulas/trees; pp. 23–32: structural induction. The algorithm exercises go beyond the deck's worked examples.

**Readiness check:** define string reversal, prove a string property structurally, and write a terminating recursive algorithm with a clear base case.

## Week 7 — Counting and combinatorics

**Slides:** [Counting, 82 pages](Lecture%20Slides/07%20Counting/Lecture7-counting.pdf).

**Practice:** [List 7](Practice%20Resources/Problem%20Sheets/List7.pdf). Solutions are not yet visible.

**Assigned Rosen:** §§6.1–6.5. Moodle additionally lists §8.4 (inclusion–exclusion) and names applications of recurrence relations.

- [ ] Choose/combine multiplication and addition principles; split cases without missing possibilities or double-counting.
- [ ] Count functions, injective functions, codes, bit strings and constrained arrangements; use tree diagrams.
- [ ] Apply ordinary/generalised pigeonhole arguments, explicitly identifying objects and boxes.
- [ ] Distinguish ordered/unordered choices and repetition/no repetition.
- [ ] Use permutation/combination formulas, circular arrangements and indistinguishable-object counts.
- [ ] Use binomial coefficients, the binomial theorem and Pascal's identity; justify identities by counting.
- [ ] Count combinations with repetition and constrained nonnegative integer solutions using stars and bars.
- [ ] Use inclusion–exclusion for overlapping conditions; read the separately assigned §8.4.
- [ ] Form recurrence models when a counting problem splits according to earlier cases; revisit sequence/recursion examples.

**Slide map:** pp. 3–26: basic principles/trees; pp. 28–36: pigeonholes; pp. 38–57: permutations/combinations; pp. 59–69: binomial coefficients/identities; pp. 71–82: repetition. Moodle's named inclusion–exclusion and recurrence applications are broader than the deck's dedicated sections.

**Readiness check:** explain why a formula counts each outcome once. Attempt past-exam **List 7, questions 19–20**, on polygon diagonals and geometric pigeonholes.

## Week 8 — Relations, equivalence and partial orders

**Slides:** [Relations, 96 pages](Lecture%20Slides/08%20Relations/Lecture8-relations.pdf).

**Practice:** [List 8](Practice%20Resources/Problem%20Sheets/List8.pdf). Solutions are not yet visible.

**Assigned Rosen:** Moodle lists §§9.1–9.6; the sheet's reading box omits §9.2. Keep §9.2 on the reading list until clarified.

- [ ] Define relations as sets of ordered pairs; represent them by lists, digraphs and Boolean matrices; recognise functions as special relations.
- [ ] Prove/refute reflexivity, symmetry, antisymmetry and transitivity. Antisymmetry is not the negation of symmetry.
- [ ] Combine/compose relations; compute powers and Boolean-matrix products with the correct order convention.
- [ ] Construct reflexive, symmetric and transitive closures; reason about minimality and the order of closure operations.
- [ ] Prove equivalence relations; move between equivalence classes and partitions.
- [ ] Recognise partial orders, posets, comparability and total orders.
- [ ] Use lexicographic order and draw Hasse diagrams without loops or transitively implied edges.
- [ ] Find lower bounds/greatest lower bounds in examples such as divisibility; List 8 supplies these definitions.
- [ ] Review the n-ary relation topic in Moodle's §9.2 reading, even though the deck focuses on binary relations.

**Slide map:** pp. 3–12: definitions; pp. 14–42: properties; pp. 44–57: combinations/composition; pp. 59–69: closures; pp. 71–82: equivalence/partitions; pp. 84–96: orders/Hasse diagrams.

**Readiness check:** classify a relation with a proof or counterexample for every property. Attempt past-exam **List 8, questions 19–20**.

## Week 9 — Graph theory I

**Slides:** [Graphs I, 47 pages](Lecture%20Slides/09%20Graphs%20I/Lecture9-graphsI.pdf).

**Practice:** [List 9](Practice%20Resources/Problem%20Sheets/List9.pdf). Solutions are not yet visible.

**Assigned Rosen:** §§10.1–10.4. Moodle also names trees and forests.

- [ ] Model situations as vertices/edges; distinguish simple graphs, multigraphs, pseudographs and directed graphs.
- [ ] Use adjacency, incidence, degree, indegree and outdegree; account correctly for loops.
- [ ] Apply the handshaking theorem and degree-counting arguments.
- [ ] Work with complete graphs, cycles, wheels, hypercubes, complete bipartite/regular graphs and complements.
- [ ] Explain bipartitions, two-colourability and the absence of odd cycles.
- [ ] Translate between adjacency lists, adjacency matrices and incidence matrices.
- [ ] Exhibit an isomorphism or refute one using invariants; matching degree sequences alone is insufficient.
- [ ] Reason about paths/circuits, connected components, strong/weak connectivity, bridges, cut vertices and vertex/edge connectivity.
- [ ] Count walks/paths of specified length under the question's conventions; prove reachability/component facts.
- [ ] Know tree/forest definitions and their connection to acyclicity; revisit Week 6 binary trees and prove the connected-graph edge bound in List 9, question 19.

**Slide map:** pp. 3–15: types/models; pp. 16–30: degrees/families/bipartiteness; pp. 31–38: representations/isomorphism; pp. 39–47: connectivity.

**Readiness check:** represent a graph three ways, prove a degree fact and compare two graphs for isomorphism. Terminology varies: use the course/question's definitions of “path”, “simple” and “circuit”.

## Week 10 — Graph theory II

**Slides:** [Graphs II, 37 pages](Lecture%20Slides/10%20Graphs%20II/Lecture10-graphsII.pdf).

**Practice:** [List 10](Practice%20Resources/Problem%20Sheets/List10.pdf). Solutions are not yet visible.

**Assigned Rosen:** §§10.5–10.8, including shortest-path problems (§10.6).

- [ ] Distinguish Euler paths/circuits (edges) from Hamilton paths/circuits (vertices).
- [ ] Apply degree/connectivity criteria for Euler paths/circuits, including the directed versions in List 10.
- [ ] Construct examples or prove impossibility, including for standard graph families.
- [ ] Use the sufficient Hamiltonicity condition named in the deck, Dirac's theorem, with its hypotheses; do not mistake sufficiency for necessity.
- [ ] Compare Hamilton circuits in small weighted graphs for the travelling-salesperson exercise; also review the assigned shortest-path chapter.
- [ ] Distinguish drawing crossings from inherent nonplanarity; identify planar regions, including the unbounded region.
- [ ] Apply Euler's planar formula and edge bounds with the required hypotheses to prove nonplanarity.
- [ ] Recognise the K5/K3,3 examples and review the Kuratowski topic named on slide 26; a requirement to prove the full theorem was not established.
- [ ] Determine/prove chromatic numbers, model scheduling/maps with colouring, and know the four-colour theorem's statement.
- [ ] Work with edge colouring as introduced in List 10, question 15.
- [ ] Prove/refute preservation of graph properties after deleting an edge (past-exam List 10, question 16).

**Slide map:** pp. 3–13: Euler; pp. 14–18: Hamilton/TSP; pp. 19–26: planarity; pp. 27–37: colouring.

**Readiness check:** justify an Euler classification, prove nonplanarity using a valid bound, and give both a colouring and a lower-bound argument for a chromatic number.

## Scope details to revisit when exam guidance appears

An absence from a slide deck is not an exclusion. Keep the following broader Moodle/reading items in view:

| Item | Published evidence | Preparation action |
| --- | --- | --- |
| Recursive algorithms | Week 6, Rosen §5.4, List 6 questions 11–14 | Complete the algorithm/comparison-count exercises |
| Program correctness | General overview's Week 6 block | Review how induction justifies recursive programs; confirm intended depth if no further teaching appears |
| Inclusion–exclusion; recurrence applications | Week 7, including Rosen §8.4 | Read the listed section and practise overlap/recurrence reasoning |
| n-ary relations | Week 8 lists §9.2; sheet reading box omits it | Review definitions and watch for clarification |
| Trees/forests | Week 9 description; binary trees in Week 6 | Cover definitions and relevant induction/graph exercises |
| Shortest-path problems | Week 10 and List 10 list §10.6 | Review the chapter; confirm which named algorithms, if any, are expected beyond the TSP example |
| Mock test | Week 10 description | Collect when visible and use its instructions to refine practice |

## Catch-up plan towards May 2027

Start with **three sessions of 60–90 minutes per week**, adjusted to your workload: one for definitions/examples, one for written problems, and one for delayed retries and older topics. This is suggested preparation time, not a module workload requirement.

| Period | Work | Milestone |
| --- | --- | --- |
| Rest of November–December | Weeks 1–3; continue current teaching where possible | Translate statements, write short proofs, handle functions/images/preimages |
| January | Weeks 4–6 and weak prerequisites | Explain countability and write complete numerical/structural induction proofs |
| February | Weeks 7–10 | Every teaching week has attempted exercises and a definition/theorem sheet |
| March | Mixed questions across the module | Choose methods without topic hints; fix recurring errors |
| April | Indexed past-exam questions and any newly released mock/papers | Timed work under the published exam conditions, followed by error review |
| May, before the confirmed exam | Recall and targeted retries | Recall definitions/hypotheses and resolve remaining weak questions |

Start with List 1's translation/quantifier questions and two short proofs from List 2. The [earlier detailed Weeks 1–5 guide](Lecture%20Slides/Discrete_Mathematics_Study_Guide.md) provides explanations/checkpoints; this ten-week syllabus tracks full coverage.

For every substantial topic, keep accurate definitions, independently written solutions, at least one proof/refutation and a retry date. After checking a solution, close it and reconstruct the argument later.

## Refresh before revision season

- [ ] Collect solutions for Lists 6–10 as released. The 11 November announcement says solutions become visible after Tuesday PBL sessions.
- [ ] Collect the mock test, complete papers and any new exam guidance.
- [ ] Record the confirmed date, duration, format and permitted aids.
- [ ] Incorporate lecturer-stated inclusions/exclusions and corrections.
- [ ] Recheck the broader reading items above and compare any updated resources with this snapshot.

Sources: [Moodle course](https://moodle.ucl.ac.uk/course/view.php?id=56448), all ten weekly sections and original PDFs; [Announcements](https://moodle.ucl.ac.uk/mod/forum/view.php?id=8511614), especially 2/11 November; the UCL catalogue above. The [Resource Index](00%20Module%20and%20Assessment/Resource%20Index.md) links every saved file and its source activity.
