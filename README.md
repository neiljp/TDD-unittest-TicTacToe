# TicTacToe - developed by TDD using unittest in Python

## Motivation & Inspiration

After participating in the 2017 [Global Day of Code Retreat (GDCR)](https://coderetreat.org)
in Portland, OR, I found myself wishing to explore TDD further. I had
previously heard of TDD, but not applied it strictly, and it had not been part
of any of my formal education.

I had previously worked on simplifying the [Zulip](https://zulipchat.com)
TicTacToe bot, so rather than spoil my experience of a future GDCR, I chose to
apply the process to this alternative simple system.

## Objectives

- Explore implementing a TicTacToe engine in python 3;

- Develop further knowledge of applying the [python unittest library](https://docs.python.org/3/library/unittest.html);

- Experience the [TDD](https://en.wikipedia.org/wiki/Test-driven_development) approach.

## Process

Following the TDD process, I implemented the basics of the engine. In the
computer branch I added the option of a computer player, which I initially
implemented from experience & intuition, and subsequently from research on
best-performing moves from
[wikipedia](https://en.wikipedia.org/wiki/Tic-tac-toe) and elsewhere.

## Outcomes

- The engine is essentially near-complete, including a computer player.

- While I had worked previously with existing tests within Zulip, this was a
  great experience to learn and observe where approaches I had seen there could
  be applied in other situations, eg. test-class inheritance.

- As in the GDCR, I found the TDD approach quite refreshing. Not only is
  testing being integral to the process reassuring to enable refactoring, but
  also a great means to focus upon what tasks need to be performed by the code.

## Status & future development

The engine is near-complete, and my personal goals have been met.

Future work is likely to involve an alternative test framework or language,
somewhat similar to the same-task different-implementation approach of GDCR.
