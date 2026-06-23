# Curated Safe-to-Cite Foundational References

These are well-known, verifiable references that can be cited confidently by domain.
All entries include a BibTeX snippet ready to paste into `references.bib`.

---

## Software Architecture & Design

```bibtex
@book{bass2003software,
  author    = {Bass, Len and Clements, Paul and Kazman, Rick},
  title     = {Software Architecture in Practice},
  edition   = {2nd},
  publisher = {Addison-Wesley},
  year      = {2003}
}

@article{fielding2000rest,
  author = {Fielding, Roy Thomas},
  title  = {Architectural Styles and the Design of Network-based Software Architectures},
  school = {University of California, Irvine},
  year   = {2000},
  note   = {Doctoral dissertation}
}

@book{gamma1994design,
  author    = {Gamma, Erich and Helm, Richard and Johnson, Ralph and Vlissides, John},
  title     = {Design Patterns: Elements of Reusable Object-Oriented Software},
  publisher = {Addison-Wesley},
  year      = {1994}
}
```

---

## Databases & Storage

```bibtex
@article{codd1970relational,
  author  = {Codd, Edgar F.},
  title   = {A Relational Model of Data for Large Shared Data Banks},
  journal = {Communications of the ACM},
  volume  = {13},
  number  = {6},
  pages   = {377--387},
  year    = {1970}
}

@inproceedings{chang2008bigtable,
  author    = {Chang, Fay and Dean, Jeffrey and Ghemawat, Sanjay and others},
  title     = {{Bigtable}: A Distributed Storage System for Structured Data},
  booktitle = {Proceedings of OSDI},
  year      = {2006}
}

@inproceedings{decandia2007dynamo,
  author    = {DeCandia, Giuseppe and Hastorun, Deniz and others},
  title     = {Dynamo: Amazon's Highly Available Key-value Store},
  booktitle = {Proceedings of SOSP},
  year      = {2007}
}
```

---

## Web & Distributed Systems

```bibtex
@inproceedings{dean2004mapreduce,
  author    = {Dean, Jeffrey and Ghemawat, Sanjay},
  title     = {{MapReduce}: Simplified Data Processing on Large Clusters},
  booktitle = {Proceedings of OSDI},
  year      = {2004}
}

@article{brewer2012cap,
  author  = {Brewer, Eric},
  title   = {{CAP} Twelve Years Later: How the "Rules" Have Changed},
  journal = {IEEE Computer},
  volume  = {45},
  number  = {2},
  pages   = {23--29},
  year    = {2012}
}

@inproceedings{lamport1978time,
  author    = {Lamport, Leslie},
  title     = {Time, Clocks, and the Ordering of Events in a Distributed System},
  journal   = {Communications of the ACM},
  volume    = {21},
  number    = {7},
  pages     = {558--565},
  year      = {1978}
}
```

---

## Machine Learning & AI

```bibtex
@book{goodfellow2016deep,
  author    = {Goodfellow, Ian and Bengio, Yoshua and Courville, Aaron},
  title     = {Deep Learning},
  publisher = {MIT Press},
  year      = {2016}
}

@article{lecun1998gradient,
  author  = {LeCun, Yann and Bottou, Léon and Bengio, Yoshua and Haffner, Patrick},
  title   = {Gradient-Based Learning Applied to Document Recognition},
  journal = {Proceedings of the IEEE},
  volume  = {86},
  number  = {11},
  pages   = {2278--2324},
  year    = {1998}
}

@article{vaswani2017attention,
  author  = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title   = {Attention Is All You Need},
  journal = {Advances in Neural Information Processing Systems (NeurIPS)},
  year    = {2017}
}
```

---

## Security

```bibtex
@book{anderson2008security,
  author    = {Anderson, Ross},
  title     = {Security Engineering: A Guide to Building Dependable Distributed Systems},
  edition   = {2nd},
  publisher = {Wiley},
  year      = {2008}
}

@article{rivest1978rsa,
  author  = {Rivest, Ron and Shamir, Adi and Adleman, Leonard},
  title   = {A Method for Obtaining Digital Signatures and Public-Key Cryptosystems},
  journal = {Communications of the ACM},
  volume  = {21},
  number  = {2},
  pages   = {120--126},
  year    = {1978}
}
```

---

## IEEE Standards

```bibtex
@techreport{ieee830,
  title       = {{IEEE} Recommended Practice for Software Requirements Specifications},
  institution = {IEEE},
  number      = {IEEE Std 830-1998},
  year        = {1998}
}

@techreport{ieee1016,
  title       = {{IEEE} Standard for Information Technology -- Systems Design -- Software Design Descriptions},
  institution = {IEEE},
  number      = {IEEE Std 1016-2009},
  year        = {2009}
}

@techreport{ieee12207,
  title       = {{ISO/IEC/IEEE} International Standard -- Systems and Software Engineering -- Software Life Cycle Processes},
  institution = {IEEE},
  number      = {IEEE Std 12207-2017},
  year        = {2017}
}
```

---

## Cloud & DevOps

```bibtex
@inproceedings{armbrust2010view,
  author    = {Armbrust, Michael and Fox, Armando and Griffith, Rean and others},
  title     = {A View of Cloud Computing},
  journal   = {Communications of the ACM},
  volume    = {53},
  number    = {4},
  pages     = {50--58},
  year      = {2010}
}

@book{kim2016devops,
  author    = {Kim, Gene and Humble, Jez and Debois, Patrick and Willis, John},
  title     = {The DevOps Handbook},
  publisher = {IT Revolution Press},
  year      = {2016}
}
```

---

## How to use this file

When generating references for a paper:
1. Identify which domains the SDD's technology stack falls into
2. Select relevant entries from above
3. Supplement with `% TODO: verify` placeholders for anything more specific
4. **Never invent authors, titles, journals, or page numbers**
