---
title: Match Statement
draft: false
weight: 15
---

{{< include file="/2022/match-statement.md.part" >}}

{{< youtube XpxTrDDcpPE >}}

Structural pattern matching is 80% faster
than similarly structured conditional structures,
thanks to custom bytecode instructions like `MATCH_STATEMENT`.

To see how the `match` statement looks in a basic conditional structure:

{{< include file="/2022/_includes/perfect_match.py" language="python" options="linenos=table,anchorlinenos=true" >}}
