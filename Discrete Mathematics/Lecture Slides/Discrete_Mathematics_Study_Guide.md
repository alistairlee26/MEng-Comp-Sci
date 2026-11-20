# Discrete Mathematics: Weeks 1–5
## COMP0147 • Summary and catch-up guide

Based on the seven lecture PDFs supplied, Term 1, 2026/27, by Elaine Pimentel and Mário Sérgio Alvim. Prepared 3 November 2026.

**Scope.** “Week” follows the lecture number in the filenames; the files do not establish the actual teaching calendar. All seven decks are covered, including number theory inside Lecture 2 and both Lecture 4 decks. The 352 PDF pages include repeated animation steps, which are consolidated here. Page references below are PDF page numbers, counting the title page as page 1.

**How to use this guide.** Read the overview, work through each week, then attempt its checkpoint without notes. Check the answers at the end. Tick a learning objective only when you can explain it and solve a new example. The summaries describe the supplied teaching; the catch-up schedule, checkpoints and some explanatory examples are study aids added for you. Priorities reflect dependencies, not predicted exam weightings: no assessment brief or past paper was supplied.

**Maths notation.** ℕ includes 0 in this module; ℤ+ starts at 1. The notation x^n means “x to the power n”; a_k means the term indexed by k. Σ and Π denote sums and products, with bounds written in words or parentheses. Aᶜ denotes the complement of A in the stated universal set U. [a] denotes an equivalence class.

## Your catch-up priorities

The module is cumulative. Logic gives you the language; proof techniques let you justify statements; sets and functions provide the objects; countability and induction use all three. Reading worked solutions will help, but catching up requires writing arguments yourself.

| Priority | Learn to do this | Why it matters |
| --- | --- | --- |
| 1 | Translate implications and quantified statements; negate them correctly | This tells you exactly what a problem asks and what would disprove it |
| 2 | Write direct, contrapositive and contradiction proofs from definitions | These methods recur throughout every later topic |
| 3 | Work with sets and prove injectivity, surjectivity and bijectivity | Countability depends on these definitions |
| 4 | Calculate with divisibility, modular arithmetic, gcd and Bézout coefficients | Lecture 2 contains a substantial number-theory section |
| 5 | Read and reindex sequences, sums and products | These are common inputs to induction proofs |
| 6 | Write complete weak and strong induction proofs | You must handle the base, hypothesis, step and range correctly |
| 7 | Construct enumerations and explain diagonalisation | This connects infinite sets to limits of computation |

**First milestone:** without notes, negate “every student solved some problem”, prove that the square of an odd integer is odd, classify x ↦ x² on ℝ → ℝ, and write the induction step for 1 + … + n = n(n + 1)/2. If these are difficult, start at Week 1 and follow the sequence below.

## Week 1 — Numbers and logic

**Sources:** Lecture1-Numbers.pdf, pp. 1–25; Lecture1-Logic.pdf, pp. 1–130.

### 1.1 Number systems and representations

**Natural numbers:** ℕ = {0, 1, 2, …}. The slides introduce them through 0 and the successor operation s(k) = k + 1: 0 is natural, and the successor of a natural number is natural. This motivates generating numbers by repeated steps and later induction; these two observations alone are not a complete axiomatisation of ℕ.

**Integers:** ℤ = {…, −2, −1, 0, 1, 2, …}; ℤ+ = {1, 2, …}. **Rationals:** ℚ = {p/q : p, q ∈ ℤ, q ≠ 0}. **Irrationals:** ℝ ∖ ℚ. **Reals:** ℝ contains both rational and irrational numbers. Thus ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ. Later slides also name ℂ, the complex numbers, and positive real numbers ℝ+.

Positional notation assigns weights to digits: in base b, a digit in position i contributes d_i b^i. Decimal uses base 10 and binary uses base 2. For example, 723 = 7·10² + 2·10 + 3 and (110111)₂ = 32 + 16 + 4 + 2 + 1 = 55. To convert an integer to binary, repeatedly divide by 2 and read the remainders backwards: 77 = (1001101)₂.

Fractional positions have negative powers: (0.11)₂ = 2^(−1) + 2^(−2) = 3/4. Infinite digit expansions can represent reals, with a minus sign used for negative values. Representations need not be unique: 0.999… = 1 and (0.111…)₂ = 1. The decimal identity follows from the geometric sum (9/10)/(1 − 1/10) = 1.

A real number is rational exactly when its decimal expansion is **eventually periodic**; terminating decimals have a repeating tail of zeros. For x = 0.121212…, subtract x from 100x to get 99x = 12, hence x = 12/99 = 4/33. Fractions p/q and r/s are equal iff ps = qr, with nonzero denominators. A fraction can be reduced until gcd(p, q) = 1. A finite numerical calculator display gives a rational approximation, even when the intended exact value is irrational.

The key irrationality proof is √2 ∉ ℚ. Suppose √2 = p/q in lowest terms. Then p² = 2q², so p is even (an odd number has an odd square). Put p = 2t; then q² = 2t², so q is even too. This contradicts lowest terms.

Both rationals and irrationals occur between any two distinct real numbers. Rational + rational is rational; rational + irrational is irrational; irrational + irrational can be rational (√2 − √2 = 0) or irrational (√2 + √2 = 2√2). An algebraic number is a root of a nonzero polynomial with rational coefficients; a transcendental number is not. The slides use π as a transcendental example and π + e as a caution against assuming that the sum of two irrationals is automatically irrational. They also preview irrational x, y for which x^y is rational, proved in Week 2, and the different cardinalities of ℚ and ℝ, studied in Week 4.

### 1.2 Propositions, connectives and truth tables

A **proposition** is a declarative statement with a definite truth value. “2 + 2 = 3” is a proposition, although false. Questions and commands are not propositions. An open expression such as “x + 2 = 3” is a predicate whose truth depends on x. Propositional variables p, q, … stand for propositions.

| p | q | ¬p | p ∧ q | p ∨ q | p XOR q | p → q | p ↔ q |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T | T | F | T | T | F | T | T |
| T | F | F | F | T | T | F | F |
| F | T | T | F | T | T | T | F |
| F | F | T | F | F | F | T | T |

Negation reverses truth; conjunction requires both statements; inclusive disjunction requires at least one; XOR requires exactly one. The conditional p → q is false only when p is true and q is false. A biconditional requires matching truth values. Operator precedence in the slides is ¬, ∧, ∨, →, ↔; use parentheses when unclear. A truth table for n independent propositional variables has 2^n rows.

For p → q, p is a **sufficient** condition for q and q is a **necessary** condition for p. “p only if q” means p → q; “p if q” means q → p. “q whenever p” means p → q. Read these carefully before doing algebra.

