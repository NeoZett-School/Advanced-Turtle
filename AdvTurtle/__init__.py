# A pygame based turtle graphics module for Python
# Version 1.0 - 2. 20. 2026
# 
# Copyright (c) 2026 Neo Zetterberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Advanced Turtle: A pygame-based evolution of the standard library Turtle.

Inspired by the performance and abstraction of the original CPython implementation, 
Advanced Turtle is a re-imagining focused on extensibility, maintainability, and modern 
standards. 
While the original 1990s source remains a masterpiece of beginner-friendly design, its 
internal structure—relying on complex inheritance and proxy patterns—can be difficult to 
reason about by modern standards. Advanced Turtle seeks to preserve that "cardinal" 
simplicity for the user while providing a cleaner, more refactorable codebase for the 
developer.

It is not a replacement, but a parallel tool for those who need the power of Pygame with the 
intuitive interface of Turtle.

---

Advanced Turtle was made as a pygame alternative to the CPython version. 
It does not, by any means, stand as replacement, or against, the original 
version and any of its, so to speak, improvements that ensure consistency 
with todays standards. We do only offer an redefinition of the package as 
essentially a whole—given many changes, but it stands truthful to its cardinal 
understanding.

It was inspired by the fact that the original source held very strong 
performance, abstraction, and was quite powerful and easy to understand. 

This package decrees in the same order and is intuitively aspiring 
to function likewise, as a tool that can be, potentially even more, useful and 
powerful, not in pure turtle-practicality but in extensibility, refactoring 
and standardization. It is important to note that we do not mean to say 
that our intentions are to overperform turtle, but to give a tool that is 
improved in specifically extensibility and how it is read, structurally.

Looking at the code of today's turtle as it is provisioned through pythons 
standard library, we find it difficult to reason and understand different 
sections and parts; every class in turtle creates either dummy functions 
or implements new ones or as previously defined in its superclass. It 
makes for a very powerful, but not so much readable and maintainable 
approach—which is understandable, given it was made during 1990, more 
than 30 years ago.

Any proxy often stands futile to attempt in its replacement since it 
carries both historical meaning, and was adapted in an ingenious manner. 
Especially considering aliasing and other abstractions that stand invaluable 
to beginners that are just starting out, using python, in a sense that 
they allow personalization over how you code and a much easier interface 
in many different practicalities.
"""

from sys import version_info
from warnings import warn

if version_info < (3, 10):
    warn(
        "Advanced Turtle is designed for Python >= 3.10 and may not function correctly.",
        RuntimeWarning,
        stacklevel=2,
    )