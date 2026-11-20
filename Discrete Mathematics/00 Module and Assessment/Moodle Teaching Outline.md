# Moodle teaching outline — saved 17 November 2026

Source: COMP0147, course ID 56448. The text below is the overview and weekly text returned by the Moodle connection. Source activity links are preserved. It is a dated snapshot; the current Moodle page remains authoritative.

# General

### Welcome to COMP0147 Discrete Mathematics for Computer Scientists

This Moodle course is the central point of your Connected Learning experience for Discrete Mathematics for Computer Scientists and contains everything you need to know about it. It's where you'll find key module and assessment information, weekly readings and other materials, and all learning activities. Some activities are designed to help you feel at home in this space while others will guide your learning individually, with tutors, and your peers.

This course is designed to provide you with the basic mathematical tools and concepts essential to Computer Science. Together, we will explore topics such as logic, set theory, combinatorics, and more—building the skills that underpin algorithm design, programming, and the theory of computation.

We, the teaching team, encourage you to engage fully with the course material, ask questions, and collaborate with your peers. We look forward to seeing your progress throughout the term.

#### Key Module Information

- `url` **Module description** — moduleId: `8625361` — [open](https://moodle.ucl.ac.uk/mod/url/view.php?id=8625361)

  UCL’s Module Catalogue provides summary information for all modules running at the University in the current academic year. To view the summary of this module enter the module code or keywords from its title.

#### Module Overview

The module aims to equip first year computer science students with knowledge of foundational mathematics and logic that will be needed for future computer science modules. To provide students with basic tools and skills for mathematical problem solving, proof and refutation.

Students are provided with weekly problem sheets and attend weekly problem classes to work through the problems.

COMP0147 introduces the mathematical foundations essential for computer science, focusing on formal reasoning, proof techniques, and discrete structures. The module combines theoretical understanding with practical applications, helping students develop the precision and logical thinking required in computing.

Teaching will take place through a mix of lectures, problem-solving classes, and guided exercises. Lectures will introduce key ideas, definitions, and theorems, while the problem sheets will reinforce understanding through hands-on practice and collaborative discussion. Students will be encouraged to reason carefully, write clear proofs, and connect abstract concepts to computational examples.

The module is organised into thematic blocks:

-

**Week 1: Logic** – Propositional Logic, Applications of Propositional Logic, logical equivalence, Predicates and Quantifiers, Rules of Inference.

-

**Week 2: Proofs** – Introduction to Proofs, Proof Methods and Strategy, Introduction to number theory: Divisibility and Modular Arithmetic, Primes and Greatest Common Divisors.

-

**Week 3: Sets & Functions** – Sets, Set Operations, Functions.

-

**Week 4: Sets & Functions** – Sequences and Summations, Cardinality of Sets, Foundations of Mathematics.

-

**Week 5: Induction** – Mathematical Induction, Strong Induction and Well-Ordering.

-

**Week 6: Recursion**– Recursive Definitions and Structural Induction, Recursive Algorithms, Program Correctness.

-

**Week 7: Counting** – Combinatorial methods including permutations, combinations, binomial coefficients, and the inclusion–exclusion principle.

-

**Week 8: Relations** – Equivalence relations, partial orders, and graphical representations.

-

**Weeks 9–10: Graph Theory** – Graphs, paths, cycles, trees, colourings, and planar graphs.

#### Formative Assessment and Developmental Learning

Formative assessment and developmental learning activities are designed to help you succeed in your summative assessments. Throughout the module, you will complete weekly exercises designed to develop your understanding of discrete mathematics and your ability to construct rigorous mathematical proofs. Lectures and Problem Solving sessions provide opportunities to discuss solutions, ask questions, and receive feedback from teaching staff. Practice quizzes and additional exercises are also provided to help you identify areas for improvement and prepare for the final examination.

#### Accessibility

##### Digital Accessibility Statement

UCL is committed to equity of opportunity for all students, including those with disabilities and specific learning difficulties. We are working to improve the digital accessibility of our learning resources and platforms, but recognise that some resources provided may not currently be accessible to all students.

- In this course we provide a range of resources in Word, PowerPoint, and PDF format which are keyboard navigable accessible to students using a screen reader.
- Alternative formats are available on demand using Blackboard Ally. [Ally works to convert common file types to other formats](https://wiki.ucl.ac.uk/x/dAZXBw) automatically and in line with the original file. These alternatives include audio (mp3), PDF, ePub for eReaders, or Braille reader files.
- If you require an accessible version (e.g. an alternative format) of any of the resources used in this module that is not provided by Ally, please contact e.pimentel@ucl.ac.uk.

#### Study Tools and Resources

We encourage students to make sure they are familiar with all the tools and resources UCL has to offer.

##### Basic bibliography

- Kenneth H. Rosen. Discrete Mathematics and its Applications (8th Edition). McGraw Hill, 2019.
- L. Lovász , J. Pelikán , K. Vesztergombi, Discrete Mathematics: Elementary and Beyond, Undergraduate Texts in Mathematics, 2003.

##### Other bibliography

- Ralph P. Grimaldi, Discrete And Combinatorial Mathematics (Fifth Edition), Addison Wesley, 2003.
- Ronald Graham, Donald Knuth, Oren Patashnik, Concrete Mathematics: A Foundation for Computer Science, 1994.
- Heather Macbeth, The Mechanics of Proof, https://hrmacbeth.github.io/math2001/index.html, 2024.


---

# Week 1

**Getting Started**

In this first lecture, we will have a general view of the course, establish the notation and study L**ogic!**

Propositional Logic, Applications of Propositional Logic, logical equivalence, Predicates and Quantifiers, Rules of Inference.

Sections covered from the main textbook (Rosen):

- Chapter 1.1: Propositional Logic
- Chapter 1.2: Applications of Propositional Logic
- Chapter 1.3: Propositional Equivalences
- Chapter 1.4: Predicates and Quantifiers
- Chapter 1.5: Nested Quantifiers

- `resource` **List 0 -- Warm-Up Challenges** — moduleId: `8511638` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=8511638)

  This first list of exercises is designed to get you thinking in flexible and creative ways. The problems highlight different styles of reasoning, from careful analysis of conditions to uncovering hidden patterns. They are intended to engage your curiosity, sharpen your problem-solving instincts, and prepare you for tackling more advanced challenges later on. Trust me: you will need it!

- `resource` **List 0 -- solutions** — moduleId: `8511639` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=8511639)