| Related statement | Formula | Equivalent to p → q? |
| --- | --- | --- |
| Converse | q → p | Generally no |
| Inverse | ¬p → ¬q | Generally no |
| Contrapositive | ¬q → ¬p | Yes |

A tautology is always true; a contradiction is always false. Logical equivalence, written ≡, means two formulas agree under every truth assignment. Establish it by comparing truth-table columns or by a justified chain of equivalences. For example, (p ∧ q) → (p ∨ q) is a tautology.

Bits use 1 for true and 0 for false. Apply AND, OR and XOR position by position to equal-length strings: for 0110 and 1101 the results are respectively 0100, 1111 and 1011.

### 1.3 Logical equivalences to know

| Law | Equivalences |
| --- | --- |
| Identity and domination | p ∧ T ≡ p; p ∨ F ≡ p; p ∧ F ≡ F; p ∨ T ≡ T |
| Idempotence and double negation | p ∧ p ≡ p; p ∨ p ≡ p; ¬¬p ≡ p |
| Commutativity | p ∧ q ≡ q ∧ p; p ∨ q ≡ q ∨ p |
| Associativity | (p ∧ q) ∧ r ≡ p ∧ (q ∧ r); likewise for ∨ |
| Distributivity | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r); p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) |
| De Morgan | ¬(p ∧ q) ≡ ¬p ∨ ¬q; ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Absorption and negation | p ∨ (p ∧ q) ≡ p; p ∧ (p ∨ q) ≡ p; p ∨ ¬p ≡ T; p ∧ ¬p ≡ F |
| Conditional | p → q ≡ ¬p ∨ q ≡ ¬q → ¬p; ¬(p → q) ≡ p ∧ ¬q |
| Biconditional | p ↔ q ≡ (p → q) ∧ (q → p) ≡ (p ∧ q) ∨ (¬p ∧ ¬q) |

The slides also give derived forms: p ∨ q ≡ ¬p → q; p ∧ q ≡ ¬(p → ¬q); p ↔ q ≡ ¬p ↔ ¬q; and ¬(p ↔ q) ≡ p ↔ ¬q. Combining conditionals gives (p → q) ∧ (p → r) ≡ p → (q ∧ r), and (p → r) ∧ (q → r) ≡ (p ∨ q) → r. With ∨ instead of ∧ between those conditionals, the corresponding conclusions are p → (q ∨ r) and (p ∧ q) → r. You can derive these by replacing each implication with ¬p ∨ q rather than memorising every variant.

Worked simplification: ¬(p → q) ≡ ¬(¬p ∨ q) ≡ ¬¬p ∧ ¬q ≡ p ∧ ¬q. Each equality has a reason: eliminate implication, apply De Morgan, remove double negation. The longer example ¬(p ∨ (¬p ∧ q)) simplifies to ¬p ∧ ¬q using the same laws plus distribution.

### 1.4 Predicates and quantifiers

A predicate P(x₁, …, x_n) becomes a proposition when all variables are assigned values or appropriately quantified. Its arity is its number of variables; its **domain of discourse** specifies allowed inputs; its truth set contains inputs making it true. For P(x): x > 3 over ℤ, the truth set is {4, 5, …}.

∀x P(x) means every allowed x satisfies P; ∃x P(x) means at least one does. A universal claim is disproved by one counterexample; an existential claim is proved by one witness. Domains matter: ∃x (x² = −1) is false over ℝ but true over ℂ.

Quantifier order encodes dependence. Over ℤ, ∀x ∃y (x + y = 0) is true: choose y = −x. But ∃y ∀x (x + y = 0) is false: no single y works for all x. “Everyone loves someone” and “someone is loved by everyone” are similarly different statements.

**Negation rules:** ¬∀x P(x) ≡ ∃x ¬P(x); ¬∃x P(x) ≡ ∀x ¬P(x). Keep quantifiers in order, swapping each as you move the negation inward. Thus ¬∀x ∃y R(x, y) ≡ ∃x ∀y ¬R(x, y).

Use a conditional for “all members of a category”: ∀x (Student(x) → Passed(x)). Use conjunction for “some member of a category”: ∃x (Student(x) ∧ Passed(x)). The negation of the universal is ∃x (Student(x) ∧ ¬Passed(x)), meaning at least one student did not pass; it does not say everyone failed.

∀ distributes over ∧, and ∃ distributes over ∨. The corresponding swaps generally fail: ∃x (P(x) ∧ Q(x)) requires the **same witness**, whereas (∃x P(x)) ∧ (∃x Q(x)) can use different witnesses. Similarly, everyone satisfying P or Q does not mean that everyone satisfies P, or everyone satisfies Q.

An implication with a false antecedent is true. Consequently “every ball on the empty plate is blue” is **vacuously true**: no ball on the plate is a counterexample. Universal statements do not assert that members of the described category exist.

### 1.5 Inference, validity and fallacies

An argument has premises and a conclusion. It is valid if no interpretation makes all premises true and the conclusion false. Validity concerns truth preservation, not whether the premises actually hold. A valid argument with true premises is sound. An invalid argument can still have a true conclusion.

| Inference rule | Premises ⇒ conclusion |
| --- | --- |
| Modus ponens | p → q, p ⇒ q |
| Modus tollens | p → q, ¬q ⇒ ¬p |
| Hypothetical syllogism | p → q, q → r ⇒ p → r |
| Disjunctive syllogism | p ∨ q, ¬p ⇒ q |
| Addition | p ⇒ p ∨ q |
| Simplification | p ∧ q ⇒ p |
| Conjunction | p, q ⇒ p ∧ q |
| Resolution | p ∨ q, ¬p ∨ r ⇒ q ∨ r |

Universal instantiation takes ∀x P(x) to P(c). Existential instantiation introduces a fresh name c for a witness, without assuming extra properties of c; existential generalisation takes P(c) to ∃x P(x). Universal generalisation requires an arbitrary element, not a specially chosen example. Universal modus ponens combines instantiation and modus ponens: ∀x (P(x) → Q(x)) and P(c) give Q(c).

For example, from “some student did not read the book” and “all students passed”, take a witness c who is a student and did not read. Instantiate the universal to infer c passed, then conclude “someone passed without reading”. Keep the same c throughout.

Two formal errors are **affirming the consequent** (p → q and q, therefore p) and **denying the antecedent** (p → q and ¬p, therefore ¬q). The addendum also discusses ad hominem (attacking the speaker), ad populum (popularity as proof), begging the question (assuming the conclusion), and appeal to ignorance (lack of disproof as proof). Other named errors include false dilemmas, appeals to antiquity/authority/emotion, straw men, reversing cause and effect, non-sequiturs, and treating “after” as “because of”. Identify the faulty reasoning; a bad argument does not by itself establish that its conclusion is false.

