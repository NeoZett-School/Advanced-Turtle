# A pygame based turtle graphics module for Python
# Version 1.0 - 2. 20. 2026
# 
# Copyright (C) 2026 - 2027  Neo Östlund Zetterberg
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

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