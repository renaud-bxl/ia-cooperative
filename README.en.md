# Cooperative AI

[Bilingual project website](https://renaud-bxl.github.io/ia-cooperative/en.html)

[Français](README.md)

**Concept and direction: Renaud Ben Lakhal — contact@renaud.brussels**

Could people voluntarily contribute part of their computers' memory and compute to a useful AI service, while keeping control of their machines?

This public research project explores that question. Its proposed design combines adjustable resource limits, trusted groups formed around measured connections, and independent work distributed between groups.

**Current status: research architecture, reproducible simulations and initial planning tools.** The repository does not yet provide a distributed inference engine, a working participant mesh or a signed consumer application. Its software licence remains to be selected; public source availability is not a claim of an open-source licence.

## Research documents

- [46-page illustrated technical report, in French](reports/IA_cooperative_v1.4.pdf)
- [Architecture](docs/ARCHITECTURE.md), [mesh design](docs/MESH.md) and [measurement protocol](docs/BENCHMARKS.md)
- [Software catalogue](catalog/software.json) and [reproducible experiments](experiments)

## Try the existing tools

With Python 3.11 or newer, run from the repository directory:

```bash
python3 -m coopai quota --installed-gb 36 --available-gb 12 --reserve-gb 2 --percent 20
python3 -m coopai plan examples/mac_circle.json
python3 -m unittest discover -s tests -v
```

These commands calculate a memory ceiling and a fictitious placement. They do not allocate shared memory, enforce operating-system limits or run an AI model. A separate [benchmark client](benchmarks/ollama_local.py) can measure an already installed local Ollama model; the project has not run that benchmark on participants' hardware.

## What we need next

Choose one model and a compatible runtime. Integrate it across two or three trusted machines. Measure quality, memory, first-token latency, throughput, failures and owner comfort against appropriate single-machine baselines. Then test across separate addresses before inviting wider participation.

Useful contributions include networking review, runtime integration, reproducible hardware measurements and usability testing. [Contributing instructions](CONTRIBUTING.md) and [research questions](docs/RESEARCH_QUESTIONS.md) are currently in French.

Distributed inference has substantial prior art, including [Petals](https://github.com/bigscience-workshop/petals) and [exo](https://github.com/exo-explore/exo). We do not claim to have invented it or to have their endorsement.

Research, drafting, simulations and code were prepared with AI assistance. No hardware speedup, energy saving or worldwide service availability has been demonstrated by this project.