**Clarification to Logic p. 124:** false premises make an argument unsound, but do not automatically make its form invalid. Informal fallacies concern flaws in content, relevance or assumptions; the slide's definition should not blur validity and truth.

### Week 1 — What you need to learn

- [ ] Classify numbers, convert decimal/binary integers and interpret binary fractions.
- [ ] Explain eventual periodicity, 0.999… = 1 and the √2 contradiction proof.
- [ ] Build truth tables, simplify formulas and distinguish converse from contrapositive.
- [ ] Translate “if”, “only if”, “necessary” and “sufficient” correctly.
- [ ] Translate and negate nested quantified statements with a stated domain.
- [ ] Build a short inference chain and identify common fallacies.

**Checkpoint W1.** (a) Convert 45 to binary and (0.101)₂ to decimal. (b) Negate ∀x (S(x) → ∃y R(x, y)). (c) Simplify ¬(p → q). (d) Is “p → q; q; therefore p” valid? Give a falsifying assignment. (e) Find a fraction equal to 0.272727….

## Week 2 — Proof techniques and number theory

**Source:** Lecture2-Proofs.pdf, pp. 1–58. Proofs: pp. 3–33; number theory: pp. 35–58.

### 2.1 What a proof is and how to write one

An axiom is an assumption of the mathematical system. A theorem is a proved result; a proposition is usually a smaller result; a lemma supports another proof; a corollary follows readily from an established result; a conjecture awaits proof or disproof. “Proposition” here names a result, while in logic it means a truth-valued statement.

Evidence from many examples is not a universal proof: n² + n + 41 is prime for n = 0, …, 39, but at n = 40 it equals 41². The slides use a counterexample to Euler's fourth-power conjecture to make the same point. They discuss Fermat's Last Theorem and P versus NP as illustrations of the role of difficult conjectures, not as techniques you are expected to reproduce.

State the claim and domains; mark where the proof begins; define every introduced variable; explain each implication using definitions or established results; end with the exact conclusion. Choose an arbitrary element when proving a universal statement. A collection of unexplained equations is usually insufficient.

| Method | What you assume and establish | Useful trigger |
| --- | --- | --- |
| Direct | Assume P and derive Q | Definitions give a clear route |
| Contraposition | Assume ¬Q and derive ¬P | Negating the conclusion gives usable structure |
| Contradiction | Assume the negation of the whole claim; derive an impossibility | Irrationality or non-existence |
| Counterexample | Find one allowed input violating a universal claim | The claim seems too strong |
| Cases/exhaustion | Cover every possible case and prove each | Signs, parity, order or a finite domain |
| Equivalence | Prove P → Q and Q → P | The statement says “iff” |
| Constructive existence | Give a witness and verify its properties | A concrete example can be found |
| Non-constructive existence | Force existence without identifying a particular witness | Contradiction or an exhaustive alternative |

For an implication, a contradiction proof assumes P ∧ ¬Q. Contraposition assumes ¬Q and aims at ¬P. To prove several statements equivalent, a closed cycle P₁ → P₂ → … → P_n → P₁ suffices; an unclosed chain does not.

### 2.2 Representative arguments

**Direct parity proof:** let n be an arbitrary odd integer. Write n = 2k + 1 with k ∈ ℤ. Then n² = 2(2k² + 2k) + 1, an odd integer. Notice the final form explicitly matches the definition.

Other direct examples: if m = s² and n = t², then mn = (st)²; if r = p/q and s = t/u with nonzero denominators, then r + s = (pu + qt)/(qu) is rational.

**Contraposition:** to prove “3n + 2 odd ⇒ n odd”, suppose n is even. Then n = 2k and 3n + 2 = 2(3k + 1) is even. For positive factors ab = n, at least one factor is ≤ √n: if both exceeded √n, their product would exceed n.

**Contradiction:** among 22 selected days at least four share a weekday; otherwise seven weekdays could account for at most 7·3 = 21 days. The √2 proof from Week 1 is another central model.

**Counterexample:** 3 cannot be a sum of two integer squares, because only squares 0 and 1 could occur. **Cases:** min(x, y) + max(x, y) = x + y follows by comparing x and y; |xy| = |x||y| follows by considering their signs, including zero.

**Existence:** 1729 = 10³ + 9³ = 12³ + 1³ gives a constructive witness. For the irrational-power example, let a = (√2)^(√2). If a is rational, x = y = √2 works. If a is irrational, x = a and y = √2 works because a^(√2) = 2. The argument proves existence without deciding which case holds.

Avoid arguing from examples, assuming the conclusion, skipping an algebraic justification, or omitting a possible case. To repair “m + n even ⇒ m − n even”, write m + n = 2k and then m − n = (m + n) − 2n = 2(k − n).

### 2.3 Division, divisibility and equivalence classes

**Euclidean division:** for integers a and b ≠ 0 there are unique integers q, r such that a = bq + r and 0 ≤ r < |b|. Examples: 3 = (−2)(−1) + 1; −7 = 3(−3) + 2. The remainder is nonnegative even when the dividend or divisor is negative.

For positive inputs, repeated subtraction constructs q and r: start q = 0, r = a; while r ≥ b, subtract b from r and add 1 to q. It halts because r decreases; it is inefficient for large quotients. Correctness means showing the result satisfies the specification, as well as showing termination.

**Corrected uniqueness argument (p. 35):** two representations give r − r′ = b(q′ − q), with |r − r′| < |b|. The only multiple of b in that range is 0, so r = r′ and q = q′. The slide's assertion 0 ≤ r − r′ is not guaranteed without ordering the remainders.

Divisibility a ∣ b means b = ac for some c ∈ ℤ. Use this definition in proofs: if b = ak, then b² + 2b = a(ak² + 2k), so a ∣ (b² + 2b). Parity is the special case of divisibility by 2; negative integers are included, e.g. −3 = 2(−2) + 1.

An **equivalence relation** is reflexive (x ∼ x), symmetric (x ∼ y ⇒ y ∼ x), and transitive (x ∼ y and y ∼ z ⇒ x ∼ z). The class [x] consists of all elements equivalent to x. Classes cover the original set and distinct classes are disjoint. Their collection is the quotient set. A representative names a class; it is not the whole class as an individual number.

### 2.4 Modular arithmetic

For a positive modulus n, a ≡ b (mod n) means n ∣ (a − b). Congruence is an equivalence relation. Its n classes form ℤ_n = {[0], [1], …, [n − 1]}, with [a] = {a + kn : k ∈ ℤ}.