- `resource` **List 1 -- First-order logic** — moduleId: `9379563` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9379563)

- `resource` **List 1 -- solutions** — moduleId: `9379564` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9379564)

- `resource` **Slides -- Numbers** — moduleId: `9379601` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9379601)

- `resource` **Slides -- Logic** — moduleId: `9379603` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9379603)


---

# Week 2

**Proofs and more proofs!**

Introduction to Proofs: direct proofs, proof by contraposition, proof by contradiction. Proof methods and strategy. Parity and divisibility, modular arithmetic, primes and greatest common divisors, sieve of Eratosthenes.

Sections covered from the main textbook (Rosen):

-

Chapter 1.7: Introduction to Proofs

-

Chapter 1.8: Proof Methods and Strategy

-

Chapter 4.1: Divisibility and Modular Arithmetic

-

Chapter 4.3: Primes and Greatest Common Divisors

- `resource` **Slides -- Proofs** — moduleId: `8511645` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=8511645)

- `resource` **List 2 -- Proofs and Modular Arithmetic** — moduleId: `9439443` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9439443)

- `resource` **List 2 -- Solutions** — moduleId: `8511646` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=8511646)

##### The Mathocalypse: A lively take about the latest breakthrough in Mathematics!

Last Tuesday (06/10/2026) was surely one of the biggest days in mathematical history, when 372 huge results were [released by OpenAI.](https://openai.com/index/sharing-ai-progress-in-mathematics/)

The blogpost "[The Mathocalypse](https://scottaaronson.blog/?p=10169)" by Scott Aaronson offers a thought-provoking discussion of the release and its implications for mathematics.

It’s well worth reading!

##### Instructions on how to install LEAN in your computer

_(Warning for Windows users: please make sure your Windows username does not have any spaces in it._

_If you have multiple hard drives on your machine please ensure that Lean is installed on the same hard drive as your Lean code files are stored.)_

Before starting the installation process ensure you have at least 5GB of free space and that your system is up-to-date.

1. If you do not already have a Github account sign up for a free one at https://github.com/ (As a student you can sign up for a Github Education account that will be useful if you want to use Codespaces, but this isn't required.)

2. If you don't have git installed then now install it following the instructions here:
https://kinsta.com/knowledgebase/install-git/

3. Install VS Code + Lean4 extension by following steps 1-2 on the following page:
https://lean-lang.org/install/

4. Clone the math2001 repository by doing the following:

- Open VS Code
- Click "Source Control" (the 3rd icon from the top on the left of VS Code)
- Click "Clone Repository"
- Paste the repository URL into the textbox: https://github.com/hrmacbeth/math2001.git
- VS Code will ask you to choose a folder to store the code. You need to remember what this is!

5. Logout and then log-in again.

6. Open a file. If you see a message in the Lean InfoView saying that you need to “Restart the file,” just click the button in the bottom right corner.

You should be ready to go!


---

# Week 3

**Basic Structures: Functions and Sets**

Injectivity, surjectivity, bijectivity, Composition of functions, Product types, partitions.

Sections covered from the main textbook (Rosen):

-

Chapter 2.1: Sets

-

Chapter 2.2: Set Operations

-

Chapter 2.3: Functions

- `resource` **Slides -- Sets and functions** — moduleId: `9459635` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9459635)

