# MLPerf® Endpoints Rules

*MLPerf Endpoints Rules Task Force — Version 1.0 Draft — 2026-05-05*

**Companion documents:**
- Submission, review, and publication process: [endpoints_submission_rules.md](endpoints_submission_rules.md)
- General MLPerf submission rules (inherited where not overridden): [submission_rules.adoc](https://github.com/mlcommons/policies/blob/master/submission_rules.adoc)

---

## Table of Contents

1. [Basics](#1-basics)
2. [Divisions and Deployment Scenarios](#2-divisions-and-deployment-scenarios)
   - [2.1 Client Deployment Scenarios](#21-client-deployment-scenarios)
   - [2.2 Standardized Division](#22-standardized-division)
   - [2.3 Serviced Division](#23-serviced-division)
   - [2.4 RDI Division](#24-rdi-research-development-and-internal-division)
   - [2.5 Division Summary](#25-division-summary)
   - [2.6 Reproducibility Requirements](#26-reproducibility-requirements)
   - [2.7 Transparency Requirements](#27-transparency-requirements)
   - [2.8 Tokenizer Rules](#28-tokenizer-rules)
   - [2.9 Model Equivalence Rules (Standardized Division)](#29-model-equivalence-rules-standardized-division)
3. [Benchmarks and Models](#3-benchmarks-and-models)
   - [3.1 Benchmark Definition](#31-benchmark-definition)
   - [3.2 Supported Models](#32-supported-models)
   - [3.3 Weight Transformations](#33-weight-transformations)
4. [Metrics](#4-metrics)
   - [4.1 Primary Metrics](#41-primary-metrics)
   - [4.2 Derived and Presentation Metrics](#42-derived-and-presentation-metrics)
   - [4.3 Accuracy Metric](#43-accuracy-metric)
5. [Pareto Collection Methodology](#5-pareto-collection-methodology)
   - [5.1 What Is Measured](#51-what-is-measured)
   - [5.2 Pareto Curve Representation](#52-pareto-curve-representation)
   - [5.3 Minimum Submission Requirements](#53-minimum-submission-requirements)
   - [5.4 Regions of Interest](#54-regions-of-interest)
   - [5.5 Region Boundary Reference Algorithm](#55-region-boundary-reference-algorithm)
   - [5.6 Maximum Point Cap](#56-maximum-point-cap)
6. [Run Requirements Per Measurement Point](#6-run-requirements-per-measurement-point)
   - [6.1 Load Pattern](#61-load-pattern)
   - [6.2 Minimum Run Duration](#62-minimum-run-duration)
   - [6.3 Warmup Period](#63-warmup-period)
   - [6.4 Minimum Completed Queries](#64-minimum-completed-queries)
   - [6.5 Dataset Considerations](#65-dataset-considerations)
   - [6.6 Accuracy Requirement](#66-accuracy-requirement)
7. [Publication Status](#7-publication-status)
8. [Submission Requirements](#8-submission-requirements)
   - [8.1 Directory Structure](#81-directory-structure)
   - [8.2 System Description (system\_desc\_id.json)](#82-system-description-system_desc_idjson)
   - [8.3 Measurement Point YAML](#83-measurement-point-yaml)
   - [8.4 Software Disclosure](#84-software-disclosure)
   - [8.5 Result ID](#85-result-id)
9. [Compliance Validation](#9-compliance-validation)
   - [9.1 Automated Checks](#91-automated-checks)
   - [9.2 Manual Review Focus Areas](#92-manual-review-focus-areas)
- [Appendix A: Open Questions and Working Group Items](#appendix-a-open-questions-and-working-group-items)
- [Appendix B: Quick-Reference Region Boundary Table](#appendix-b-quick-reference-region-boundary-table)

---

## 1. Basics

These rules define the technical requirements for MLPerf Endpoints benchmark submissions: what to measure, how to measure it, which division to submit under, and what evidence is required for each publication status category.

The submission, review, and publication *process* are defined separately in the companion [MLPerf Endpoints Submission Rules](endpoints_submission_rules.md) document.

> [!NOTE]
> **Rule Stability.** These rules are *tentative* until the first MLPerf Endpoints submission round (v0.7) closes on **2026-06-26**. Sections explicitly marked **`[TENTATIVE — Subject to change after 2026-06-26]`** are most likely to evolve between v0.7 and **v1.0** (next submission tentatively **2026-09-01**, after which rolling submission begins) based on submitter feedback and working-group discussion. The traditional MLPerf Inference v6.1 round on **2026-07-31** runs in parallel and is unaffected by Endpoints rule changes. See [Submission Rules §4.0](endpoints_submission_rules.md#40-submission-milestones) for the full milestone table.

MLPerf Endpoints measures the performance of *inference endpoints* serving generative AI models. Unlike traditional MLPerf Inference benchmarks — which measure latency or throughput at a single operating point — MLPerf Endpoints characterizes the full performance *envelope* of a serving system as a Pareto curve across a range of concurrency levels.

The benchmark is designed to be:

- **Fair** — standardized measurement methodology with compliance validation.
- **Inclusive** — minimum 7 measurement points with flexible placement to accommodate systems of all scales.
- **Relevant** — covering operating points valued by real users: single-user interactive latency through high-throughput batch serving.
- **Extensible** — modular rules that can accommodate new models, metrics, and divisions without redesign.

---

## 2. Divisions and Deployment Scenarios

MLPerf Endpoints replaces the traditional Closed/Open division structure from MLPerf Inference with three divisions tailored to endpoint benchmarking: **Standardized**, **Serviced**, and **RDI**. All divisions use the same pareto collection methodology ([§5](#5-pareto-collection-methodology)) and run requirements ([§6](#6-run-requirements-per-measurement-point)). A submission must declare exactly one division.

For readers familiar with MLPerf Inference's Closed/Open structure: **Standardized** plays the role of *Closed* (strict equivalence, full disclosure); **Serviced** is a new division for commercial endpoint services with no direct MLPerf Inference analog; **RDI** (Research / Development / Internal) plays the role of *Open*. The Available/Preview/RDI **publication status** dimension is *orthogonal* to the division; see [Submission Rules §7](endpoints_submission_rules.md#7-publication) for which (division, status) combinations are valid.

### 2.1 Client Deployment Scenarios

MLPerf Endpoints defines two scenarios that determine how the client infrastructure connects to the System Under Test (SUT).

#### 2.1.1 Client on Prem (CoP)

The submitter hosts both the client infrastructure and the endpoint server infrastructure. The client and server may be co-located in the same data center or connected via a local network.

- The submitter provides and operates both client and server infrastructure.
- The client must use the MLPerf Endpoints reference client (`inference_endpoint` from `github.com/mlcommons/endpoints`) without source-code modification, compiled from a commit accessible to the MLCommons review committee. Submitters MAY configure runtime behavior via the YAML configuration file the client accepts; everything that changes behavior MUST be expressible via that YAML. The client logs the commit SHA used for the run; review may additionally use a seeded RNG check (analogous to LoadGen's RNG-output check in MLPerf Inference) to detect undisclosed client modifications.
- Network latency between client and server is included in all timing measurements.
- The submitter must document the network topology between client and server, including type of interconnect, number of hops, and measured baseline network latency.
- On-prem submissions must be self-contained: all components required to replicate the result must be documented and provided.

#### 2.1.2 Client over Network (CoN)

MLCommons is responsible for the client infrastructure, which interrogates the System Under Test via an endpoint accessed over the public Internet.

- MLCommons operates the client infrastructure at a designated location.
- The submitter provides a publicly accessible endpoint URL that the MLCommons client can reach.
- All timing measurements include public Internet network latency between the MLCommons client and the submitter's endpoint.
- CoN submitters must provide equivalent containers and code to replicate the server in alternative locations, clusters, or data centers for identical hardware and software configurations.
- The endpoint must conform to the MLPerf Endpoints reference API specification.

> [!NOTE]
> The specific MLCommons client locations, network requirements, and scheduling procedures for CoN submissions will be published separately by the working group.

#### 2.1.3 Scenario Summary

| Property | Client on Prem (CoP) | Client over Network (CoN) |
|---|---|---|
| Client operator | Submitter | MLCommons |
| Server operator | Submitter | Submitter |
| Network | Local / data center | Public Internet |
| Network latency included | Yes | Yes |
| Reference client required | Yes | Yes (MLCommons-hosted) |

---

### 2.2 Standardized Division

The Standardized division is the primary benchmark division, requiring strict adherence to model equivalence rules and full software disclosure. It replaces the traditional "Closed" division from MLPerf Inference.

**Transparency:** Whitebox — model weights, configurations, optimization details, and launch / integration scripts must be disclosed. The serving framework and low-level software stack must satisfy the **Available** definition in the Submission Rules ([Submission Rules §7.2](endpoints_submission_rules.md#72-available)); they need not be open-sourced verbatim if the Available criteria are met.

**Available Scenarios:** Client on Prem (CoP) and Client over Network (CoN), reported as separate sub-divisions.

#### 2.2.1 General Rules

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** This section ports the MLPerf Inference optimization framing to a strictly disallowed-list ("blacklist") style. The exact disallowed entries below may be revised after v0.7 submitter feedback.

**Inheritance.** Standardized division submissions inherit the model-equivalence and optimization rules of [MLPerf Inference §Model Equivalence](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#model-equivalence). **This document is the source of truth and overrides upstream wherever the two conflict.** Where upstream uses a non-exhaustive list of allowed examples followed by a disallowed list, Endpoints uses a single **disallowed-only** formulation: anything not listed below and not in conflict with the [§2.9 Model Equivalence Rules](#29-model-equivalence-rules-standardized-division) is permitted. See [§2.9.8 Q&A](#298-qa-model-equivalence-clarifications) for clarifying examples.

**Operative requirements:**

- Pre-processing, post-processing, and the model executed by the SUT must be equivalent to the reference implementation, per [§2.9](#29-model-equivalence-rules-standardized-division).
- Submissions must be reproducible: configuration, server launch scripts, and client integration scripts must be submitted. For numerical recipes such as calibration, the submission must either (a) describe the recipe in sufficient detail for an external team to reproduce it, or (b) provide the scripts / software that implement it. The underlying serving framework and low-level software stack must satisfy the **Available** definition in the Submission Rules ([Submission Rules §7.2](endpoints_submission_rules.md#72-available)).
- On-prem (CoP) submissions must be self-contained.

**Disallowed optimizations** (Standardized division):

- Wholesale weight replacement or supplements.
- Discarding non-zero weight elements (pruning), except where the operation is *mathematically equivalent* to the dense reference (see [§2.9.8 Q&A](#298-qa-model-equivalence-clarifications)).
- Knowledge distillation to a different architecture.
- Retraining, fine-tuning, LoRA, adapter layers, RLHF, or any gradient-based weight update — applied to the canonical model or to any draft model used in speculative decoding (see [§2.9.4](#294-speculative-decoding)).
- Response caching: returning a cached response *verbatim* to a request that matches a previous request, bypassing the forward pass. Every request must execute the forward pass. (Note: this is distinct from cross-query KV-cache reuse, which still executes the forward pass on a per-query, salt-uniquified token stream — see [§2.9.5 KV Cache Rules](#295-kv-cache-rules) for the operative rule.)
- Coalescing identical queries (deduplicating duplicate queries in flight to amortize work across them).
- Modifying weights during the timed portion of an inference run (online learning).
- Benchmark detection: the framework or system must not detect a benchmark workload and behave differently.
- Input-based optimization: the submission's *implementation* (the framework, model artifacts, kernels, calibration outputs, and build-time configuration) must not encode any information about the content of the benchmark input dataset. This rule targets static / build-time dataset awareness (e.g., baking dataset statistics into kernel selection, embedding tables, or compile-time constants). It does **not** prohibit *runtime* serving-stack behavior that derives cache keys from the live token stream — KV-cache reuse based on shared prefixes (governed by [§2.9.5 KV Cache Rules](#295-kv-cache-rules)) is permitted, since it operates on the request data rather than on prior knowledge of the dataset.
- Client-side dispatch manipulation: the reference client must not be modified to delay, batch, or reorder the dispatching of queries in order to manipulate TTFT, TPS/User, or other measured metrics. Server-side scheduling of received requests is governed by the normal serving rules and is not constrained by this bullet.
- Modification of the request/response stream outside the reference API specification.
- Weight-quantization algorithms whose specification is similar in size to the non-zero weights they produce (inherited from upstream — defeats principled-quantization intent).
- Hard-coding the total number of queries; techniques that boost performance for fixed-length experiments but are inapplicable to long-running services.

> [!NOTE]
> **Why blacklist-only?** Submitters frequently ask "is X allowed?" for techniques that don't exist yet (new quantization formats, novel kernels, alternative attention impls). A closed whitelist forces a rule change every time. Endpoints maintains a single disallowed list together with the Model Equivalence rules ([§2.9](#29-model-equivalence-rules-standardized-division)); anything not banned and consistent with model equivalence is permitted. The [§2.9.8 Q&A](#298-qa-model-equivalence-clarifications) provides interpretive guidance.

#### 2.2.2 Client over Network (CoN) — Additional Rules

When submitting to the Standardized division via the CoN scenario, the following additional rules apply:

- CoN submitters may choose to submit to CoP instead, but must follow all CoN compliance rules when doing so.
- Servers must not modify incoming or outgoing request/response streams outside the provided MLPerf Endpoints reference API specification.
- The reference client performs all request pre-processing (e.g., tokenization, packing, precision conversion) and all response post-processing (e.g., detokenization, ArgMax, reduction). The SUT executes the model and the reference's serving path only; it does not transform request/response payloads beyond what the reference API specifies.
- Server must not deliberately delay token dispatch to manipulate TTFT or TPS/User metrics.
- Server must not cache responses or requests across queries.

> [!NOTE]
> **[WIP]** — A comprehensive list of allowed techniques and optimizations for the Standardized CoN scenario is under development by the working group.

#### 2.2.3 Result Naming

Unqualified use of "MLPerf Endpoints" refers to results from the Standardized division. Example: *"MLPerf Endpoints result of 5,000 tokens/s at concurrency 64."*

---

### 2.3 Serviced Division

The Serviced division benchmarks publicly available, generally accessible inference-as-a-service endpoints. This is a new division unique to MLPerf Endpoints, designed to benchmark commercial Gen AI API offerings.

**Transparency:** Greybox — the endpoint behavior must be reproducible and auditable, but full internal implementation details need not be disclosed. The API interface, model identity, and pricing must be public.

**Available Scenarios:** Client over Network (CoN) only.

#### 2.3.1 Rules

- The endpoint must be a publicly available, generally accessible commercial service. "Generally accessible" means any customer meeting standard terms of service can obtain access.
- Performance must be reproducible: the endpoint must deliver consistent results when benchmarked at different times within a reasonable window.
- Audit and accuracy tests are required to verify the endpoint produces correct outputs.
- The submitter must disclose: the model name and version as advertised by the service, the API endpoint URL, the pricing model and rates at time of submission, and any rate limits or quotas that apply.
- Serviced submissions may augment the base reference model by pruning, sparsification, quantizing, fine-tuning, modification of speculative decoding heads, and alternative attention mechanisms. Any such augmentations must be disclosed.
- Response caching across queries is not allowed.

**Optimization transparency:**

| Category | Requirement |
|---|---|
| Precision | Required |
| Speculative decode, fusion, changes | Disclosure required (no source code required) |
| Model quantization | Optional |

#### 2.3.2 Result Naming

Results must use the qualified name "MLPerf Endpoints Serviced." Example: *"MLPerf Endpoints Serviced result of 3,200 tokens/s at concurrency 32."*

---

### 2.4 RDI (Research, Development, and Internal) Division

The RDI division provides a category for experimental, pre-release, or internal systems that do not meet Standardized or Serviced requirements. It replaces the traditional "Open" division.

**Transparency:** Blackbox — no audit or compliance tests required. Internal implementation details need not be disclosed.

**Available Scenarios:** Client on Prem (CoP) or Client over Network (CoN). Server may be self-hosted, hybrid, or cloud-hosted. CoP and CoN are not reported as separate sub-divisions.

#### 2.4.1 Rules

- Must use the standard MLPerf Endpoints performance and accuracy datasets.
- Must report the same metrics as Standardized and Serviced divisions (System TPS, TPS/User, TTFT P50/P95) using the same measurement methodology.
- Must use the same base reference model. RDI submissions may augment the model by pruning, sparsification, quantizing, fine-tuning, modification of speculative decoding heads, and alternative attention mechanisms.
- No audit or compliance tests required. No code visibility requirement.
- Submitters must report achieved accuracy on the accuracy dataset.

For RDI publication status and the cooling-off period for RDI hardware transitioning to Available or Preview, see [Submission Rules §7.4](endpoints_submission_rules.md#74-rdi-research-development-or-internal).

#### 2.4.2 Result Naming

Results must use the qualified name "MLPerf Endpoints RDI." Example: *"MLPerf Endpoints RDI result of 8,000 tokens/s at concurrency 128."*

---

### 2.5 Division Summary

| Property | Standardized | Serviced | RDI |
|---|---|---|---|
| Transparency | Whitebox | Greybox | Blackbox |
| Scenarios | CoP, CoN (separate) | CoN only | CoP or CoN (single) |
| Model Equivalence | Required | Augmentation allowed | Augmentation allowed |
| Code Visibility | Full | API-level | None |
| Audit / Compliance | Yes | Yes (audit + accuracy) | No |
| Retraining Allowed | No | Yes (with disclosure) | Yes |
| Public Availability | Not required | Required (GA service) | Not required |

---

### 2.6 Reproducibility Requirements

| Division | By Any 3rd Party (MLC Peer) | On 3rd Party System / Datacenter | On Publicly Available Endpoint |
|---|---|---|---|
| Standardized — CoP | Required | Required | N/A |
| Standardized — CoN | Required | Required | N/A |
| Serviced — CoN | Required | Optional | Required |
| RDI | Optional | Optional | Optional |

- **By Any 3rd Party (MLC Peer):** A review committee member or designated auditor can reproduce the benchmark result using the submitted materials. For Standardized, this means building from provided source code and configurations. For Serviced, this means running the benchmark against the public endpoint.
- **On 3rd Party System / Datacenter:** For Standardized, the submitter must provide containers, drivers, and code sufficient to replicate the setup. For Serviced, this is optional because the endpoint is accessed remotely regardless of client location.
- **On Publicly Available Endpoint:** Only applicable to the Serviced division, where the endpoint must be a generally accessible commercial service.

---

### 2.7 Transparency Requirements

**Source Code**

| Division | Code to Reproduce On-Prem | Code to Reproduce Remote Server |
|---|---|---|
| Standardized — CoP | Required | Required |
| Standardized — CoN | Required | Required |
| Serviced — CoN | N/A | Optional |
| RDI | Optional | Optional |

**Hardware**

| Division | All Rack / Node Hardware | Primary Accelerator Details | Mapping Configurations (TP, EP, PP, Batching) |
|---|---|---|---|
| Standardized — CoP | Required | Required | Required |
| Standardized — CoN | Required | Required | Required |
| Serviced — CoN | Optional | Required | Optional |
| RDI | Required | Required | Optional |

**Hardware details:** accelerator model, count, memory capacity, host CPU/memory, and the interconnect type and topology (e.g., NVLink, InfiniBand, Ethernet, routing layer). For Serviced submissions, full rack hardware disclosure is optional, but the primary accelerator must be identified.

**Software / deployment configuration:** parallelism mapping (e.g., tensor parallelism `TP`, expert parallelism `EP`, pipeline parallelism `PP`, sequence parallelism, data parallelism), batch sizes, scheduling parameters, KV cache configuration, and any other parameters that materially affect throughput or latency. These must be fully disclosed for Standardized division submissions.

---

### 2.8 Tokenizer Rules

Tokenizers can produce different token counts depending on how text is fed to them — the same output text tokenized as a single string versus tokenized as a sequence of streamed chunks can yield different counts, even with the same tokenizer. To ensure consistent and representative measurement across divisions:

- The **reference tokenizer** — defined as the tokenizer published with the benchmarked model in its canonical Hugging Face repository — produces the canonical token count for the system under measurement. All token-count metrics (`system_tps`, `tps_per_user`, etc.) are computed from the reference tokenizer applied to the coalesced output, not from any tokenizer used internally by the SUT.
- **Token counts are obtained by applying the reference tokenizer once to the entire coalesced output** — the full response text reassembled from the submission, tokenized as a single string. Counts are *not* the sum of per-chunk or per-streamed-token counts observed during generation.
  - *Fairness:* every submitter is scored against the same tokenizer applied the same way, independent of how their system batches, chunks, or streams during generation.
  - *Representativeness:* this measures the tokens the user perceives in the final response, rather than implementation artifacts of streamed token boundaries that can differ across submitters.
- Token-count metrics (System TPS, TPS/User) are derived from these coalesced-output counts. TTFT remains a latency measurement (time to receipt of the first output token from the submission, per §5) and is not derived from coalesced counts.
- Submitters using alternative tokenizers must demonstrate equivalence to — or report mapping factors against — the reference tokenizer applied to the coalesced output.

> [!NOTE]
> **[WIP]** — Edge-case handling (e.g., partial Unicode at chunk boundaries, special-token treatment, alternative-tokenizer equivalence criteria, and the definition of "coalesced output" for multi-turn or tool-use responses) is under development by the working group.

---

### 2.9 Model Equivalence Rules (Standardized Division)

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** Endpoints model-equivalence and optimization rules **inherit from** [MLPerf Inference Rules §Model Equivalence](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#model-equivalence). The subsections below restate the inheritance and call out the Endpoints-specific deltas (most notably KV-cache reuse in [§2.9.5](#295-kv-cache-rules) and drafter PTQ in [§2.9.4](#294-speculative-decoding)). Where this section conflicts with upstream, this section is the source of truth for Endpoints submissions.

These rules define what it means for a Standardized division submission to be "model equivalent" to the reference implementation. The accuracy quality target (§4.3) is the ultimate arbiter of model equivalence: a submission that passes the accuracy gate is considered equivalent regardless of internal implementation choices. The rules below define which implementation choices are permitted in reaching that accuracy gate.

#### 2.9.1 Reference Implementation

> [!NOTE]
> **[WIP — align with inference_rules.adoc §reference-implementation]**

Each benchmark has a **reference implementation** published in the MLPerf Endpoints reference repository. The reference implementation defines:

- The canonical model weights and the reference tokenizer (the tokenizer published with the model on Hugging Face).
- The required input and output format.
- The **dataset** used for performance and accuracy runs (Hugging Face dataset ID or download URL, plus the canonical split and any preprocessing recipe).
- The **reference chat template** (Hugging Face chat-template string or the equivalent message-formatting spec). Submissions MUST use the reference chat template; alternative templates that produce different tokenized output are not permitted.
- The **reference server / sampling parameters**: temperature, top-k, top-p, repetition penalty, greedy-vs-stochastic decoding flag, max output tokens, stop sequences. These MUST be set per the benchmark definition; submissions MUST NOT modify them.
- The **speculative-decoding configuration** if the benchmark designates a drafter (drafter ID, precision, algorithm, default per-point configuration). See [§2.9.4](#294-speculative-decoding).
- The accuracy evaluation methodology and quality target.
- The endpoint API interface.

An **alternative reference implementation** may be designated by the working group for a specific architecture or hardware class, subject to passing the same accuracy quality target as the primary reference implementation.

#### 2.9.2 Pre-Processing Equivalence

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division pre-processing rules]**

The server-side processing of each incoming request — both input pre-processing and output post-processing — must be functionally equivalent to the reference implementation:

- **Tokenization:** Must produce the same token IDs as the reference tokenizer for the same input text. Submitters using an alternative tokenizer implementation must demonstrate token-for-token equivalence on the accuracy dataset.
- **Chat template / prompt formatting:** The system prompt, user turn formatting, and special tokens (BOS, EOS, role markers) must match the canonical chat template defined in the benchmark specification. Modifications to the chat template that change the effective input to the model are not permitted.
- **Input truncation:** If the reference implementation truncates inputs that exceed the model's context window, the submitter's truncation method must produce the same result.

#### 2.9.3 Model Weight Rules

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`**

All Standardized division submissions must begin from the **canonical model weights** specified in the benchmark definition (identified by Hugging Face model ID or a published checksum).

Per [§2.2.1](#221-general-rules), weight transformations are governed by the inherited MLPerf Inference rules. The following transformations of the canonical weights are **disallowed**:

- **Block-sparse weight pruning, unstructured pruning, or any operation that discards non-zero weight elements *without* a mathematically equivalent replacement.** Pruning that produces asymptotically equivalent results to a dense reference (e.g., a dense matmul replaced by a sparse matmul that yields the same outputs) inherits the upstream "Replacing dense operations with mathematically equivalent sparse operations" allowance and is *not* a disallowed pruning. See [§2.9.8 Q&A](#298-qa-model-equivalence-clarifications).
- **Fine-tuning, LoRA, adapter layers, RLHF, or any gradient-based update of weights.** Applies equally to the canonical model and to any draft model used in speculative decoding (see [§2.9.4](#294-speculative-decoding)).
- **Retraining from scratch, continued pre-training, or knowledge distillation to a different architecture.**
- **Modifying weights during the timed portion of an inference run** (online learning).
- **Weight-quantization algorithms whose specification is similar in size to the non-zero weights they produce** (inherited from upstream — defeats principled-quantization intent).

#### 2.9.4 Speculative Decoding

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`**

Speculative decoding is permitted for any benchmark whose definition designates a drafter (MTP head, EAGLE-style head, or analogous module). The drafter is treated as part of the canonical reference and is **frozen** in the training sense. The following transformations of the drafter are **disallowed**:

- **Fine-tuning, LoRA, adapter layers, RLHF, or any gradient-based weight update** to the drafter.
- **Continued pre-training or retraining** of the drafter.
- **Swapping the drafter** for a different model — including a different checkpoint of the same family, a smaller checkpoint, or a model trained specifically for benchmark performance.
- **Replacing the speculative-decoding algorithm** with one that differs from the reference (e.g., swapping EAGLE for Medusa).

The following are **also disallowed** at run time:

- **Approximate speculative-decoding methods that alter the output distribution.** The verification step MUST NOT introduce acceptance criteria that would cause the model to accept tokens the target would not have generated. Outputs MUST be token-for-token identical to what the target model would generate without speculation.
- **Approximating, skipping, or replacing the verification step**, including replacing the target with a secondary drafter for verification. The target model in the verification step MUST be the canonical model with the permitted transformations of [§2.9.3](#293-model-weight-rules) applied.

**Disclosure and run-time requirements:**

- The drafter identity (name, version, source URL), precision, algorithm, and per-point configuration MUST be declared in the submission YAML.
- All measurement points on a submission's pareto curve for a given benchmark MUST use the same drafter (same head, same algorithm). Different **configurations** of the same drafter (e.g., varying `speculative-num-steps` or `speculative-eagle-topk`) are permitted across pareto points, including disabling speculation entirely at some points. The drafter itself is fixed across the curve. The configuration values used at each point MUST be declared in the submission YAML, and any dynamic variation within a single point's run MUST be reported as a distribution.

For PTQ on drafter weights, see [§2.9.8 Q&A Q6](#298-qa-model-equivalence-clarifications).

#### 2.9.5 KV Cache Rules

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** This section **intentionally diverges from MLPerf Inference §KV-Cache**, which prohibits cross-query KV reuse. Endpoints targets agentic-style workloads where a shared system prompt across queries is the norm; prohibiting cross-query reuse would force submitters to artificially cripple production-style serving stacks. The salt mechanism in [§2.9.5.1](#2951-salting-mechanism) preserves measurement validity by ensuring caches cannot leak context beyond the system-prompt prefix.

Per [§2.2.1](#221-general-rules), KV-cache management is governed by the inherited MLPerf Inference rules with the Endpoints-specific cross-query-reuse delta described below. The following KV-cache techniques are **disallowed**:

- **Response caching that bypasses the forward pass.** Returning a cached response verbatim to a request that matches a previous request is not permitted. Every request must execute the forward pass. (Cross-query KV-cache reuse — covered by the Endpoints delta below — is *not* response caching: it still executes the forward pass on a salt-uniquified per-query token stream.)
- **KV-cache compression methods that are not in the reference implementation and that have not been disclosed in the submission.** Compression methods that are part of the reference or a designated alternative implementation are permitted by default; submission-specific compression methods are subject to Methodology objections during peer review even after disclosure.

**Endpoints-specific delta — cross-query KV reuse:** Sharing KV cache state across independent requests — including prefix / prompt caching of the shared system prompt — is permitted as a serving optimization, with no requirement of bit-for-bit output identity vs. an un-cached run and no requirement of cross-user partitioning. The performance dataset injects a per-query salt between the shared system prompt and the per-query user context (see [§2.9.5.1](#2951-salting-mechanism)). The salt guarantees that the only prefix two queries can share is the system prompt itself; any KV state derived from the user context cannot be reused across queries with different contexts.

**Disclosure requirements:**

- If the KV cache is stored at reduced precision (e.g., INT8, INT4, FP8 KV), the precision and quantization method MUST be disclosed in the submission YAML.
- Any KV-cache compression method that is not part of the reference implementation MUST be disclosed in the submission YAML.
- Paged / virtual KV cache implementations (e.g., vLLM's PagedAttention) are inherited as permitted under the upstream "Different in-memory representations" allowance and do not require separate disclosure beyond what is already captured in the serving-framework / software-stack disclosure.

##### 2.9.5.1 Salting Mechanism

The performance benchmark workload prepends a unique, deterministic-but-pseudorandom **salt** to each per-query user prompt at request-construction time. The salt:

- **MUST** carry at least 64 bits of entropy per query.
- **MUST** be generated from a seeded pseudo-random sequence (e.g., `random.Random(seed)`) where the seed is declared in the run configuration. This makes the salt sequence reproducible across runs with the same seed while still preventing cross-query KV reuse beyond the system prompt.
- **MUST** be inserted *between* the system prompt and the user-context portion of the prompt, so the system prompt remains a shared prefix across queries (and is therefore cacheable as the legitimate optimization this section permits) while the user-context portion becomes per-query-unique.
- **MUST** be generated at request-construction time, **not** stored in the dataset on disk, so that repeated runs of the same dataset always produce a per-query-unique salt sequence regardless of how many times the dataset is replayed. (Storing salt in the dataset would lose uniqueness across replays — see [endpoints PR #305](https://github.com/mlcommons/endpoints/pull/305) for the reference rationale.)
- **SHOULD** use the reference implementation in `mlcommons/endpoints` (`Dataset.with_salt(random.Random(seed))`, introduced in [endpoints PR #305](https://github.com/mlcommons/endpoints/pull/305)).

How a submitter's client achieves the per-query uniqueness above (e.g., for clients that pre-tokenize prompts) is an **implementation detail** addressed in [§2.9.8 Q&A Q9](#298-qa-model-equivalence-clarifications). The operative requirement is that the token stream actually seen by the SUT contains a unique per-query salt between the system prompt and the user context — not the *means* by which the client constructs that stream.

**Accuracy runs use the un-salted reference dataset** to ensure model output matches the canonical implementation exactly. Submissions are not required to disable cross-query KV reuse in their serving stack for accuracy runs; the accuracy dataset simply omits the salt prefix, and the serving stack reuses KV as it would in production. This split (salted performance dataset, un-salted accuracy dataset) is the operational mechanism that allows blanket cross-query KV reuse without compromising the accuracy gate's role as a model-output check.

> [!NOTE]
> **Backward compatibility note.** This rule intentionally diverges from MLPerf Inference's KV-cache FAQ, which states KV state "does not apply across queries". Endpoints submissions are not portable to standard MLPerf Inference without disabling cross-query KV reuse; conversely, MLPerf Inference submissions that already prohibit cross-query reuse are trivially compliant with this section. Submitters should treat the two rule sets as **not** mutually compatible for code paths that rely on this delta.

#### 2.9.6 Post-Processing Equivalence

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division post-processing rules]**

- **Detokenization.** The response text must be produced by applying the reference detokenizer to the generated token IDs.
- **Stop token handling.** The generation must halt on the same stop tokens and EOS conditions defined in the benchmark specification.
- **Sampling.** For benchmarks using greedy decoding (temperature = 0), the submission must also use greedy decoding. For benchmarks specifying a sampling configuration, the submission must use the same sampling parameters as specified in the benchmark definition.
- **Output stream.** With `stream_all_chunks = true`, every output token must be dispatched to the client as it is generated. Buffering token dispatch is not permitted.

#### 2.9.7 Accuracy Gate

> [!NOTE]
> **[WIP — accuracy tolerance values to be specified per benchmark, aligned with inference_rules.adoc accuracy targets]**

A Standardized division submission passes model equivalence if and only if it meets the **accuracy quality target** defined for the benchmark, evaluated using the reference evaluation methodology on the accuracy dataset. Passing the accuracy gate is necessary and sufficient for model equivalence.

The accuracy quality target and tolerance relative to the reference score are specified per benchmark in the benchmark definition.

#### 2.9.8 Q&A: Model Equivalence Clarifications

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** Q&A entries are interpretive guidance. If a Q&A entry conflicts with the operative rules in §2.2.1 or §2.9.x, the rules take precedence and the Q&A entry will be revised.

**Q1: Is post-training quantization (PTQ) with the published calibration set allowed?**
A: Yes. PTQ is the canonical example of an allowed weight transformation, inherited from upstream. PTQ-style methods (AWQ, GPTQ, bitsandbytes) and arbitrary numerical formats (INT8/INT4/FP8 and similar) are allowed provided they (a) use only the published calibration set, (b) are publicly described to a level where they could be reproduced, (c) pass the accuracy gate, and (d) are disclosed in the submission YAML.

**Q2: Is "mathematically equivalent" sparsification allowed?**
A: Yes. Replacing a dense operation with a sparse operation that produces asymptotically equivalent results is allowed — inherited verbatim from upstream §Model Equivalence. What is disallowed is *pruning*: discarding non-zero weight elements in a way that *alters* the computation.

**Q3: Are mathematically-equivalent attention implementations (Sage Attention, Flash-Attention variants, fused-softmax kernels, Triton rewrites) allowed?**
A: Yes — they are inherited from upstream §Model Equivalence (see [§2.2.1 inheritance clause](#221-general-rules)). Implementations that compute the same output as the canonical attention are permitted. Implementations that *alter* the attention pattern — converting full attention to sparse attention, adding sink tokens not present in the canonical architecture, swapping in a different attention mask, or otherwise changing the pattern the canonical model uses — are not.

**Q4: Is response or query caching allowed?**
A: No. Returning a cached response verbatim to a request that matches a previous request is prohibited. Every request must go through the forward pass. KV-cache reuse (within or across queries) is a *serving optimization* governed by [§2.9.5](#295-kv-cache-rules), **not** response caching — the distinction is that KV-cache reuse still executes the forward pass on per-query tokens (which include a unique salt; see [§2.9.5.1](#2951-salting-mechanism)), whereas response caching skips compute entirely.

**Q5: Is iteration coalescing — the server returning multiple generated tokens in a single network message — allowed?**
A: *Open question.* See [Appendix A](#appendix-a-open-questions-and-working-group-items); the WG is discussing this in the context of Client-over-Network (CoN) scenarios. Until resolved, submitters must disclose any token-coalescing behavior and conservatively assume `stream_all_chunks = true` semantics. Token-count metrics use the reference tokenizer applied to the coalesced output (see [§2.8 Tokenizer Rules](#28-tokenizer-rules)).

**Q6: Is PTQ allowed on the speculative-decoding drafter?**
A: Yes. The drafter weights MAY be post-training quantized using the same rules as the canonical model ([§2.9.3 Model Weight Rules](#293-model-weight-rules)): calibration-only, using only the published calibration set, no gradient updates, must be disclosed, must pass the accuracy gate. The drafter remains *frozen* in every other training-side sense ([§2.9.4](#294-speculative-decoding)) — no fine-tuning, no RLHF, no continued pre-training, no swap for a custom-trained model.

**Q7: Can I use a different serving framework than the reference (vLLM vs. TensorRT-LLM vs. SGLang)?**
A: Yes. Arbitrary frameworks and runtimes are inherited from upstream, provided the framework conforms to the rest of the rules (model equivalence, no benchmark detection, no input-based optimization, etc.). The framework must satisfy the **Available** definition ([Submission Rules §7.2](endpoints_submission_rules.md#72-available)).

**Q8: How does cross-request KV cache sharing interact with the salt mechanism?**
A: See [§2.9.5 KV Cache Rules](#295-kv-cache-rules) and [§2.9.5.1 Salting Mechanism](#2951-salting-mechanism). Cross-request KV sharing is **blanket allowed** in Endpoints (this is the primary delta vs. upstream MLPerf Inference). The performance dataset injects a per-query salt between the shared system prompt and the per-query user context, so the only prefix two queries can share is the system prompt itself. Accuracy runs use the un-salted dataset.

**Q9: How does the salt mechanism apply to clients that pre-tokenize prompts before sending to the SUT?**
A: The operative rule ([§2.9.5.1](#2951-salting-mechanism)) is about the *token stream the SUT sees*, not about a particular client-side text-field implementation. A client that pre-tokenizes (e.g., SGLang-style adapters that send `input_tokens` rather than text) must ensure the *token stream* it sends to the SUT contains the unique per-query salt between the system-prompt tokens and the user-context tokens. Two clean ways to do this: (a) apply the salt to the text and then re-tokenize the result before sending, or (b) reserve a salt-marker token ID (or short sequence) and emit it inline. Applying the salt only to a `prompt` text field while sending the original `input_tokens` will *not* prevent KV reuse — the SUT never sees the text — and is non-compliant. The reference implementation in `mlcommons/endpoints` follows path (a); see the warning logged by `Dataset._apply_salt` in [endpoints PR #305](https://github.com/mlcommons/endpoints/pull/305) for the contract.

---

## 3. Benchmarks and Models

### 3.1 Benchmark Definition

A benchmark in MLPerf Endpoints is defined by a specific model, task, and quality target. Each benchmark has a reference implementation that defines the correct endpoint interface, input/output format, and accuracy evaluation method.

### 3.2 Supported Models

The set of supported benchmark models is defined per submission round and maintained in the MLPerf Endpoints reference repository. The full per-model specification — canonical weights, dataset, chat template, server parameters, accuracy target, and (if applicable) drafter configuration — is given by the [reference implementation](#291-reference-implementation). Each supported model is identified by:

- A Hugging Face model ID (or equivalent checksummed source).
- The task category (text generation, summarization, reasoning, etc.) and the input/output modality (text, token IDs, streaming, non-streaming).

> [!NOTE]
> The model list for each submission round is published in the MLPerf Endpoints reference repository at least 6 weeks before the submission round opens. New models may be proposed to the working group per the benchmark roadmap process defined in the MLPerf General Submission Rules §4.3.

### 3.3 Weight Transformations

Submitters may apply quantization, format conversion, or other weight transformations to the reference weights, subject to the accuracy quality target. All transformations must be documented in the submission. For the Standardized division, the full set of permitted and prohibited transformations is defined in [§2.9.3 Model Weight Rules](#293-model-weight-rules).

---

## 4. Metrics

### 4.1 Primary Metrics

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** TTFT framing — see note below the table on percentile selection.

Each measurement point on the pareto curve captures the following metrics at a specific concurrency level:

| Metric | Symbol | Definition |
|---|---|---|
| System Tokens per Second | `system_tps` | Total output tokens produced per second across all concurrent users. `system_tps = total_output_tokens / elapsed_duration_seconds`. |
| TPS per User | `tps_per_user` | Average output tokens per second experienced by a single user. `tps_per_user = system_tps / concurrency`. |
| Time to First Token (P95) | `ttft_p95_ms` | 95th-percentile time, in milliseconds, from query issuance to receipt of the first output token. |
| Concurrency | `concurrency` | The target number of in-flight concurrent queries for this measurement point. |

> [!NOTE]
> **TTFT percentiles under discussion.** The WG has agreed to use **P95** for the publication plot and as the primary TTFT metric in v0.7. Additional TTFT percentiles (e.g., P50, P99) are under discussion and may be added as a **secondary metrics** table in a later version. Until then, only `ttft_p95_ms` is required to be reported per measurement point; submitters MAY voluntarily report additional percentiles in their submission YAML, but they will not appear on the publication chart for v0.7.

### 4.2 Derived and Presentation Metrics

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`**

The following metrics are derived from primary measurements and used in publication charts. All charts use the percentile metric defined in [§4.1](#41-primary-metrics):

| Metric | Description |
|---|---|
| **Pareto curve (System TPS vs. TPS/User)** | The primary publication chart. **Y-axis:** `system_tps`. **X-axis:** `tps_per_user`. Each point corresponds to a different concurrency level. Represents the fundamental tradeoff between aggregate system capacity and per-user experience. |
| **System TPS vs. Concurrency** | **Y-axis:** `system_tps`. **X-axis:** `concurrency`. Shows aggregate throughput scaling with load. Each point annotated with its region. |
| **TTFT (P95) vs. Concurrency** | **Y-axis:** `ttft_p95_ms`. **X-axis:** `concurrency`. Shows how first-token latency degrades with load. P95 is the default and the only percentile plotted for v0.7; additional percentiles are deferred to a later version (see [§4.1](#41-primary-metrics)). |
| **Interactivity vs. Concurrency** | **Y-axis:** `tps_per_user`. **X-axis:** `concurrency`. Shows how per-user output rate degrades with load. |

### 4.3 Accuracy Metric

Each benchmark defines a quality target expressed as a minimum acceptable score on the benchmark's accuracy metric (e.g., ROUGE score, exact match, perplexity). The accuracy metric and quality target are specified in the benchmark definition.

One accuracy validation run is required per submission (not per measurement point). The same endpoint configuration, model weights, and software stack used for performance runs must be used for the accuracy run.

---

## 5. Pareto Collection Methodology

### 5.1 What Is Measured

Each measurement point on the pareto curve is a benchmark run at a specific concurrency level using the **ConcurrencyScheduler** load pattern in the MLPerf Endpoints reference client. The ConcurrencyScheduler maintains a fixed number of in-flight queries at all times: when a query completes, a new query is immediately issued to maintain the target concurrency.

### 5.2 Pareto Curve Representation

The pareto curve is represented exclusively as a **step-function** plot. Each submitted measurement point defines a discrete step at its concurrency level; between submitted points, the curve holds constant at the last measured value. No interpolation, curve fitting, or smoothing is applied to the official curve.

Visualization tools may optionally overlay interpolated or smoothed curves for readability, but these must be clearly labeled as **"interpolated (not official)"** and must not replace the step-function representation in official publications.

### 5.3 Minimum Submission Requirements

#### Minimum Point Count

Each submission must include a minimum of **7 measurement points**, structured as **1 + 3 + 3**:

| Points | Placement |
|---|---|
| 1 mandatory point | One point in the [Low Latency region](#low-latency-region) (concurrency 1–32). |
| 3 mandatory points | One point in each of the three [Throughput regions](#throughput-regions) (Low Throughput, Medium Throughput, High Throughput). |
| 3 submitter's-choice points | Any concurrency level in any of the four regions, at the submitter's discretion. |

#### No Spacing Requirements

There is no requirement to space points evenly within or across regions. Submitters choose the exact concurrency levels that best characterize their system. This freedom enables submitters to cluster points around inflection points, highlight sweet-spot operating points, or demonstrate consistent performance across a region.

#### Submitter's-Choice Points

The 3 submitter's-choice points may be placed in any of the four regions, including regions that already have a required point. For example, a submitter could place all 3 additional points in the High Throughput region to demonstrate scaling behavior, or distribute them to show overall consistency.

### 5.4 Regions of Interest

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** Regions of Interest (ROIs) are named for either latency or throughput, but in both cases they are constrained by concurrency. Please read the methodology carefully before proceeding.

The concurrency space is divided into four regions.

#### Low Latency Region <a id="low-latency-region"></a>

| Property | Value |
|---|---|
| Concurrency range | 1 to 32 (inclusive), fixed across all submissions. |
| Required points | 1 |

*Rationale:* Low-concurrency operation is critical for interactive applications (chatbots, coding assistants, real-time translation). Fixed boundaries ensure direct cross-submission comparability — every submission has at least one point in the 1–32 range.

> [!NOTE]
> Submitters are encouraged — but not required — to include a measurement at concurrency 1 (the single-user baseline) as their Low Latency point. Concurrency 1 represents the best-case per-user experience and is commonly cited in performance comparisons, but any concurrency level in the 1–32 range satisfies the region requirement.

> [!WARNING]
> **[Subject to WG Review]** — The bounds of the Low Latency region (currently 1–32) are not final and may be adjusted by the working group in a future revision of these rules.

#### Maximum Supported Concurrency

Before the throughput regions can be defined, the submitter must declare a **Maximum Supported Concurrency** value `M`. This is the highest concurrency level at which the submitter chooses to benchmark their system.

Rules:

- `M` must be greater than 32 (otherwise no throughput regions can be defined).
- There is no compliance test to force a particular value of `M`.
- Submitters are incentivized to choose well: `M` defines the extent of their published pareto curve. Declaring too low a value leaves performance on the table; declaring too high a value may produce degraded per-user metrics at the high end.
- The declared `M` defines the upper bound of the High Throughput region.

#### Throughput Regions <a id="throughput-regions"></a>

Beyond the Low Latency region (concurrency > 32), the remaining concurrency space up to `M` is divided into **three equal regions in logarithmic space (base 2)**.

**Region Boundary Computation**

Given a declared Maximum Supported Concurrency `M`, the log-space interval `I` is:

```
I = log2(M - 32) / 3
```

The three throughput regions are:

| Region | Start | End |
|---|---|---|
| Low Throughput | 33 | `round(32 + 2^I)` |
| Medium Throughput | `low_tput_end + 1` | `round(32 + 2^(2*I))` |
| High Throughput | `med_tput_end + 1` | `M` |

All non-integer boundaries are rounded to the nearest integer using **round-half-to-even (banker's rounding)**, consistent with Python's built-in `round()` function used in the reference implementation.

> **Why logarithmic spacing?** Logarithmic spacing reflects how system behavior changes: the difference between concurrency 1 and 10 is far more significant than between 1000 and 1010. Log-space division ensures each region represents a similarly meaningful range of behavioral change, regardless of absolute concurrency scale.

**High Throughput Margin**

The High Throughput region has a **10% margin** beyond `M`, extending the valid upper bound to `ceil(M * 1.10)`.

This margin allows submitters to add points above their initial `M` during the post-submission update window (see [Submission Rules §8.1](endpoints_submission_rules.md#81-pareto-updates)) without requiring a complete redefinition of region boundaries. The margin does not affect the required point distribution.

**Worked Examples**

<details>
<summary><strong>Example A — Large-Scale System (M = 8,192)</strong></summary>

```
I = log2(8192 - 32) / 3 = log2(8160) / 3 = 12.994 / 3 = 4.331

Region boundaries:
  Low Latency:      concurrency    1 –   32  (fixed)
  Low Throughput:   concurrency   33 –   52  (round(32 + 2^4.331) = round(32 + 20.1) = 52)
  Med Throughput:   concurrency   53 –  437  (round(32 + 2^8.663) = round(32 + 405.2) = 437)
  High Throughput:  concurrency  438 – 8192

Minimum 7-point example: {16, 40, 200, 2000, 500, 1000, 4096}
```
</details>

<details>
<summary><strong>Example B — Smaller System (M = 256)</strong></summary>

```
I = log2(256 - 32) / 3 = log2(224) / 3 = 7.807 / 3 = 2.602

Region boundaries:
  Low Latency:     concurrency  1 –  32  (fixed)
  Low Throughput:  concurrency 33 –  38  (round(32 + 2^2.602) = round(32 + 6.1) = 38)
  Med Throughput:  concurrency 39 –  69  (round(32 + 2^5.204) = round(32 + 36.9) = 69)
  High Throughput: concurrency 70 – 256

Minimum 7-point example: {16, 36, 55, 150, 80, 110, 200}
```
</details>

<details>
<summary><strong>Example C — Mid-Range System (M = 1,024)</strong></summary>

```
I = log2(1024 - 32) / 3 = log2(992) / 3 = 9.955 / 3 = 3.318

Region boundaries:
  Low Latency:     concurrency   1 –   32  (fixed)
  Low Throughput:  concurrency  33 –   42  (round(32 + 2^3.318) = round(32 + 10.0) = 42)
  Med Throughput:  concurrency  43 –  131  (round(32 + 2^6.636) = round(32 + 99.4) = 131)
  High Throughput: concurrency 132 – 1024

Minimum 7-point example: {16, 38, 88, 512, 256, 768, 1000}
```
</details>

**Boundary Edge Cases**

- **M ≤ 33:** All three throughput regions collapse to approximately one level each. Submitters with `M ≤ 33` must notify the working group and provide written justification. The working group will review and may request additional information before accepting the submission.
- **M > 100,000:** The algorithm scales correctly. The Low Throughput region will be narrow while the High Throughput region spans most of the range, reflecting the log-scale nature of concurrency scaling.
- **Region boundary collisions:** If rounding causes two boundaries to be equal, the affected region has zero width and a single valid concurrency level at the boundary value. One point at that level satisfies the region's requirement.

### 5.5 Region Boundary Reference Algorithm

The following pseudocode defines the authoritative computation. Submitters must use the reference implementation in the MLCommons Endpoints repository to compute their boundaries and validate their submitted points.

```python
def compute_regions(M: int) -> dict:
    assert M > 32, "Maximum Supported Concurrency must be > 32"

    # Low Latency region (fixed boundaries)
    low_latency = {"start": 1, "end": 32}

    # Compute log-space interval
    I = math.log2(M - 32) / 3

    # Throughput region boundaries (banker's rounding)
    low_tput_end = round(32 + 2**I)
    med_tput_end = round(32 + 2**(2 * I))

    low_throughput  = {"start": 33,              "end": low_tput_end}
    med_throughput  = {"start": low_tput_end+1,  "end": med_tput_end}
    high_throughput = {"start": med_tput_end+1,  "end": M}

    # Extended High Throughput margin (10%)
    margin_end = math.ceil(M * 1.10)

    return {
        "low_latency":      low_latency,
        "low_throughput":   low_throughput,
        "med_throughput":   med_throughput,
        "high_throughput":  high_throughput,
        "margin":           {"start": M+1, "end": margin_end},
    }
```

### 5.6 Maximum Point Cap

At no point shall the total number of measurement points on a single submission's pareto exceed **32 points** (including post-submission additions).

*Rationale:* The 32-point cap balances comprehensive characterization against review burden and result presentation clarity.

---

## 6. Run Requirements Per Measurement Point

> [!WARNING]
> **WORK IN PROGRESS** — This entire section is under active development. Final values will be determined through working group discussion and empirical validation.
> Current constraints, thresholds, and duration values are locked for the v0.7 submission in June 2026 and have been approved by the TaskForce. 

### 6.1 Load Pattern

All measurement points must use the **ConcurrencyScheduler** load pattern in the MLPerf Endpoints reference client. The `target_concurrency` setting specifies the exact concurrency level for each point. Other load patterns (`MaxThroughput`, `Poisson`) are not valid for pareto submission points.

### 6.2 Minimum Run Duration

*(Example values — subject to ratification.)*

Each measurement point must sustain the target concurrency for a minimum duration of steady-state measurement, excluding warmup. These values correspond to the `min_duration_ms` setting in `RuntimeSettings`.

| Concurrency Region | Minimum Duration (steady state) | Rationale |
|---|---|---|
| Low Latency (1–32) | 600 seconds | Reduced duration accounts for slower query completion at low concurrency. |
| Low Throughput | 1200 seconds | Standard duration for statistical confidence at scale. |
| Medium Throughput | 1200 seconds | Standard duration for statistical confidence at scale. |
| High Throughput | 1200 seconds | Standard duration for statistical confidence at scale. |

### 6.3 Warmup Period

*(Requirements below are subject to working group ratification.)*

A warmup period may precede every measurement period. Warmup events — all requests issued before `TEST_STARTED` — are excluded from metric computation. The purpose of warmup is to bring the system to steady state (populated connection pools, warm caches, calibrated scheduler) before any data contributing to reported metrics is collected. The warmup period is optional but must not exceed 24 hours, per measurement point.

#### 6.3.1 Prohibited Warmup Data

Warmup requests must not use any sample from the benchmark performance dataset. This prohibition covers direct use, subsets, truncations, or any query whose content was derived from performance dataset samples.
If the inference client uses benchmark performance dataset, then *salting must be enabled*.

The accuracy dataset and any other data source not drawn from the performance dataset are permitted for warmup.

> [!WARNING]
> For v0.7, the inference client may use performance dataset during warmup. In such case - salting must be enabled. The salting flag is not enabled by default — submitters must manually enable it in the client config and also disable KV cache reuse.

#### 6.3.2 Discard Policy

All requests issued before `TEST_STARTED` are warmup requests and must not appear in any reported metric. Warmup request logs must be retained and available for reviewer inspection.

#### 6.3.3 Documentation Requirements

Beyond the constraints above, warmup is at the submitter's discretion. Because warmup state materially affects the measurement (KV cache population, JIT compilation, scheduler calibration), the full warmup procedure must be documented in sufficient detail for an independent team to reproduce it. Each submission must declare, in the measurement point metadata (see [§8.3](#83-measurement-point-yaml)):

- Total warmup duration (seconds from the first warmup request to `TEST_STARTED`).
- Total warmup requests issued and completed.
- Warmup data source and content description (e.g., dataset name and split, synthetic generation method and parameters, or fixed prompt text).
- Concurrency level used during warmup.
- Any platform-specific initialization steps performed (e.g., CUDA graph capture, engine loading, JIT compilation triggers), and confirmation that initialization was complete before `TEST_STARTED`.

> [!NOTE]
> Reviewers may request warmup logs as part of a reproducibility objection. Incomplete or ambiguous warmup documentation is grounds for a Methodology objection under [Submission Rules §6.8](endpoints_submission_rules.md#68-types-of-objections).

### 6.4 Minimum Completed Queries

*(Example values — subject to ratification.)*

Each measurement point must complete a minimum number of queries (`min_sample_count` in `RuntimeSettings`). The minimum ensures sufficient statistical confidence in the reported percentile metrics.

| Concurrency Region | Minimum Completed Queries | Rationale |
|---|---|---|
| Low Latency (1–32) | One pass over the low-latency dataset | Lower count acceptable given longer run duration. |
| Low Throughput | One pass over the dataset | Consistent and comparable accuracy across all runs. |
| Medium Throughput | One pass over the dataset | Consistent and comparable accuracy across all runs.  |
| High Throughput | One pass over the dataset | Consistent and comparable accuracy across all runs.  |

> [!NOTE]
> These minimum query counts require statistical validation against required sample sizes for target confidence intervals. Values are subject to adjustment pending working group ratification.

### 6.5 Dataset Considerations

*(Example constraints — subject to ratification.)*

- Performance runs use `WithReplacementSampleOrder` (random sampling with replacement from the performance dataset).
- Accuracy runs use `WithoutReplacementSampleOrder` (each sample exactly once).
- For Low Latency region runs, a representative subset of the dataset may be used (configured via `n_samples_from_dataset`) to reduce run time, subject to pre-approval by the working group. The subset must be documented and identical across all submitters.
- `stream_all_chunks` must be set to `true` for all performance runs to enable accurate per-token timing.

### 6.6 Accuracy Requirement

*(Example constraint — subject to ratification.)*

Accuracy validation is required per submission (including per measurement point). The accuracy run verifies that the system meets the benchmark's quality target. The same endpoint configuration, model weights, and software stack used for performance runs must be used for the accuracy run.

---

## 7. Publication Status

Publication status categories — **Available**, **Preview**, and **RDI** — including the four-point availability test, public evidence rules, software stack requirements, the 180-day Preview commitment, the 221-day RDI cooling-off period, and the [CUSTOM-SKU] open question are defined in [MLPerf Endpoints Submission Rules §7](endpoints_submission_rules.md#7-publication).

---

## 8. Submission Requirements

### 8.1 Directory Structure

An Endpoints submission must follow this directory structure:

```
<submitting_organization>/
  systems/
    <system_desc_id>.json
  src/
    <benchmark_model>/
      <endpoint interface code and configuration to reproduce the code>
  pareto/
    <system_desc_id>/
      <benchmark_model>/
        points/
          point_<concurrency_level>.yaml    # one per measurement point, should be generated from the results folder
        results/
          point_<concurrency_level>/
            results_summary.json            # Contains throughput and latency distribution information
            config.yaml                     # Client config
            accuracy/
              results.json                  # Contains accuracy number and truncated output sequences
  documentation/
    calibration.adoc                        # if weight transformations applied
    <additional documentation>
```

### 8.2 System Description (`system_desc_id.json`)

In addition to the standard fields defined in [General Submission Rules §5.7](https://github.com/mlcommons/policies/blob/master/submission_rules.adoc#system_desc_id-json-metadata), Endpoints submissions must include:

| Field | Description |
|---|---|
| `division` | `Standardized`, `Serviced`, or `RDI`. |
| `publication_status` | `Available`, `Preview`, or `RDI`. |
| `benchmark_model` | Benchmark model name (must match supported model list). |
| `max_supported_concurrency` | Declared Maximum Supported Concurrency `M`. |
| `endpoint_url` | URL or description of the endpoint under test. |
| `serving_framework` | Inference serving framework and version (e.g., `vLLM 0.4.0`). |

### 8.3 Measurement Point YAML

Each measurement point must be accompanied by a YAML configuration file specifying:

- `concurrency`: The target concurrency level.
- `region`: The region this point satisfies (`low_latency`, `low_throughput`, `med_throughput`, `high_throughput`, or `submitters_choice`).
- `runtime_settings`: The `RuntimeSettings` used for this run (load pattern, `min_duration_ms`, `min_sample_count`, `stream_all_chunks`, etc.).
- `dataset`: Dataset name and any `n_samples_from_dataset` override (if applicable).
- `warmup`: The warmup procedure declaration required by [§6.3.3](#633-documentation-requirements) — `duration_s`, `requests_issued`, `requests_completed`, `data_source` (description of the warmup data and its origin), `concurrency`, and `initialization_steps` (platform-specific setup completed before `TEST_STARTED`).

### 8.4 Software Disclosure

For **Standardized** and **RDI** division submissions, all software components that substantially determine ML performance must be disclosed. This includes, at minimum:

- Inference serving framework (name, version, commit hash or release tag).
- ML accelerator library (e.g., TensorRT-LLM, cuDNN — version and build).
- Driver version.
- Operating system.

For **Serviced** division submissions, disclose all software information available from public documentation and API metadata.

### 8.5 Result ID

Two identifiers are attached to every submission, and they serve different purposes.

The **submission ID** is generated automatically by the submission pipeline as a hash. It is opaque, carries no meaning, and exists so the lifecycle tooling can track a bundle through upload, review, and amendment.

The **result ID** identifies a single published result and is human-readable. A result is one published Pareto curve: one system, one benchmark model, one dataset. It is constructed as:

```
<major-version>.<minor-version>.<cohort-id>.<model_id>.<dataset_id>.<entry-number>
```

| Component | Description |
|---|---|
| `major-version` | Major version of the MLPerf Endpoints rules under which the result was submitted (e.g., `1` for v1.0). |
| `minor-version` | Minor version of the same (e.g., `0` for v1.0). |
| `cohort-number` | Cohort ID for this submission (e.g., `XXXX-YY-C0`)
| `model_id` | Benchmark model identifier from the round's supported model list ([§3.2](#32-supported-models)). Must match `benchmark_model` in `system_desc_id.json` ([§8.2](#82-system-description-system_desc_idjson)). |
| `dataset_id` | Identifier of the dataset used for the performance and accuracy runs, as named in the benchmark definition ([§3.1](#31-benchmark-definition)) and recorded in each point's `dataset` field ([§8.3](#83-measurement-point-yaml)). |
| `entry-number` | Sequence number assigned at publication, unique within the preceding four components. |

Example: `1.0.deepseek-r1.mmlu-pro.7` — the seventh published DeepSeek-R1 result on MMLU-Pro under the v1.0 rules.

Result IDs are assigned by MLCommons at publication; they are not chosen by the submitter and are not part of the submitted bundle. They are stable and never reused — a result that is superseded, withdrawn, or invalidated retains its result ID in the historical record, and the replacement result receives a new entry number (see [Submission Rules §8.1](endpoints_submission_rules.md#versioning-and-historical-record)).

---

## 9. Compliance Validation

### 9.1 Automated Checks

The compliance validator — run by the submitter before submission and by MLCommons upon receipt — performs the following checks:

| Check | Validation | Failure Action |
|---|---|---|
| **Submission completeness** | All required files, YAML configurations, result artifacts, and system descriptions are present. | Reject submission. |
| **Point count** | ≥ 7 total measurement points. | Reject submission. |
| **Low Latency coverage** | ≥ 1 point with concurrency in [1, 32]. | Reject submission. |
| **Low Throughput coverage** | ≥ 1 point in the Low Throughput region. | Reject submission. |
| **Medium Throughput coverage** | ≥ 1 point in the Medium Throughput region. | Reject submission. |
| **High Throughput coverage** | ≥ 1 point in the High Throughput region. | Reject submission. |
| **Max concurrency declared** | `M > 32`; declared in `system_desc_id.json`. | Reject submission. |
| **Point cap** | ≤ 32 total measurement points. | Reject points beyond 32. |
| **Concurrency in range** | Each point's concurrency falls within a valid region (including the 10% High Throughput margin), computed using the reference algorithm in [§5.5](#55-region-boundary-reference-algorithm). | Flag out-of-range points. |
| **Load pattern** | All points used `ConcurrencyScheduler`. | Reject non-conforming points. |
| **Run duration** | Each point meets the minimum steady-state duration for its region (see [§6.2](#62-minimum-run-duration)). | Flag non-compliant points. |
| **Minimum query count** | Each point meets the minimum completed queries for its region (see [§6.4](#64-minimum-completed-queries)). | Flag non-compliant points. |
| **Streaming config** | `stream_all_chunks = true` for all performance runs. | Flag non-compliant points. |
| **Warmup metadata** | Each point's YAML declares the warmup fields required by [§6.3.3](#633-documentation-requirements) (`duration_s`, `requests_issued`, `requests_completed`, `data_source`, `concurrency`, `initialization_steps`). | Flag non-compliant points. |
| **Warmup logs retained** | Warmup request logs are retained and available for reviewer inspection (see [§6.3.2](#632-discard-policy)). | Flag non-compliant points. |
| **Metric consistency** | `system_tps` derivable from total tokens and elapsed duration; `tps_per_user = system_tps / concurrency`. | Flag inconsistent points. |
| **Accuracy** | At least one accuracy run passes the benchmark quality target. | Reject submission. |
| **Configuration consistency** | Same model, endpoint configuration, and software stack across all measurement points. | Flag inconsistencies. |

### 9.2 Manual Review Focus Areas

Human reviewers should focus on aspects that automation cannot easily verify:

- Whether the pareto curve shape is physically plausible (throughput should generally increase with concurrency up to saturation, then plateau or decrease).
- Whether metric distributions suggest artificial manipulation (e.g., suspiciously uniform TTFT values across very different concurrency levels).
- Whether warmup requests drew on any sample from the performance dataset (prohibited under [§6.3.1](#631-prohibited-warmup-data)); reviewers may cross-check retained warmup logs against the performance dataset.
- Whether the system description accurately reflects the hardware and software used.
- Cross-submission consistency for the same hardware platform.
- Division eligibility (especially Serviced division API compliance and availability status).
- Whether post-submission updates are consistent with the original submission's system configuration.

---

---

## Appendix A: Open Questions and Working Group Items

> [!WARNING]
> **WORK IN PROGRESS** — This appendix collects items that require working group decision before the rules can be finalized. None of the open items below represent current policy; they are placeholders for decisions in progress.

The following items require working group decision before finalization.

### \[RDI-COMP\] Comparability Across Publication Status Categories

**Question:** Should RDI results be directly comparable to Available and Preview results on the same charts?

**Context:** Currently all three categories are plotted together. RDI systems may have unfair advantages (unavailable hardware, prototype software) that make direct comparison misleading.

**Options under consideration:**

1. Display all categories on the same chart with clear visual distinction (current approach).
2. Display RDI on separate charts.
3. Allow submitters to opt in to co-display with Available/Preview.

### \[CUSTOM-SKU\] Production Hardware Not Available for General Purchase

See [§7.4](#74-open-question-custom-sku-classification-custom-sku).

### \[SERVICED-REQ\] Serviced Division Requirements

**Question:** What additional disclosure and reproducibility requirements apply to the Serviced division, given that the submitter does not control the underlying stack?

**Context:** Key open items include: what system description fields are required vs. optional for APIs; how to handle API versioning (the underlying model or serving stack may change without notice); and whether Serviced results should carry a permanent disclaimer about reproducibility.

### \[RUN-REQ\] Run Requirements Ratification

**Question:** What are the ratified values and rules for minimum run duration, minimum query count, dataset subset rules, and the warmup data and documentation requirements ([§6.3](#63-warmup-period))?

**Context:** [§6 Run Requirements](#6-run-requirements-per-measurement-point) currently contains illustrative example values, and the [§6.3](#63-warmup-period) warmup model — submitter discretion plus mandatory disclosure, in place of a fixed warmup duration — is itself pending ratification. All constraints in that section are pending working group ratification based on empirical validation data.

### \[TOK-COUNT\] Coalesced-Output Tokenization and Reported Throughput

**Question:** The reference-tokenizer-on-coalesced-output rule ([§2.8 Tokenizer Rules](#28-tokenizer-rules)) produces token counts that may be ~10–20% lower than what individual serving stacks report as "tokens/second" internally. Have MLC stakeholders and submitter organizations agreed that the published metric will be the coalesced-tokenizer count and not the serving-stack-reported count?

**Context:** Resolution is needed before v0.7 publishes side-by-side comparison charts. The current §2.8 wording (apply reference tokenizer once to the coalesced output) is the proposed rule; the open question is whether stakeholders accept that the published numbers will differ from internal serving-stack-reported numbers by the expected 10–20% margin.

### Division and Scenario Open Items

| Item | Current Proposal | Status |
|---|---|---|
| Allowed techniques for Standardized CoN | Framework defined, details TBD | TBD |
| Tokenizer equivalence rules | Reference tokenizer as canonical; alternative tokenizers must show equivalence on coalesced output | Proposed |
| Serviced division audit procedures | Required, details TBD | TBD |
| Caching rules for Serviced division | Not allowed across queries | Proposed |
| Response stream modification rules | Not allowed outside reference API | Proposed |
| Future division for new models/datasets | To be determined by WG | TBD |
| Fabric vs. bus restrictions (Standardized CoN) | Not imposed (borrowed from Network Division) | Proposed |
| Batch/chunk tokenizer variability | Apply reference tokenizer once to the entire coalesced output (not per-chunk) for all token-count metrics | Proposed |

---

## Appendix B: Quick-Reference Region Boundary Table

Pre-computed region boundaries for common Maximum Supported Concurrency values using the reference algorithm (Low Latency fixed at 1–32).

| Max Concurrency (M) | Low Latency | Low Throughput | Medium Throughput | High Throughput | 10% Margin |
|---|---|---|---|---|---|
| 64 | 1–32 | 33–35 | 36–42 | 43–64 | 65–71 |
| 128 | 1–32 | 33–37 | 38–53 | 54–128 | 129–141 |
| 256 | 1–32 | 33–38 | 39–69 | 70–256 | 257–282 |
| 512 | 1–32 | 33–40 | 41–93 | 94–512 | 513–564 |
| 1,024 | 1–32 | 33–42 | 43–131 | 132–1,024 | 1,025–1,127 |
| 2,048 | 1–32 | 33–45 | 46–192 | 193–2,048 | 2,049–2,253 |
| 4,096 | 1–32 | 33–48 | 49–287 | 288–4,096 | 4,097–4,506 |
| 8,192 | 1–32 | 33–52 | 53–437 | 438–8,192 | 8,193–9,012 |
| 16,384 | 1–32 | 33–57 | 58–676 | 677–16,384 | 16,385–18,023 |

*All boundaries computed using the reference algorithm in [§5.5](#55-region-boundary-reference-algorithm) with banker's rounding. The Low Latency region has fixed boundaries across all submissions; all other region boundaries are submission-specific and depend on the declared `M`.*