Compute addition, subtraction and multiplication using representatives, then reduce modulo n. These operations respect congruence, so changing representatives does not change the result. Addition and multiplication are associative and commutative, with identities [0] and [1]; addition has inverses; multiplication distributes over addition.

Division/cancellation needs care: in ℤ₆, [2][3] = [0] although neither factor is [0]. You cannot cancel an arbitrary nonzero factor as in ℝ. As an explanatory link to Bézout below, a has a multiplicative inverse modulo n exactly when gcd(a, n) = 1.

Digit tests follow from place values: 10 ≡ 1 modulo 3 and 9, so a number has the same residue as its digit sum. Since 10 ≡ −1 modulo 11, use an alternating digit sum for divisibility by 11. For powers, repeatedly square and reduce after each step. The slide example gives 35^15 ≡ 15 (mod 20), using 15 = 8 + 4 + 2 + 1.

### 2.5 Primes, gcd and algorithms

A prime is an integer p ≥ 2 with exactly two positive divisors, 1 and p. A composite integer is ≥ 2 and not prime. Neither 0 nor 1 is prime or composite; keep this restriction explicit when reading p. 47. If n is composite, some prime factor is ≤ √n. Trial division can stop at that bound.

The greatest common divisor gcd(a, b) is the nonnegative common divisor divisible by every common divisor (positive for the positive inputs used here). Numbers with gcd 1 are relatively prime. The Euclidean algorithm repeatedly divides and replaces (a, b) with (b, r). Its key invariant is gcd(a, b) = gcd(b, a − bq): both pairs have exactly the same common divisors. Remainders strictly decrease until 0; the last nonzero remainder is the gcd.

Slide example: 1234 = 54·22 + 46; 54 = 46 + 8; 46 = 8·5 + 6; 8 = 6 + 2; 6 = 2·3. Therefore gcd(1234, 54) = 2. Back-substitution gives **Bézout's identity**, αa + βb = gcd(a, b); here 2 = −7·1234 + 160·54. This is the extended Euclidean algorithm. The coefficients need not be unique.

If gcd(a, b) = 1, Bézout gives αa + βb = 1. Multiplying by c shows that b ∣ ac implies b ∣ c. It also follows that if both a and b divide t, then ab divides t. For a prime p, **p ∣ ab ⇒ p ∣ a or p ∣ b**: if p does not divide a, then gcd(p, a) = 1 and the coprime lemma applies.

The **fundamental theorem of arithmetic** says every integer n ≥ 2 has a prime factorisation, unique up to order. The slides express it as n = p₁^e₁ · … · p_k^e_k with increasing primes and positive exponents. Existence follows by repeatedly extracting the smallest nontrivial divisor, which must be prime. Uniqueness follows by matching a prime across two proposed factorisations using the prime-divides-a-product property, cancelling it and repeating; a least-counterexample argument formalises this.

The **sieve of Eratosthenes** finds all primes up to N. Keep 2 separately; retain odd candidates ≥ 3. For each surviving p ≤ √N, cross out multiples starting at p²; smaller multiples already have a smaller prime factor. In an odd-only array, successive crossed-out values differ by 2p. The revised slide algorithm uses the index (t − 1)/2 for odd value t and must exclude 1. Understand both why the sieve works and how this indexing represents odd values.

### Week 2 — What you need to learn

- [ ] Choose an appropriate proof method and write a complete argument in sentences.
- [ ] Use even/odd, rational, divisibility and perfect-square definitions explicitly.
- [ ] Compute quotient/remainder with signs and explain uniqueness.
- [ ] Verify an equivalence relation; calculate residue classes and modular powers.
- [ ] Run Euclid and back-substitute to obtain Bézout coefficients.
- [ ] Explain the coprime lemma, prime-divides-a-product property, unique factorisation and sieve.

**Checkpoint W2.** (a) Prove odd + odd is even. (b) Find q, r when −17 is divided by 5. (c) Find gcd(252, 198) and express it as 252α + 198β. (d) Compute 7^13 modulo 10. (e) Explain why 2x ≡ 2y (mod 6) does not imply x ≡ y (mod 6). (f) Prove congruence modulo n is transitive.

## Week 3 — Sets and functions

**Source:** Lecture3-sets-functions.pdf, pp. 1–52. Sets: pp. 4–33; functions: pp. 35–52.

### 3.1 Sets, subsets and constructions

A set is an unordered collection of distinct objects. Order and repeated listings do not affect equality. a ∈ A asserts membership; A ⊆ B asserts every member of A is in B. A ⊂ B means a proper subset, so A ⊆ B and A ≠ B. Always distinguish an object from the singleton set containing it.

Sets can be defined by listing elements, set-builder notation {x ∈ D : P(x)}, recursive generation, or a characteristic function μ_A taking value 1 on A and 0 outside A in a specified universe. Recursive generation needs starting elements and rules, with only generated elements included. Venn diagrams illustrate relationships but are not proofs.

The empty set ∅ has no elements; {∅} has one element. ∅ ⊆ A for every A, vacuously. The power set 𝒫(A) contains all subsets of A: 𝒫({a, b}) = {∅, {a}, {b}, {a, b}}. If |A| = n, then |𝒫(A)| = 2^n, because each element is either included or excluded. In particular 𝒫(∅) = {∅}.

An ordered tuple remembers positions; two n-tuples are equal exactly when corresponding entries match. The Cartesian product A × B = {(a, b) : a ∈ A, b ∈ B}; generally A × B ≠ B × A. Products extend to any finite number of factors, and A^n means n repeated factors. For finite sets, the number of choices gives |A × B| = |A||B|.

### 3.2 Operations and proofs of set identities

| Construction | Membership condition |
| --- | --- |
| Union A ∪ B | x ∈ A or x ∈ B |
| Intersection A ∩ B | x ∈ A and x ∈ B |
| Difference A ∖ B | x ∈ A and x ∉ B |
| Complement Aᶜ = U ∖ A | x ∈ U and x ∉ A |
| Indexed union ⋃ A_i | x belongs to at least one indexed set |
| Indexed intersection ⋂ A_i | x belongs to every indexed set |

Set equality means identical membership: A = B iff A ⊆ B and B ⊆ A. Prove it by two inclusions, a chain of membership equivalences, or a membership table. For example, x ∈ (A ∩ B)ᶜ iff ¬(x ∈ A ∧ x ∈ B), iff x ∉ A or x ∉ B, iff x ∈ Aᶜ ∪ Bᶜ.