- `resource` **List 3 -- Sets and functions** — moduleId: `9459686` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9459686)

- `resource` **List 3 -- Solutions** — moduleId: `9459700` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9459700)


---

# Week 4

**Basic Structures: Functions and Sets**

Sequences summations, cardinality.

Sections covered from the main textbook (Rosen):

-

Chapter 2.4: Sequences and Summations

- Chapter 2.5: Cardinality of Sets

- `resource` **Slides -- Set Cardinality and Countability** — moduleId: `9470370` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9470370)

- `resource` **Slides -- Sequences, Summations, and Products** — moduleId: `9470504` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9470504)

- `resource` **List 4 -- Sequences, sums, cardinality** — moduleId: `9470602` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9470602)

- `resource` **List 4 -- solutions** — moduleId: `9471094` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9471094)

- `resource` **Recording - Lecture 4** — moduleId: `9484469` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9484469)


---

# Week 5

**Mathematical induction**

Induction, strong Induction and Well-Ordering.

Sections covered from the main textbook (Rosen):

- Chapter 5.1: Mathematical induction
- Chapter 5.2: Strong Induction and Well-Ordering

- `resource` **Slides -- Induction, Strong Induction and Well Ordering** — moduleId: `8511663` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=8511663)

- `resource` **List 5 -- Induction** — moduleId: `9479843` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9479843)

- `resource` **List 5 - solutions** — moduleId: `9479942` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9479942)


---

# Week 6

**Recursion**

Recursive Definitions and Structural Induction, Recursive Algorithms

Sections covered from the main textbook (Rosen):

- Chapter 5.3: Recursive Definitions and Structural Induction
- Chapter 5.4: Recursive Algorithms

- `resource` **Slides -- Recursion and structural induction** — moduleId: `9491738` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9491738)

- `resource` **List 6 - recursion** — moduleId: `9492759` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9492759)


---

# Week 7

**Counting**

The Basics of Counting, The Pigeonhole Principle, permutations, combinations, binomial coefficients; inclusion-exclusion principle; Applications of Recurrence Relations.

Sections covered from the main textbook (Rosen):

- Chapter 6.1: The Basics of Counting
- Chapter 6.2: The Pigeonhole Principle
- Chapter 6.3: Permutations and Combinations
- Chapter 6.4: Binomial Coefficients and Identities
- Chapter 6.5: Generalized Permutations and Combinations
- Chapter 8.4: Inclusion--Exclusion

- `resource` **Slides -- Counting** — moduleId: `9492320` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9492320)

- `resource` **List 7 - counting** — moduleId: `9495155` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495155)


---

# Week 8

**Relations**

Basic properties of relations; equivalences and partial orders. Graphical representation of relations.

Sections covered from the main textbook (Rosen):

- Chapter 9.1: Relations and Their Properties
- Chapter 9.2: n-ary Relations and Their Application
- Chapter 9.3: Representing Relations
- Chapter 9.4: Closures of Relations
- Chapter 9.5: Equivalence Relations
- Chapter 9.6: Partial Orderings

- `resource` **Slides -- Relations** — moduleId: `9492033` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9492033)

- `resource` **List 8 - relations** — moduleId: `9495227` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495227)


---

# Week 9

**Graph Theory -- Part I**

Graphs, basic terminology and examples; connectivity; paths, cycles, trees, and forests.

Sections covered from the main textbook (Rosen):

- Chapter 10.1: Graphs and Graph Models
- Chapter 10.2: Graph Terminology and Special Types of Graphs
- Chapter 10.3: Representing Graphs and Graph Isomorphism
- Chapter 10.4: Connectivity

- `resource` **Slides -- Graphs Part I** — moduleId: `9495381` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495381)

- `resource` **List 9 - Graphs Part I** — moduleId: `9495520` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495520)


---

# Week 10

**Graph Theory -- Part II**

Further topics in Graphs. Bipartite graphs and even/odd cycles; colourings, planar graphs and Euler's formula.

Sections covered from the main textbook (Rosen):

- Chapter 10.5: Euler and Hamilton Paths
- Chapter 10.6: Shortest-Path Problems
- Chapter 10.7: PlanarGraphs
- Chapter 10.8: Graph Coloring

Preparing for the exam: the mock test!

- `resource` **Slides -- Graphs Part II** — moduleId: `9495514` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495514)

- `resource` **List 10 -- Graphs Part II** — moduleId: `9495818` — [open](https://moodle.ucl.ac.uk/mod/resource/view.php?id=9495818)


---