The logical laws have set counterparts: ∪ and ∩ are commutative, associative, idempotent, distributive over each other and satisfy absorption. Identities are A ∪ ∅ = A and A ∩ U = A; domination gives A ∪ U = U and A ∩ ∅ = ∅. Complements satisfy (Aᶜ)ᶜ = A, A ∪ Aᶜ = U, A ∩ Aᶜ = ∅, Uᶜ = ∅ and ∅ᶜ = U. De Morgan gives (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ and (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ. Difference is A ∖ B = A ∩ Bᶜ, and is generally not commutative.

Disjoint sets have empty intersection. A partition of A consists of nonempty, pairwise disjoint blocks whose union is A. Pairwise disjointness is stronger than merely saying that the intersection of all blocks is empty. Equivalence classes from Week 2 give partitions.

### 3.3 Russell's paradox

The barber who shaves exactly those men who do not shave themselves cannot consistently be one of those men: “the barber shaves himself” would hold iff it did not hold. Russell's analogous definition S = {A : A is a set and A ∉ A} produces S ∈ S iff S ∉ S. The lesson is that arbitrary properties cannot freely define unrestricted sets. Axiomatic approaches such as Zermelo–Fraenkel set theory restrict set construction; you are introduced to the motivation, not a full development of those axioms.

### 3.4 Functions and their types

A total function f : A → B assigns **exactly one** element of B to **every** element of A. A is its domain, B its codomain, and f(A) = {f(a) : a ∈ A} its image/range. The preimage of b is {a ∈ A : f(a) = b}; this set may be empty or have many elements. It does not require an inverse function.

For f = {(x, 2), (y, 4), (z, 2)} from {x, y, z} to {1, 2, 3, 4}, the image is {2, 4}; the preimage of 2 is {x, z}; the preimage of 1 is ∅. Under the course convention, equal functions have the same domain, codomain and outputs at every input.

| Property | Definition | Proof/disproof strategy |
| --- | --- | --- |
| Injective (one-to-one) | f(a₁) = f(a₂) ⇒ a₁ = a₂ | Start from equal outputs; or disprove with a collision |
| Surjective (onto) | ∀b ∈ B ∃a ∈ A, f(a) = b | Start with arbitrary b; find a valid input; or show a missed output |
| Bijective | Injective and surjective | Prove both parts |

For ℝ → ℝ, x + 1 and x/10 are bijections. The square function is neither: 2 and −2 collide, and negative outputs are missed. The exponential 2^x is injective but misses nonpositive reals. The cubic (x − 1)(x − 2)(x − 3) is surjective onto ℝ but not injective, since three inputs give 0. Types matter: x² : [0, ∞) → [0, ∞) is bijective, with inverse √x.

A bijection f : A → B has inverse f⁻¹ : B → A, where f⁻¹(b) = a iff f(a) = b. For f(n) = n + 1 on ℤ, f⁻¹(n) = n − 1. The symbol f⁻¹ here does not mean 1/f.

### 3.5 Composition, identity, floor/ceiling and partial functions

Composition (f ∘ g)(a) = f(g(a)) applies g first. It is defined when the outputs of g lie in the domain of f. Composition is generally not commutative: with f(n) = n + 1 and g(n) = n², (f ∘ g)(n) = n² + 1 while (g ∘ f)(n) = (n + 1)².

The identity id_A maps every a to itself. For f : A → B, f ∘ id_A = f and id_B ∘ f = f. If f is bijective, f⁻¹ ∘ f = id_A and f ∘ f⁻¹ = id_B. A composition of injections is injective; a composition of surjections is surjective. To prove the first, pass equality of outputs backwards through each injection; for the second, choose a preimage through each surjection.

Floor ⌊x⌋ is the greatest integer ≤ x; ceiling ⌈x⌉ is the least integer ≥ x. Both map ℝ to ℤ. For example, ⌊−2.7⌋ = −3 and ⌈−2.7⌉ = −2. Useful properties are ⌊−x⌋ = −⌈x⌉, ⌈−x⌉ = −⌊x⌋, and x − 1 < ⌊x⌋ ≤ x ≤ ⌈x⌉ < x + 1. For proofs write x = ⌊x⌋ + ε with 0 ≤ ε < 1, separating ε = 0 if necessary.

A **partial function** allows some inputs in its declared domain to be undefined; where defined, its output is still unique. The partial map √n from ℤ to ℝ has domain of definition ℕ. Restricting the declared domain to ℕ makes it total.

### Week 3 — What you need to learn

- [ ] Distinguish ∈ from ⊆, ∅ from {∅}, and sets from ordered tuples.
- [ ] Calculate power sets, Cartesian products, complements and differences.
- [ ] Prove a set identity and recognise a partition.
- [ ] Explain Russell's paradox and why unrestricted set formation fails.
- [ ] Identify a function's domain, codomain, image and preimages.
- [ ] Prove or disprove injectivity/surjectivity; calculate inverses and compositions.
- [ ] Work correctly with negative floor/ceiling values and partial functions.

**Checkpoint W3.** (a) List 𝒫({0, 1}) and find |{∅}|. (b) Prove A ∖ B and B are disjoint. (c) Classify f(n) = 2n on ℤ → ℤ and on ℤ → 2ℤ, where 2ℤ is the even integers. (d) Find the inverse of f(x) = 3x − 2 on ℝ. (e) Evaluate ⌊−3.2⌋ and ⌈−3.2⌉. (f) Show that a composition of injections is injective.

## Week 4 — Cardinality, countability, sequences, sums and products

**Sources:** Lecture4-cardinality.pdf, pp. 1–21; Lecture4-sequences.pdf, pp. 1–24.

### 4.1 Comparing infinite sets

Two sets have equal cardinality exactly when a bijection pairs their elements. A set is **countable** if it is finite or bijective with ℤ+; **countably infinite** excludes the finite case. An infinite set need not be uncountable.

Hilbert's Hotel shows why finite-size intuition fails. In a full hotel with rooms 1, 2, …, moving each guest n → n + 1 accommodates one newcomer. Moving n → 2n accommodates a countably infinite bus in odd rooms. Countably many buses can also fit: reserve the even rooms for existing guests, enumerate pairs (bus, passenger) diagonally and place newcomers in successive odd rooms. This solves the slide's challenge.

Positive even integers are countably infinite via n ↦ 2n. Enumerate ℤ as 0, 1, −1, 2, −2, …. Enumerate positive rationals by traversing a numerator/denominator grid diagonally, omitting duplicate fractions. Each fraction is reached after finitely many diagonals; row-by-row traversal would never leave an infinite first row. Include 0 and interleave positives with negatives to enumerate ℚ. The deck also gives an alternative listing of reduced rationals in [0, 1] by denominator, then adds reciprocals and negatives, removing duplicates.

The union of two countable sets is countable: interleave their enumerations and omit repetitions, handling finite/empty sets separately. Every subset of a countable set is countable: restrict its enumeration to retained elements. Consequently, any set containing an uncountable subset is uncountable. In particular, ℕ, ℤ and ℚ have the same cardinality despite being proper subsets of one another.

### 4.2 Diagonalisation and non-computable functions

**Cantor's diagonal argument:** suppose all reals in [0, 1) could be listed r₁, r₂, …. Write their decimal expansions. Build a new real s whose nth digit differs from the nth digit of r_n. Then s differs from each listed number at a designated position, contradicting completeness of the list. Thus [0, 1), and therefore ℝ, is uncountable.

**Precision added to pp. 16–17:** decimal expansions can be non-unique. Choose the expansion of each r_n that does not end in repeating 9s. Let digit n of s be 2 if the corresponding diagonal digit is 1, and 1 otherwise. Then s uses only 1s and 2s, avoiding the repeating-9 ambiguity and ensuring s ∈ [0, 1). Simply incrementing digits modulo 10, as in the slides, needs this extra care.

Finite strings over a finite programming alphabet are countable: list by length, then lexicographically within each length. Programs are a subset, so they are countable. Functions from ℕ to a fixed finite digit set with at least two values are uncountable: diagonalise their output sequences. For binary functions listed as f₀, f₁, …, define g(n) = 1 − f_n(n); g is missing from the list. Hence there are more such functions than programs, so some functions have no computing program. This is a cardinality-based existence argument, not a method for identifying every non-computable problem.

**Reading note for p. 21:** a digit sequence represents a function taking the position n as input and the digit at that position as output; one sentence in the slide reverses that direction.

### 4.3 Sequences and generating rules

A sequence is an ordered list, formally a function from consecutive natural-number indices (often starting at 0 or 1) into a set S. a_n is the term at index n. Unlike a set, a sequence retains order and repetition. Always state the starting index.

An arithmetic progression has constant difference d: a_n = a₀ + nd for n ≥ 0. A geometric progression has constant ratio r: a_n = a₀r^n. With first index 1, use a₁ + (n − 1)d and a₁r^(n − 1). Explicit formulas give a term directly; algorithms give generation instructions; recurrence relations use earlier terms together with initial values.

Examples in the slides include (−1)^n/(n + 1) for n ≥ 0, equivalently (−1)^(n + 1)/n for n ≥ 1 after shifting the index; 3^n − 2 giving 1, 7, 25, 79, … for n ≥ 1; and (−1)^(n + 1)n giving 1, −2, 3, −4, …. Algorithmic examples repeat each positive integer n exactly n times, or append n zeros followed by n ones for successive n. Factorials have a₀ = 1 and a_n = n·a_(n−1).

Matching a finite prefix does not establish the whole sequence: both ordinary counting and listing numbers whose last decimal digit is 1–5 start 1, 2, 3, 4, 5, but their next terms differ. A guessed pattern is a conjecture unless the generating rule is specified.

For sequences on the same index set, equality is termwise. When starting indices differ, explicitly reindex before comparing: a_i = i/(i + 1), i ≥ 1, and b_j = (j − 1)/j, j ≥ 2, have a_i = b_(i+1). The slides call the resulting ordered lists identical; their function domains differ until this shift is made.

### 4.4 Summations, products and reindexing

Σ_(i=m)^n a_i means a_m + a_(m+1) + … + a_n; Π_(i=m)^n a_i means the corresponding product. Endpoints are inclusive, giving n − m + 1 terms when n ≥ m. The index is bound (a dummy variable); parameters such as m and n are free. Renaming a bound index changes nothing if variable capture is avoided; changing a free parameter can change the value.

Examples: Σ_(k=3)^6 k² = 86; Σ_(s∈{0,3,7}) s² = 58; Π_(i=1)^3 i^i = 108. To shift an index, change both the summand and the bounds: with j = k + 1, Σ_(k=0)^6 1/(k + 1) = Σ_(j=1)^7 1/j. Similarly, Σ_(j=2)^4 (j − 1)² = Σ_(k=1)^3 k².

For matching bounds, sums are linear: Σa_k + Σb_k = Σ(a_k + b_k), and cΣa_k = Σ(ca_k). Products combine pointwise: (Πa_k)(Πb_k) = Π(a_kb_k). Do not infer Σ(a_kb_k) = (Σa_k)(Σb_k). Also, equal numerical sums need not have identical lists of terms; matching terms is a sufficient way to prove equality, despite the stronger wording on sequence slide p. 21.

### Week 4 — What you need to learn

- [ ] Define equal cardinality, countable, countably infinite and uncountable.
- [ ] Enumerate ℤ and ℚ and explain why every element is eventually reached.
- [ ] Explain Hilbert's Hotel, the closure properties and Cantor's contradiction.
- [ ] Explain why counting programs and functions proves non-computable functions exist.
- [ ] Generate terms from explicit formulas/recurrences and track index shifts.
- [ ] Expand, evaluate, rename and reindex sums and products correctly.

**Checkpoint W4.** (a) Explain why the multiples of 3 in ℕ have the same cardinality as ℕ. (b) Explain why ℚ ∩ [0, 1] is countable but [0, 1] is not. (c) Give a_n for 5, 8, 11, … with n starting at 1. (d) Reindex Σ_(k=2)^5 (k − 1)² using j = k − 1 and evaluate it. (e) Evaluate Π_(i=1)^4 i. (f) Explain what is missing from a proposed list of all binary functions on ℕ.

## Week 5 — Weak and strong mathematical induction

**Source:** Lecture5-induction.pdf, pp. 1–42. Weak induction: pp. 4–29; strong induction: pp. 31–41; well-ordering: p. 42.

### 5.1 Weak induction and the proof template

To prove P(n) for every integer n ≥ b, prove the base P(b), then prove P(k) → P(k + 1) for an arbitrary fixed integer k ≥ b. The assumption P(k) is the induction hypothesis (IH). Like a staircase, the first step and the rule for moving onward together reach every finite step. The base may be 0, 1, 2, 4 or another stated starting point.

1. Define P(n) precisely, including the range.
2. Prove the base case at the correct starting value b.
3. Assume P(k) for an arbitrary fixed k ≥ b.
4. Write out the target P(k + 1), substituting k + 1 everywhere needed.
5. Derive that target using the IH and justify the remaining steps.
6. Conclude that P(n) holds for every n ≥ b by induction.

You are allowed to assume P(k) while proving the conditional step; this is not assuming the final universal theorem. You must not assume P(k + 1), omit the base or merely verify several examples. Induction proves a proposed property; it does not determine an unknown sequence from a finite prefix.

### 5.2 All the weak-induction examples in the deck

| Result | Starting case | Main inductive move |
| --- | --- | --- |
| 1 + … + n = n(n + 1)/2 | n = 1 | Add k + 1 to k(k + 1)/2 and factor |
| 1 + 3 + … + (2n − 1) = n² | n = 1 | Add 2k + 1 to k² |
| Σ_(i=0)^n 2^i = 2^(n+1) − 1 | n = 0 | Add 2^(k+1) to the IH sum |
| 2^n < n! for n ≥ 4 | n = 4 | 2^(k+1) < 2k! < (k + 1)k! |
| 3 ∣ (n³ − n) for n ≥ 0 | n = 0 | (k + 1)³ − (k + 1) = (k³ − k) + 3(k² + k) |
| An n-element set has 2^n subsets | n = 0 | Pair subsets excluding the new element with those including it |
| (⋂_(j=1)^n A_j)ᶜ = ⋃_(j=1)^n A_jᶜ | n = 2 | Apply two-set De Morgan, then the IH |
| A 2^n × 2^n board with any one square removed admits L-tromino tiling | n = 1 | Split into four quadrants; place one central tromino; apply IH to each |

The introduction also mentions n! ≤ n^n for n ≥ 1: each factor in n! is at most n. For the board result, the central tromino covers the central square of each of the three quadrants without the original missing square. All four quadrants now have exactly one unavailable square, so the IH applies. The IH must say **any location** of the missing square, not just a fixed corner.

**Complete model proof:** let P(n) mean Σ_(i=1)^n i = n(n + 1)/2. The base n = 1 gives 1 = 1. Assume P(k) for an arbitrary k ≥ 1. Then Σ_(i=1)^(k+1) i = Σ_(i=1)^k i + (k + 1) = k(k + 1)/2 + (k + 1), using the IH. This equals (k + 1)(k + 2)/2, exactly P(k + 1). Hence the formula holds for all n ≥ 1 by induction.

### 5.3 Strong induction

Strong induction allows the hypothesis P(b), P(b + 1), …, P(k) when proving P(k + 1). It is useful when the next case depends on some smaller value rather than only its immediate predecessor. Establish enough initial cases for the step you actually use.

**Staircase example:** if you can reach steps 1 and 2 and can move two steps at a time, to reach k + 1 use reachability of k − 1. Both starting cases matter.

**Prime factorisation existence:** start at 2. Assume every integer from 2 to k is a product of primes. If k + 1 is prime, it already is such a product. Otherwise k + 1 = ab with 2 ≤ a, b ≤ k. Apply the IH to both factors and combine their prime products. This proves existence; uniqueness is a separate argument from Week 2.

**4- and 5-cent stamps:** every amount n ≥ 12 can be made. Establish 12 = 4 + 4 + 4, 13 = 4 + 4 + 5, 14 = 4 + 5 + 5 and 15 = 5 + 5 + 5. For k ≥ 15, the IH supplies amount k − 3 ≥ 12; adding a 4-cent stamp gives k + 1. One base case would leave gaps when advancing by 4.

**Two-pile Nim:** with equal positive pile sizes and the last match winning, the second player mirrors the first player's removal in the other pile. Either both piles become empty and the second player wins immediately, or a smaller equal-pile position remains with the first player to move. Strong induction on the common pile size proves the strategy; the one-match case starts the argument.

### 5.4 Well-ordering and common traps

The **well-ordering principle** says every nonempty subset of ℕ has a least element. Weak induction, strong induction and well-ordering are equivalent principles in this setting. A least-counterexample argument uses well-ordering: if some natural-number case fails, choose the smallest failure and contradict it using the earlier cases.

For the slide's equivalence challenge, weak induction is a special case of strong induction. Conversely, to simulate strong induction with weak induction, prove the stronger statement Q(k): “P(j) holds for every b ≤ j ≤ k”. This shows that “strong” describes a convenient hypothesis, not greater logical power.

Typical errors: starting at 1 when the claim starts at 0; substituting k + 1 into only part of the target; assuming a needed smaller case outside the IH range; omitting required base cases; multiplying inequalities without checking signs; and writing an induction step that never connects the hypothesis to the target.

### Week 5 — What you need to learn

- [ ] Write a complete weak-induction proof for a sum, inequality and divisibility claim.
- [ ] Explain the subset-counting and generalised De Morgan steps.
- [ ] Explain how the tiling construction makes all four subproblems satisfy the IH.
- [ ] Use strong induction for factorisation, stamps and the Nim strategy.
- [ ] Choose sufficient base cases and check every IH index is in range.
- [ ] State well-ordering and explain its link to least-counterexample proofs.

**Checkpoint W5.** (a) Prove by induction that the first n positive odd integers sum to n². (b) Explain why the stamp proof needs four consecutive base cases. (c) Prove 3 ∣ (n³ − n) for n ≥ 0 by induction. (d) Explain why prime-factorisation existence naturally uses strong induction. (e) Describe exactly where the central tromino goes in the tiling proof.

## A practical catch-up schedule

Use 10 focused sessions of about 60–90 minutes as a starting estimate, taking longer where needed. For each session: spend roughly 15–20 minutes reviewing, 35–50 minutes solving without notes, and 10–20 minutes correcting and explaining mistakes. Keep up with new lectures alongside this backlog.

| Session | Focus | Evidence that you are ready to move on |
| --- | --- | --- |
| 1 | Number systems, binary, connectives and truth tables | Complete W1(a), (c), (e); explain the conditional truth table |
| 2 | Translation, quantifiers, negation and inference | Complete W1(b), (d) and translate five new English statements |
| 3 | Direct, contrapositive, contradiction, cases and existence proofs | Write three short proofs from definitions and reproduce √2 irrationality |
| 4 | Division, congruences, gcd and Bézout | Complete W2(b)–(f) with workings |
| 5 | Primes, coprime lemma, factorisation and sieve | Explain the main proofs and sieve the primes up to 50 |
| 6 | Sets, operations, partitions and paradoxes | Complete W3(a), (b); prove one De Morgan identity |
| 7 | Functions, inverses, composition, floor/ceiling | Complete W3(c)–(f), stating domains and codomains |
| 8 | Countability, diagonalisation and computability | Reconstruct ℚ's enumeration and the real-number diagonal proof |
| 9 | Sequences, sums/products and weak induction | Complete W4(c)–(e), then write two induction proofs |
| 10 | Strong induction and mixed practice | Explain stamps, factorisation and Nim; redo missed checkpoints |

**If time is very limited:** first practise quantifier negation, proof structure, injective/surjective definitions, gcd/Bézout and both induction templates. Then fill the remaining topics from the weekly checklists. This is a dependency-based triage plan, not a claim that other topics will be absent from assessment.

Use your actual tutorial sheets or problem sets after these checkpoints; they can establish the module's expected difficulty more reliably than a summary alone. For each error, record the definition or inference you missed, then solve a similar question the next day without looking at the solution.

## Checkpoint answers and proof sketches

These are for checking after a serious attempt. For proof questions, compare your assumptions, domains and conclusion as well as the final algebra.

### W1 answers

(a) 45 = 32 + 8 + 4 + 1 = (101101)₂. (0.101)₂ = 1/2 + 1/8 = 5/8 = 0.625.

(b) ∃x (S(x) ∧ ∀y ¬R(x, y)), with the original domains retained. For the student/problem reading: “Some student solved no problem.”

(c) p ∧ ¬q. (d) Invalid: p = F, q = T makes both premises true and the conclusion false. (e) Let x = 0.272727…; 100x − x = 27, so x = 27/99 = 3/11.

### W2 answers

(a) Let a = 2r + 1 and b = 2s + 1 for integers r, s. Then a + b = 2(r + s + 1), which is even. (b) −17 = 5(−4) + 3, so q = −4, r = 3.

(c) 252 = 198 + 54; 198 = 3·54 + 36; 54 = 36 + 18; 36 = 2·18. Hence gcd = 18. Back-substitution: 18 = 54 − 36 = 4·54 − 198 = 4·252 − 5·198, so α = 4 and β = −5.

(d) 7⁴ ≡ 1 (mod 10), so 7^13 = (7⁴)³·7 ≡ 7. (e) x = 1, y = 4 gives 2x ≡ 2y ≡ 2 modulo 6, but 1 is not congruent to 4. The factor 2 has no inverse modulo 6.

(f) If a − b = nr and b − c = ns for integers r, s, then a − c = n(r + s), so a ≡ c (mod n).

### W3 answers

(a) 𝒫({0, 1}) = {∅, {0}, {1}, {0, 1}}; |{∅}| = 1. (b) Membership in A ∖ B requires non-membership in B, so no x belongs to both; their intersection is ∅.

(c) On ℤ → ℤ the function is injective but not surjective because odd integers are missed. On ℤ → 2ℤ it is bijective: every even integer 2k has input k. (d) f⁻¹(y) = (y + 2)/3. (e) −4 and −3 respectively.

(f) Let f : X → Y and g : Y → Z be injective. If g(f(a)) = g(f(b)), injectivity of g gives f(a) = f(b), then injectivity of f gives a = b. Thus g ∘ f is injective.

### W4 answers

(a) n ↦ 3n is a bijection from ℕ to {0, 3, 6, …}; its inverse sends 3n to n. (b) ℚ ∩ [0, 1] is a subset of the countable set ℚ. The interval [0, 1] contains the uncountable subset [0, 1), so is uncountable.

(c) a_n = 5 + 3(n − 1) = 3n + 2 for n ≥ 1. (d) Σ_(j=1)^4 j² = 1 + 4 + 9 + 16 = 30. (e) 1·2·3·4 = 24. (f) If the proposed list is f₀, f₁, …, the binary function g(n) = 1 − f_n(n) differs from every f_n at input n, so is absent.

### W5 answers

(a) Base n = 1: 1 = 1². Assume Σ_(i=1)^k (2i − 1) = k². The next sum is k² + (2(k + 1) − 1) = k² + 2k + 1 = (k + 1)². Conclude by induction for all n ≥ 1.

(b) Adding 4 advances in steps of 4, so 12, 13, 14 and 15 establish every residue class modulo 4. The step for k + 1 uses k − 3, which is in the established range only when k ≥ 15.

(c) Base n = 0: 0 is divisible by 3. Assume 3 ∣ (k³ − k). Then (k + 1)³ − (k + 1) = (k³ − k) + 3(k² + k), a sum of two multiples of 3. Conclude for all n ≥ 0.

(d) The composite case n = ab needs the result for both smaller factors a and b, not merely n − 1. Strong induction supplies all those earlier cases. (e) Place one L-shaped tromino at the centre covering one central square in each quadrant without the original hole. Those covered squares become the three quadrants' unavailable squares; each quadrant can now be tiled using the IH.

## Source map for returning to the slides

| Week | File and PDF pages | Topic |
| --- | --- | --- |
| 1 | Lecture1-Numbers.pdf, 3–14 | Naturals, successors, decimal/binary, integers |
| 1 | Lecture1-Numbers.pdf, 15–25 | Reals, rational/irrational, √2 and cardinality preview |
| 1 | Lecture1-Logic.pdf, 5–30 | Propositions, connectives, truth tables, bitwise logic |
| 1 | Lecture1-Logic.pdf, 31–54 | Equivalence laws and worked simplifications |
| 1 | Lecture1-Logic.pdf, 55–92 | Predicates, domains, quantifiers, negation, vacuous truth |
| 1 | Lecture1-Logic.pdf, 93–120 | Validity and propositional/quantified inference |
| 1 | Lecture1-Logic.pdf, 121–130 | Fallacy addendum |
| 2 | Lecture2-Proofs.pdf, 3–33 | Proof terminology, methods, writing and errors |
| 2 | Lecture2-Proofs.pdf, 35–46 | Division, divisibility, equivalence classes, modular arithmetic |
| 2 | Lecture2-Proofs.pdf, 47–58 | Primes, Euclid/Bézout, factorisation and sieve |
| 3 | Lecture3-sets-functions.pdf, 4–19 | Set definitions, subsets, power sets and products |
| 3 | Lecture3-sets-functions.pdf, 21–33 | Operations, identities, partitions and Russell's paradox |
| 3 | Lecture3-sets-functions.pdf, 35–52 | Functions, inverses, composition, floor/ceiling, partial maps |
| 4 | Lecture4-cardinality.pdf, 5–14 | Hotel, bijections, enumerations and countability properties |
| 4 | Lecture4-cardinality.pdf, 15–21 | Diagonalisation and non-computable functions |
| 4 | Lecture4-sequences.pdf, 3–15 | Sequences, progressions, formulas, algorithms and recurrences |
| 4 | Lecture4-sequences.pdf, 17–24 | Sums/products, bound variables, reindexing and laws |
| 5 | Lecture5-induction.pdf, 4–29 | Weak induction, examples and template |
| 5 | Lecture5-induction.pdf, 31–42 | Strong induction, factorisation, stamps, Nim and well-ordering |

**Completion standard:** you can state the definitions accurately, choose a proof method, solve the checkpoints without notes and explain why your reasoning works. Use the weekly boxes to track that standard rather than the number of pages read.
