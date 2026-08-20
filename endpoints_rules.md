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
  The seeded RNG check uses the submission's **bound seed set**, selected from the sets MLCommons made available for the submission's target cohort ([Submission Rules §4.6](endpoints_submission_rules.md#46-seed-rotation)); the client's request-issue / sample-order RNG and the per-query salt MUST each be seeded from that set, and the seed set MUST be set through the YAML configuration.
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

**Inheritance.** Standardized division submissions inherit the model-equivalence and optimization rules of [MLPerf Inference §Model Equivalence](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#model-equivalence). **This document is the source of truth and overrides upstream wherever the two conflict.** Where upstream uses a non-exhaustive list of allowed examples followed by a disallowed list, Endpoints uses a single **disallowed-only** formulation: anything not listed below and not in conflict with the [§2.9 Model Equivalence Rules](#29-model-equivalence-rules-standardized-division) is permitted. See [§2.9.6 Sparsity and Approximate Computation](#296-sparsity-and-approximate-computation) for the treatment of sparse and approximate execution, and [§2.9.9 Q&A](#299-qa-model-equivalence-clarifications) for clarifying examples.

**Operative requirements:**

- Pre-processing, post-processing, and the model executed by the SUT must be equivalent to the reference implementation, per [§2.9](#29-model-equivalence-rules-standardized-division).
- Submissions must be reproducible: configuration, server launch scripts, and client integration scripts must be submitted. For numerical recipes such as calibration, the submission must either (a) describe the recipe in sufficient detail for an external team to reproduce it, or (b) provide the scripts / software that implement it. The underlying serving framework and low-level software stack must satisfy the **Available** definition in the Submission Rules ([Submission Rules §7.2](endpoints_submission_rules.md#72-available)).
- On-prem (CoP) submissions must be self-contained.

**Disallowed optimizations** (Standardized division):

- Wholesale weight replacement or supplements.
- Discarding non-zero weight elements (pruning), except where the operation is *mathematically equivalent* to the dense reference (see [§2.9.6.2](#2962-exact-sparse-execution-and-softmax-elision)).
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
> **Why blacklist-only?** Submitters frequently ask "is X allowed?" for techniques that don't exist yet (new quantization formats, novel kernels, alternative attention impls). A closed whitelist forces a rule change every time. Endpoints maintains a single disallowed list together with the Model Equivalence rules ([§2.9](#29-model-equivalence-rules-standardized-division)); anything not banned and consistent with model equivalence is permitted. The [§2.9.9 Q&A](#299-qa-model-equivalence-clarifications) provides interpretive guidance.

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
- Must report the same metrics as Standardized and Serviced divisions (System TPS, TPS/User, TTFT P50/P90) using the same measurement methodology.
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

- The **reference tokenizer** — defined as the tokenizer published with the benchmarked model in its canonical Hugging Face repository — produces the canonical token count for the system under measurement. Complete-response token-count metrics such as `system_tps` are computed from the reference tokenizer applied to the fully reconstructed assistant response through the benchmark model's official reference chat template, not from any tokenizer used internally by the SUT.
- **Complete-response token counts are obtained by applying the reference tokenizer once per completed assistant response.** Visible-output and reasoning fragments are reassembled in arrival order, while tool-call fragments are reassembled by tool-call list index as defined below. The reconstructed visible output, reasoning, and structured tool calls are supplied together as one assistant message to the official reference chat template and tokenized once. Counts are *not* the sum of per-chunk or per-streamed-token counts observed during generation.
  - *Fairness:* every submitter is scored against the same tokenizer applied the same way, independent of how their system batches, chunks, or streams during generation.
  - *Representativeness:* this measures the benchmark model's canonical representation of the completed assistant response, rather than implementation artifacts of streamed token boundaries that can produce different token counts across submitters.

**Input sequence length (ISL).** For each request, the reference client first applies all benchmark-required input preprocessing, including request construction, salting where required, and the benchmark model's official reference chat template. The fully preprocessed input is then tokenized with the reference tokenizer using the generation-prompt and special-token behavior defined by the reference implementation. If the reference implementation truncates the tokenized input, ISL is the length after that truncation. This sequence replicates the input tokenization expected on the server side; special tokens inserted by the reference chat template are included in ISL. Where model-equivalence rules apply, a submitter may use a different implementation only if it produces the same effective prompt and token IDs. The generated benchmark report includes ISL statistics computed from these per-request values.

**Response categories and what is counted.** A model response can carry three kinds of content — user-visible **output**, **tool-call** content, and **reasoning** (thinking) traces. Serving frameworks convert the raw generation into structured OpenAI chat-completion objects received by the reference client. For visible output and reasoning, the client concatenates all text fragments in arrival order. Tool calls are reassembled into structured objects by list index as described below. The client supplies all three reconstructed fields together as one assistant message to the benchmark model's official reference chat template and tokenizes the rendered message once.

Category assignment is mutually exclusive: the reference client MUST assign each received text fragment to exactly one response field, and a fragment MUST NOT contribute more than once to the reconstructed assistant message. Deliberately duplicating substantially identical content across fields, or adding padding content to any field, for the purpose of increasing reported token counts is prohibited and invalidates the affected measurement point.

For parallel tool calls, the client maintains a list keyed by the tool-call index supplied by the response protocol. Function-argument fragments are appended in arrival order within their corresponding index; the protocol-provided call ID, type, and function name are retained. After the response completes, the structured tool calls are ordered by ascending list index. If `function.arguments` is a JSON string encoding an object, the client parses it to that object for the reference chat template; otherwise, it preserves the received value. If the transport provides separate streams for parallel tool calls, each stream is reassembled independently before the completed calls are ordered. The resulting structured tool-call list is supplied, together with assistant visible output and reasoning, to the official reference chat template.

The assistant-payload token count excludes empty chat-template framing. The reference client renders and tokenizes both (a) a minimal reference conversation containing an empty user message followed by the reconstructed assistant response and (b) the same conversation with an empty assistant message. The official output-token count is `max(0, count(a) - count(b))`. Both renders use `add_generation_prompt = false`. Tokens introduced specifically to represent the reconstructed assistant payload, including model-defined reasoning or tool-call framing, are counted; framing already present for an empty assistant message is not.

| Content category | Counted? | How it is measured |
|---|---|---|
| Visible output | Yes | Text fragments concatenated in arrival order and supplied as assistant `content` |
| Tool-call content | Yes | Fragments reassembled into structured calls, ordered by ascending tool-call index, and supplied as assistant `tool_calls` |
| Reasoning / thinking | Yes | Text fragments concatenated in arrival order and supplied as the assistant reasoning field expected by the reference chat template |
| Chat-template framing / special tokens | Conditional | Payload-specific reasoning and tool-call framing inserted by the official reference chat template is counted; framing present for an empty assistant message is excluded by the baseline subtraction above |

- Because frameworks differ in their internal serialization, the reconstructed assistant message may not be byte-identical to the server's raw generation. Rendering the received structured response with the official reference chat template provides one model-specific, reproducible representation for scoring every submitter.
- Complete-response token-count metrics such as System TPS are derived from this single assistant-payload count. TPOT instead uses the suffix after the first output-bearing streamed chunk; that suffix is tokenized once with the reference tokenizer, and non-positive or non-finite samples and non-streaming responses are excluded. TTFT remains a latency measurement and is not derived from token counts: it is measured from query issuance until the client receives the first non-empty text fragment (`len(s) > 0`) in any response category (visible-output, tool-call, or reasoning).
- Submitters may use any tokenizer internally for output generation or accounting; that output-side choice does not affect scoring. The official output-token count is always produced by the **client-side reference tokenizer applied once to the reconstructed assistant message through the official reference chat template**. No equivalence demonstration or mapping factor is required for an internal output tokenizer. This output-scoring rule does not waive the input tokenization and preprocessing equivalence requirements in [§2.9.2](#292-pre-processing-equivalence).

> [!NOTE]
> **[WIP]** — One edge case remains under working-group development: partial Unicode at chunk boundaries.

---

### 2.9 Model Equivalence Rules (Standardized Division)

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** Endpoints model-equivalence and optimization rules **inherit from** [MLPerf Inference Rules §Model Equivalence](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#model-equivalence). The subsections below restate the inheritance and call out the Endpoints-specific deltas (most notably KV-cache reuse in [§2.9.5](#295-kv-cache-rules), dynamic approximate sparsity in [§2.9.6.4](#2964-dynamic-approximate-sparsity), and drafter PTQ in [§2.9.4](#294-speculative-decoding)). Where this section conflicts with upstream, this section is the source of truth for Endpoints submissions.

These rules define what it means for a Standardized division submission to be "model equivalent" to the reference implementation. The subsections below define which implementation choices are permitted; the accuracy quality target (§4.3) then determines whether a permitted approximation is acceptable in a given submission. Passing the accuracy gate is necessary but not sufficient — see [§2.9.8](#298-accuracy-gate).

#### 2.9.1 Reference Implementation

> [!NOTE]
> **[WIP — align with inference_rules.adoc §reference-implementation]**

Each benchmark has a **reference implementation** published in the MLPerf Endpoints reference repository. The reference implementation defines:

- The canonical model weights and the reference tokenizer (the tokenizer published with the model on Hugging Face).
- The **canonical attention pattern**, including any architecture-native sparsity configuration — block size, token-selection rule, local/global window structure, and any learned or heuristic selection module — where the canonical architecture specifies sparse attention. See [§2.9.6.3](#2963-canonical-architectural-sparsity).
- The required input and output format.
- The **dataset** used for performance and accuracy runs (Hugging Face dataset ID or download URL, plus the canonical split and any preprocessing recipe).
- The **reference chat template** (Hugging Face chat-template string or the equivalent message-formatting spec). Submissions MUST use the reference chat template; alternative templates that produce different tokenized output are not permitted.
- The **reference server / sampling parameters**: temperature, top-k, top-p, repetition penalty, greedy-vs-stochastic decoding flag, max output tokens, stop sequences. These MUST be set per the benchmark definition; submissions MUST NOT modify them.
- The **speculative-decoding configuration** if the benchmark designates a drafter (drafter ID, precision, algorithm, default per-point configuration). See [§2.9.4](#294-speculative-decoding).
- The accuracy evaluation methodology and quality target.
- The endpoint API interface.
- **Fixed configuration:** Configuration parameters explicitly designated as fixed by the reference implementation MUST NOT be modified by submitters.

An **alternative reference implementation** may be designated by the working group for a specific architecture or hardware class, subject to passing the same accuracy quality target as the primary reference implementation.

#### 2.9.2 Pre-Processing Equivalence

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division pre-processing rules]**

The server-side processing of each incoming request — both input pre-processing and output post-processing — must be functionally equivalent to the reference implementation:

- **Tokenization:** Must produce the same token IDs as the reference tokenizer for the same input text. Submitters using an alternative tokenizer implementation must demonstrate token-for-token equivalence on the accuracy dataset.
- **Chat template / prompt formatting:** The system prompt, user turn formatting, special tokens (BOS, EOS, role markers), and chat-template flags must match the benchmark specification. Modifications that change the effective input to the model are not permitted.
- **Input truncation:** If the reference implementation truncates inputs that exceed the model's context window, the submitter's truncation method must produce the same result.

#### 2.9.3 Model Weight Rules

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`**

All Standardized division submissions must begin from the **canonical model weights** specified in the benchmark definition (identified by Hugging Face model ID or a published checksum).

Per [§2.2.1](#221-general-rules), weight transformations are governed by the inherited MLPerf Inference rules. The following transformations of the canonical weights are **disallowed**:

- **Block-sparse weight pruning, unstructured pruning, or any operation that discards non-zero weight elements *without* a mathematically equivalent replacement.** Pruning that produces mathematically equivalent results to a dense reference (e.g., a dense matmul replaced by a sparse matmul that yields the same outputs) inherits the upstream "Replacing dense operations with mathematically equivalent sparse operations" allowance and is *not* a disallowed pruning. See [§2.9.6.2](#2962-exact-sparse-execution-and-softmax-elision).
- **Fine-tuning, LoRA, adapter layers, RLHF, or any gradient-based update of weights.** Applies equally to the canonical model and to any draft model used in speculative decoding (see [§2.9.4](#294-speculative-decoding)).
- **Retraining from scratch, continued pre-training, or knowledge distillation to a different architecture.**
- **Modifying weights during the timed portion of an inference run** (online learning).
- **Weight-quantization algorithms whose specification is similar in size to the non-zero weights they produce** (inherited from upstream — defeats principled-quantization intent).

**Post-training quantization (PTQ).** PTQ is the canonical *permitted* weight transformation, inherited from upstream. PTQ-style methods (AWQ, GPTQ, bitsandbytes) and arbitrary numerical formats (INT8/INT4/FP8 and similar) are permitted provided they (a) use only the published calibration set, (b) are publicly described to a level at which they could be reproduced, (c) pass the accuracy gate ([§2.9.8](#298-accuracy-gate)), and (d) are disclosed in the submission YAML. The same conditions govern PTQ applied to a speculative-decoding drafter ([§2.9.4](#294-speculative-decoding)).

Submitters may either derive a quantized checkpoint from the reference checkpoint using only the MLPerf-provided calibration data set, or use a publicly available checkpoint pre-approved by the MLPerf Endpoints Rules Task Force or Working Group. 

**Components of the canonical checkpoint.** Permitted weight transformations MUST preserve the component set of the canonical checkpoint. A submission's derived checkpoint — quantized or otherwise transformed — MUST contain every component the reference checkpoint ships, including auxiliary prediction heads and speculative-decoding modules such as MTP or EAGLE-style heads. **Stripping such a component from the derived checkpoint is not permitted**, even where the component does not participate in producing output and even where the submission does not intend to use it. The derived checkpoint must remain a faithful transformation of the canonical one, so that reviewers can verify provenance against the published model ID or checksum and, where applicable, re-run the submission with the component enabled.

Declining to *use* a component at run time is a separate matter, governed by [§2.9.4](#294-speculative-decoding): a submission MAY disable speculative decoding at some or all measurement points, provided the drafter remains present in the submitted checkpoint and the per-point configuration is declared in the submission YAML.

Statically removing weights that *do* participate in the forward pass for some inputs is pruning, and is disallowed above and in [§2.9.6.5](#2965-disallowed).

> [!NOTE]
> **[WG Open Item — `[CKPT-RESIDENCY]`]** — **TODO:** this rule governs the checkpoint *artifact*. Whether a component present in the checkpoint must also be **resident in accelerator memory** during measurement is undecided, and the memory freed by not loading it is a measurable performance advantage. See [Appendix A \[CKPT-RESIDENCY\]](#ckpt-residency-checkpoint-component-residency).

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

**PTQ on drafter weights.** The drafter weights MAY be post-training quantized under the same conditions as the canonical model ([§2.9.3](#293-model-weight-rules)): calibration-only, using only the published calibration set, no gradient updates, disclosed in the submission YAML, and subject to the accuracy gate. The drafter remains *frozen* in every other training-side sense.

**Leaving the drafter unused.** A submission is not required to load or use a drafter shipped with the canonical checkpoint; see [§2.9.3](#293-model-weight-rules). Where a benchmark's reference implementation does not designate a drafter ([§2.9.1](#291-reference-implementation)), speculative decoding is not available for that benchmark at all — a drafter shipped with the model but not designated by the benchmark definition may not be used.

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

The operative requirement is that the token stream actually seen by the SUT contains a unique per-query salt between the system prompt and the user context — not the *means* by which the client constructs that stream.

**Clients that pre-tokenize.** A client that pre-tokenizes prompts (e.g., SGLang-style adapters that send `input_tokens` rather than text) MUST ensure the *token stream* it sends to the SUT contains the unique per-query salt between the system-prompt tokens and the user-context tokens. Two conforming approaches: (a) apply the salt to the text and re-tokenize the result before sending, or (b) reserve a salt-marker token ID (or short sequence) and emit it inline. Applying the salt only to a `prompt` text field while sending the original `input_tokens` will *not* prevent KV reuse — the SUT never sees the text — and is non-compliant. The reference implementation in `mlcommons/endpoints` follows path (a); see the warning logged by `Dataset._apply_salt` in [endpoints PR #305](https://github.com/mlcommons/endpoints/pull/305) for the contract.

For agentic benchmarks, benchmark-defined trajectory-aware salting supersedes this subsection's per-query and un-salted-accuracy requirements. Submitters MUST enable and use it without modification; Agentic Inference requires `agentic_inference.enable_salt: true`.

**Accuracy runs use the un-salted reference dataset** to ensure model output matches the canonical implementation exactly. Submissions are not required to disable cross-query KV reuse in their serving stack for accuracy runs; the accuracy dataset simply omits the salt prefix, and the serving stack reuses KV as it would in production. This split (salted performance dataset, un-salted accuracy dataset) is the operational mechanism that allows blanket cross-query KV reuse without compromising the accuracy gate's role as a model-output check.

> [!NOTE]
> **Backward compatibility note.** This rule intentionally diverges from MLPerf Inference's KV-cache FAQ, which states KV state "does not apply across queries". Endpoints submissions are not portable to standard MLPerf Inference without disabling cross-query KV reuse; conversely, MLPerf Inference submissions that already prohibit cross-query reuse are trivially compliant with this section. Submitters should treat the two rule sets as **not** mutually compatible for code paths that rely on this delta.

#### 2.9.6 Sparsity and Approximate Computation

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** This section consolidates the Endpoints treatment of sparse execution, softmax elision, and runtime approximation. It **intentionally diverges from MLPerf Inference**, which admits only mathematically equivalent sparse operations: [§2.9.6.4](#2964-dynamic-approximate-sparsity) permits bounded runtime approximation under the accuracy gate.

##### 2.9.6.1 Scope and Operative Test

This section governs techniques that skip, elide, or approximate part of the computation at run time — sparse execution paths, softmax elision, attention-score thresholding, and activation thresholding. It does not govern transformations of the stored weights, which remain subject to [§2.9.3](#293-model-weight-rules).

The operative test throughout is whether the technique **changes the tokens the model emits for any input**:

- Techniques that provably do not are permitted without exception ([§2.9.6.2](#2962-exact-sparse-execution-and-softmax-elision), [§2.9.6.3](#2963-canonical-architectural-sparsity)).
- Techniques that may are permitted only under [§2.9.6.4](#2964-dynamic-approximate-sparsity): they must pass the accuracy gate and be disclosed.
- Techniques that change the model's structure rather than approximating its computation are disallowed ([§2.9.6.5](#2965-disallowed)).

Whether a technique is implemented in software or accelerated by hardware is not a criterion. Sparse tensor cores, block-sparse kernels, and gather/scatter dispatch are implementation choices governed by what they compute, not by which units execute them; they are permitted on the same basis as arbitrary frameworks and kernels ([§2.2.1](#221-general-rules)) and the upstream "different in-memory representations" allowance inherited in [§2.9.5](#295-kv-cache-rules). Neither the sparsity ratio achieved at run time nor the hardware's supported sparsity granularity is itself a compliance criterion.

##### 2.9.6.2 Exact Sparse Execution and Softmax Elision

The following are mathematically equivalent to the reference computation. They are permitted with no exception and no disclosure beyond the software-stack listing of [§8.4](#84-software-disclosure):

- **Mathematically equivalent sparse operations.** Replacing a dense operation with a sparse operation that produces the same outputs — for example a dense matmul executed as a sparse matmul, or skipping blocks whose values are exactly zero. Inherited from upstream §Model Equivalence.
- **Fused, streaming, and online softmax.** FlashAttention-style running max/sum, fused softmax kernels, log-sum-exp rearrangement, and max-subtraction for numerical stability.
- **Vocabulary softmax elision under greedy decoding.** Softmax is monotonic, so `argmax(softmax(logits)) == argmax(logits)`. Where the benchmark's reference sampling configuration is greedy (temperature = 0, per [§2.9.7](#297-post-processing-equivalence)), taking argmax over raw logits and skipping normalization entirely is exactly equivalent.
- **Softmax elision in speculative-decoding verification** where the target's sampling configuration is greedy, since acceptance reduces to comparing argmax.

Bit-exact identity is not required — ordinary floating-point reassociation is expected.

##### 2.9.6.3 Canonical Architectural Sparsity

Where the canonical architecture is itself sparse, implementing that sparsity is **required** for equivalence rather than being a disallowed transformation. The reference point is the canonical model's own computation, not a dense idealization of it.

- **Native sparse attention.** Architectures that specify sparse attention in the reference architecture define the pattern submissions must implement, including its sparsity configuration ([§2.9.1](#291-reference-implementation)). Substituting a different structural sparse pattern for the canonical one is disallowed under [§2.9.6.5](#2965-disallowed) even where the canonical model is itself sparse.
- **Canonical sparse routing.** Where the architecture activates a subset of weights per token by design — for example a mixture-of-experts model routing each token to a fraction of its experts — touching only the routed weights on a given forward pass *is* the canonical computation. That the majority of expert weights go untouched on any individual token is not grounds for an objection.

##### 2.9.6.4 Dynamic Approximate Sparsity

Sparsity derived at run time from live attention scores or activations is permitted in the Standardized division even where it does not preserve outputs exactly. This is an Endpoints-specific delta from upstream. It covers:

- **Attention-score thresholding.** Within the online-softmax loop, a key/value block whose local maximum score falls more than `ln(λ)` below the running maximum is treated as contributing negligible post-softmax mass, and that block's exponential, value-block load from HBM, and attention-weight × value product are skipped. The reference technique is softmax thresholding as described in BLASST ([arXiv:2512.12087](https://arxiv.org/abs/2512.12087)).
- **Activation thresholding.** Skipping computation because an activation block falls below a magnitude threshold. Skipping computation because an activation block is exactly zero is instead governed by [§2.9.6.2](#2962-exact-sparse-execution-and-softmax-elision).

Methods in this category are subject to all of the following:

- They MUST pass the benchmark's accuracy quality target on the un-salted accuracy dataset. The accuracy gate ([§2.9.8](#298-accuracy-gate)) is the arbiter of whether the approximation is acceptable.
- They MUST NOT be calibrated on the benchmark performance or accuracy dataset. Threshold selection must use the published calibration set or a data-independent procedure; calibrating against benchmark inputs is input-based optimization and is disallowed under [§2.2.1](#221-general-rules).
- They MUST be disclosed per [§2.9.6.6](#2966-disclosure).
- They apply to the computation only. This allowance does not license discarding weight elements; weight transformations remain governed by [§2.9.3](#293-model-weight-rules).

**Interaction with speculative decoding.** Where the target model uses an approximate method under this section, the token-for-token identity requirement of [§2.9.4](#294-speculative-decoding) is evaluated against the submission's own target-model configuration: the drafter and verification step must introduce no divergence beyond the disclosed approximation.

##### 2.9.6.5 Disallowed

- **Structural attention-pattern changes.** Adding sink tokens not present in the canonical architecture, swapping in a different attention mask, imposing a fixed or precomputed sparsity pattern on a canonically dense attention layer, substituting a different structural sparse pattern for the canonical one, or otherwise changing the pattern the canonical model uses. Dynamic score-derived sparsity is governed by [§2.9.6.4](#2964-dynamic-approximate-sparsity) and is not a structural change.
- **Normalization substitution.** Replacing softmax with a different normalization not present in the canonical architecture (e.g. linear or ReLU attention) — an architecture substitution rather than an approximation of the canonical attention.
- **Weight-side sparsity to reach a hardware sparse path.** Pruning, zeroing, or restructuring weights — for example imposing a 2:4 or block-structured pattern — in order to use sparse hardware. Dense weights MAY be dispatched through a sparse kernel; the weights themselves must remain dense. See [§2.9.3](#293-model-weight-rules).
- **Static removal of weights from the checkpoint.** Dropping experts, layers, or any other weights that participate in the forward pass for some inputs — including experts that are rarely routed to — whether or not the resulting submission passes the accuracy gate. The distinction from [§2.9.6.3](#2963-canonical-architectural-sparsity) is static versus dynamic: canonical routing decides per token at run time; removing an expert from the checkpoint decides once, for every token. Components that do *not* participate in the forward pass, such as speculative-decoding heads, may likewise not be stripped from the derived checkpoint — see [§2.9.3](#293-model-weight-rules).
- **Softmax elision where the reference sampling configuration is stochastic** (temperature > 0, top-p, top-k), since sampling depends on the normalized probabilities.
- **Softmax elision where the response returns token logprobs or probabilities**, unless those values are computed exactly as the reference would.

##### 2.9.6.6 Disclosure

Techniques permitted under [§2.9.6.4](#2964-dynamic-approximate-sparsity) MUST be declared in the submission YAML:

| Field | Requirement |
|---|---|
| Method and source | The technique and its paper or implementation reference. |
| Threshold parameter | The threshold or target-sparsity value (e.g. `λ`). |
| Calibration procedure | How the threshold was selected, and the data used to select it. |
| Per-point value | The value in force at each measurement point. |
| Schedule or distribution | Required where the threshold varies with context length or varies dynamically within a run. |

Techniques permitted under [§2.9.6.2](#2962-exact-sparse-execution-and-softmax-elision) and [§2.9.6.3](#2963-canonical-architectural-sparsity) require no disclosure beyond the software-stack listing of [§8.4](#84-software-disclosure).

#### 2.9.7 Post-Processing Equivalence

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division post-processing rules]**

- **Detokenization.** The response text must be produced by applying the reference detokenizer to the generated token IDs.
- **Stop token handling.** The generation must halt on the same stop tokens and EOS conditions defined in the benchmark specification.
- **Sampling.** For benchmarks using greedy decoding (temperature = 0), the submission must also use greedy decoding. For benchmarks specifying a sampling configuration, the submission must use the same sampling parameters as specified in the benchmark definition.
- **Output stream.** With `stream_all_chunks = true`, every output token must be dispatched to the client as it is generated. Buffering token dispatch is not permitted.

#### 2.9.8 Accuracy Gate

> [!NOTE]
> **[WIP — accuracy tolerance values to be specified per benchmark, aligned with inference_rules.adoc accuracy targets]**

A Standardized division submission meets model equivalence only if it meets the **accuracy quality target** defined for the benchmark, evaluated using the reference evaluation methodology on the accuracy dataset. Passing the accuracy gate is **necessary** for model equivalence, and it is the arbiter of whether an approximation these rules permit — such as those in [§2.9.6.4](#2964-dynamic-approximate-sparsity) — is acceptable in a given submission.

Passing the accuracy gate is **not a general override**. A submission that meets the quality target while violating an operative rule of [§2.2.1](#221-general-rules) or §2.9.x — for example by pruning weights ([§2.9.3](#293-model-weight-rules)), removing experts from the checkpoint ([§2.9.6.5](#2965-disallowed)), or fine-tuning a drafter ([§2.9.4](#294-speculative-decoding)) — is not model equivalent.

The accuracy quality target and tolerance relative to the reference score are specified per benchmark in the benchmark definition.

#### 2.9.9 Q&A: Model Equivalence Clarifications

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`** Q&A entries are interpretive guidance. If a Q&A entry conflicts with the operative rules in §2.2.1 or §2.9.x, the rules take precedence and the Q&A entry will be revised.

**Q1: Is response or query caching allowed?**
A: No. Returning a cached response verbatim to a request that matches a previous request is prohibited. Every request must go through the forward pass. KV-cache reuse (within or across queries) is a *serving optimization* governed by [§2.9.5](#295-kv-cache-rules), **not** response caching — the distinction is that KV-cache reuse still executes the forward pass on per-query tokens (which include a unique salt; see [§2.9.5.1](#2951-salting-mechanism)), whereas response caching skips compute entirely.
The salt is itself part of the submission's **bound seed set** ([Submission Rules §4.6](endpoints_submission_rules.md#46-seed-rotation)), so it changes when MLCommons refreshes the seed set every two cohorts.

**Q2: Is iteration coalescing — the server returning multiple generated tokens in a single network message — allowed?**
A: *Open question.* See [Appendix A](#appendix-a-open-questions-and-working-group-items); the WG is discussing this in the context of Client-over-Network (CoN) scenarios. Until resolved, submitters must disclose any token-coalescing behavior and conservatively assume `stream_all_chunks = true` semantics. Token-count metrics use the reference tokenizer applied to the coalesced output (see [§2.8 Tokenizer Rules](#28-tokenizer-rules)).

**Q3: Can I use a different serving framework than the reference (vLLM vs. TensorRT-LLM vs. SGLang)?**
A: Yes. Arbitrary frameworks and runtimes are inherited from upstream, provided the framework conforms to the rest of the rules (model equivalence, no benchmark detection, no input-based optimization, etc.). The framework must satisfy the **Available** definition ([Submission Rules §7.2](endpoints_submission_rules.md#72-available)).

**Q4: How does cross-request KV cache sharing interact with the salt mechanism?**
A: See [§2.9.5 KV Cache Rules](#295-kv-cache-rules) and [§2.9.5.1 Salting Mechanism](#2951-salting-mechanism). Cross-request KV sharing is **blanket allowed** in Endpoints (this is the primary delta vs. upstream MLPerf Inference). The performance dataset injects a per-query salt between the shared system prompt and the per-query user context, so the only prefix two queries can share is the system prompt itself. Accuracy runs use the un-salted dataset.

**Q5: Where did the previous Q&A entries on quantization, sparsity, and softmax elision go?**
A: They were promoted into the operative rules and are no longer restated here: PTQ and unused checkpoint components are in [§2.9.3](#293-model-weight-rules); drafter PTQ is in [§2.9.4](#294-speculative-decoding); pre-tokenizing clients and the salt are in [§2.9.5.1](#2951-salting-mechanism); sparse execution, attention patterns, softmax elision, hardware sparsity, and expert removal are all in [§2.9.6](#296-sparsity-and-approximate-computation).

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
| TPS per User | `tps_per_user` | `tps_per_user = 1000 / tpot_p90_ms`, where `tpot_p90_ms` is the P90 of valid per-response TPOT samples. Higher is better. |
| E2E Interactivity | `e2e_interactivity` | For agentic benchmarks, the output-token rate across completed turns. `e2e_interactivity = sum(output_tokens_per_turn) / sum(e2e_turn_time_seconds)`, where each turn is measured from request issuance through receipt of the complete response. |
| Time to First Token (P90) | `ttft_p90_ms` | 90th-percentile time, in milliseconds, from query issuance until the client receives the first non-empty text fragment (`len(s) > 0`) in any response category (visible-output, tool-call, or reasoning). |
| Concurrency | `concurrency` | The target number of in-flight concurrent queries for this measurement point. |

> [!NOTE]
> **Genuine first token.** TTFT is triggered by the first non-empty fragment (`len(s) > 0`). Emitting whitespace, control characters, punctuation, or other meaningless leading content solely to stop the TTFT clock — rather than as a genuine part of the model response — is not allowed.

> [!NOTE]
> **TTFT versioning.** The historical v0.7 rules used **P95** for the publication plot and as the primary TTFT metric. These v1.0 rules use **P90**; only `ttft_p90_ms` is required to be reported per measurement point. Additional TTFT percentiles (e.g., P50, P99) may be reported in a submission YAML, but they are not plotted in the v1.0 publication chart.

### 4.2 Derived and Presentation Metrics

> [!CAUTION]
> **`[TENTATIVE — Subject to change after 2026-06-26]`**

The following metrics are derived from primary measurements and used in publication charts. All charts use the percentile metric defined in [§4.1](#41-primary-metrics):

| Metric | Description |
|---|---|
| **Pareto curve (System TPS vs. TPS/User)** | The primary publication chart. **Y-axis:** `system_tps`. **X-axis:** `tps_per_user`. Each point corresponds to a different concurrency level. Represents the fundamental tradeoff between aggregate system capacity and per-user experience. |
| **Agentic Pareto curve (System TPS vs. E2E Interactivity)** | The primary publication chart for agentic benchmarks. **Y-axis:** `system_tps`. **X-axis:** `e2e_interactivity`. Each point corresponds to a different concurrency level. Higher values are better on both axes. |
| **System TPS vs. Concurrency** | **Y-axis:** `system_tps`. **X-axis:** `concurrency`. Shows aggregate throughput scaling with load. Each point annotated with its region. |
| **TTFT (P90) vs. Concurrency** | **Y-axis:** `ttft_p90_ms`. **X-axis:** `concurrency`. Shows how first-token latency degrades with load. P90 is the default and the only percentile plotted for v1.0; additional percentiles are deferred to a later version (see [§4.1](#41-primary-metrics)). |
| **Interactivity vs. Concurrency** | **Y-axis:** `tps_per_user`. **X-axis:** `concurrency`. Shows how per-user output rate degrades with load. |

### 4.3 Accuracy Metric

Each benchmark defines a quality target expressed as a minimum acceptable score on the benchmark's accuracy metric (e.g., ROUGE score, exact match, perplexity). The accuracy metric and quality target are specified in the benchmark definition.

Accuracy and performance runs MUST use the same endpoint configuration, model weights, and software stack.

- **Single-turn:** Every performance point MUST meet the quality threshold. Its accuracy run MUST use matching concurrency on the same instance, immediately after the performance run.
- **Multi-turn:** The arithmetic mean of accuracy scores across submitted points MUST meet the quality threshold; individual points need not. Accuracy concurrency may differ, and runs may use separate instances and need not be consecutive.

---

## 5. Pareto Collection Methodology

### 5.1 What Is Measured

Each measurement point is a benchmark run at a specific target concurrency using the benchmark-defined fixed-concurrency load pattern. Replacement queries and dependent turns are issued according to benchmark-defined timing.

### 5.2 Pareto Curve Representation

The pareto curve is represented exclusively as a **step-function** plot. Each submitted measurement point defines a discrete step at its concurrency level; between submitted points, the curve holds constant at the last measured value. No interpolation, curve fitting, or smoothing is applied to the official curve.

Visualization tools may optionally overlay interpolated or smoothed curves for readability, but these must be clearly labeled as **"interpolated (not official)"** and must not replace the step-function representation in official publications.

### 5.3 Minimum Submission Requirements

#### Minimum Point Count

Each submission must include a minimum of **7 measurement points**, structured as **1 + 3 + 3**:

| Points | Placement |
|---|---|
| 1 mandatory point | One low-latency point in the [Ultra Low Concurrency region](#low-latency-region) (concurrency 1–32). |
| 3 mandatory points | One point in each of the three [Concurrency regions](#concurrency-regions) (Low Concurrency, Medium Concurrency, High Concurrency). |
| 3 submitter's-choice points | Any concurrency level in any of the three "concurrency" regions, at the submitter's discretion. |

#### No Spacing Requirements

There is no requirement to space points evenly within or across regions. Submitters choose the exact concurrency levels that best characterize their system. This freedom enables submitters to cluster points around inflection points, highlight sweet-spot operating points, or demonstrate consistent performance across a region.

#### Submitter's-Choice Points

The 3 submitter's-choice points may be placed in any of the three "concurrency" regions, including regions that already have a required point. For example, a submitter could place all 3 additional points in the High Concurrency region to demonstrate scaling behavior, or distribute them to show overall consistency.

### 5.4 Regions of Interest

> [!CAUTION]
> Regions of Interest (ROIs) are named for either latency or concurrency, and in both cases they are constrained by concurrency. Please read the methodology carefully before proceeding.

The concurrency space is divided into four regions.

#### Ultra Low Concurrency Region <a id="low-latency-region"></a>

| Property | Value |
|---|---|
| Concurrency range | 1 to 32 (inclusive), fixed across all submissions. |
| Required points | 1 |

*Rationale:* Low-concurrency operation is critical for interactive applications (chatbots, coding assistants, real-time translation). Fixed boundaries ensure direct cross-submission comparability — every submission has at least one point in the 1–32 range.

> [!NOTE]
> Submitters are encouraged — but not required — to include a measurement at concurrency 1 (the single-user baseline) as their Low Latency point. Concurrency 1 represents the best-case per-user experience and is commonly cited in performance comparisons, but any concurrency level in the 1–32 range satisfies the region requirement.

> [!WARNING]
> The bounds of the Ultra Low Concurrency region (currently 1–32) are final for Endpoints v1.0, but they may be adjusted by the working group in a future version of these rules.

#### Maximum Supported Concurrency

The concurrency regions are defined using the **minimum concurrency** value $C_{min}$ (ideally corresponds to the best interactivity on the system) and a **maximum supported concurrency** value $C_{max}$ (this is the highest concurrency level at which the submitter chooses to benchmark their system).

Rules:

- $C_{min}$ is derived from the submission points, and $C_{max}$ defines the upper bound of the High Throughput region.
- $C_{max}$ >> $C_{min}$.
- There is no compliance test to force a particular value of $C_{max}$.
- Submitters are incentivized to choose well: $C_{max}$ defines the extent of their published pareto curve, while $C_{min}$ should produce best case interactivity.
- The value of $C_{max}$ defines the upper bound of the High Concurrency region.

#### Concurrency Regions <a id="concurrency-regions"></a>

Beyond the Ultra Low Concurrency region (concurrency > $C_{min}$), the remaining concurrency space up to $C_{max}$ is divided into **three equal regions in logarithmic space (base 2)**.

**Region Boundary Computation**

Given a declared Maximum Supported Concurrency $C_{max}$, the log-space interval `I` is:

```
I = log2(C_max - C_min) / 3
```

The three concurrency regions are:

| Region | Start | End |
|---|---|---|
| Low Concurrency | $C_{min}+1$ | $round(C_{min} + 2^{I})$ |
| Medium Concurrency | `low_conc_end + 1` | $round(C_{min} + 2^{2I})$ |
| High Concurrency | `med_conc_end + 1` | $C_{max}$ |

All non-integer boundaries are rounded to the nearest integer using **round-half-to-even (banker's rounding)**, consistent with Python's built-in `round()` function used in the reference implementation.

> **Why logarithmic spacing?** Logarithmic spacing reflects how system behavior changes: the difference between concurrency 1 and 10 is far more significant than between 1000 and 1010. Log-space division ensures each region represents a similarly meaningful range of behavioral change, regardless of absolute concurrency scale.

**High Concurrency Margin**

The High Concurrency region has a **10% margin** beyond $C_{max}$, extending the valid upper bound to $ceil(1.10 * C_{max})$.

This margin allows submitters to add points above their initial $C_{max}$ during the post-submission update window (see [Submission Rules §8.1](endpoints_submission_rules.md#81-pareto-updates)) without requiring a complete redefinition of region boundaries. The margin does not affect the required point distribution.

**Worked Examples**

<details>
<summary><strong>Example A — Large-Scale System ($C_{min} = 32$; $C_{max} = 8,192$)</strong></summary>

```
I = log2(8192 - 32) / 3 = log2(8160) / 3 = 12.994 / 3 = 4.331

Region boundaries:
  Low Latency point:        concurrency    32
  Low Concurrency:    concurrency   33 –   52  (round(32 + 2^4.331) = round(32 + 20.1) = 52)
  Med Concurrency:    concurrency   53 –  437  (round(32 + 2^8.663) = round(32 + 405.2) = 437)
  High Concurrency:   concurrency  438 – 8192

Minimum 7-point example: {32, 40, 200, 500, 1000, 2000, 4096}
```
</details>

<details>
<summary><strong>Example B — Smaller System ($C_{min} = 1$; $C_{max} = 256$)</strong></summary>

```
I = log2(256 - 1) / 3 = log2(255) / 3 = 7.994 / 3 = 2.665

Region boundaries:
  Low Latency point:       concurrency  1
  Low Concurrency:   concurrency 2 –  7  (round(1 + 2^2.665) = round(1 + 6.34) = 7)
  Med Concurrency:   concurrency 8 –  41  (round(1 + 2^5.33) = round(1 + 40.21) = 41)
  High Concurrency:  concurrency 42 – 256

Minimum 7-point example: {1, 4, 16, 32, 64, 128, 256}
```
</details>

<details>
<summary><strong>Example C — Mid-Range System ($C_{min} = 16$; $C_{max} = 1,024$)</strong></summary>

```
I = log2(1024 - 16) / 3 = log2(1008) / 3 = 9.977 / 3 = 3.326

Region boundaries:
  Low Latency point:       concurrency   16
  Low Concurrency:   concurrency  16 –   26  (round(16 + 2^3.326) = round(16 + 10.0) = 26)
  Med Concurrency:   concurrency  27 –  116  (round(16 + 2^6.652) = round(16 + 100.4) = 116)
  High Concurrency:  concurrency 117 – 1024

Minimum 7-point example: {16, 24, 64, 96, 128, 256, 1000}
```
</details>

**Boundary Edge Cases**

- **$C_{max}$ ≤ 33:** All three concurrency regions collapse to approximately one level each. Submitters with $C_{max} ≤ 33$ must notify the working group and provide written justification. The working group will review and may request additional information before accepting the submission.
- **$C_{max}$ > 100,000:** The algorithm scales correctly. The Low Concurrency region will be narrow while the High Concurrency region spans most of the range, reflecting the log-scale nature of concurrency scaling.
- **Region boundary collisions:** If rounding causes two boundaries to be equal, the affected region has zero width and a single valid concurrency level at the boundary value. One point at that level satisfies the region's requirement.

### 5.5 Region Boundary Reference Algorithm

The following pseudocode defines the authoritative computation. Submitters must use the reference implementation in the MLCommons Endpoints repository to compute their boundaries and validate their submitted points.

```python
def compute_regions(C_max: int, C_min: int) -> dict:
    assert 1 <= C_min <= 32, "Minimum concurrency must be between 1 and 32 (inclusive)"
    assert C_max > 32, "Maximum Supported Concurrency must be > 32"

    # Low Latency point (in Ultra Low Concurrency region)
    low_latency = {"start": 1, "end": C_min}

    # Compute log-space interval
    I = math.log2(C_max - C_min) / 3

    # Concurrency region boundaries (banker's rounding)
    low_conc_end = round(C_min + 2**I)
    med_conc_end = round(C_min + 2**(2 * I))

    low_concurrency  = {"start": C_min + 1,              "end": low_conc_end}
    med_concurrency  = {"start": low_conc_end+1,  "end": med_conc_end}
    high_concurrency = {"start": med_conc_end+1,  "end": C_max}

    # Extended High Concurrency margin (10%)
    margin_end = math.ceil(1.10 * C_max)

    return {
        "low_latency":      low_latency,
        "low_concurrency":   low_concurrency,
        "med_concurrency":   med_concurrency,
        "high_concurrency":  high_concurrency,
        "margin":           {"start": C_max+1, "end": margin_end},
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

All measurement points must use the benchmark-defined fixed-concurrency load pattern. The `target_concurrency` setting specifies the exact concurrency level for each point. Other load patterns (`MaxThroughput`, `Poisson`) are not valid for pareto submission points.

### 6.2 Minimum Run Duration

*(Example values — subject to ratification.)*

Each measurement point must sustain the target concurrency for a minimum duration of steady-state measurement, excluding warmup. These values correspond to the `min_duration_ms` setting in `RuntimeSettings`.

| Concurrency Region | Minimum Duration (steady state) | Rationale |
|---|---|---|
| Ultra Low Concurrency (1–32) | 600 seconds | Reduced duration accounts for slower query completion at ultra low concurrency. |
| Low Concurrency | 1200 seconds | Standard duration for statistical confidence at scale. |
| Medium Concurrency | 1200 seconds | Standard duration for statistical confidence at scale. |
| High Concurrency | 1200 seconds | Standard duration for statistical confidence at scale. |

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
| Ultra Low Concurrency (1–32) | One pass over the Ultra low concurrency dataset | Lower count acceptable given longer run duration. |
| Low Concurrency | One pass over the dataset | Consistent and comparable accuracy across all runs. |
| Medium Concurrency | One pass over the dataset | Consistent and comparable accuracy across all runs.  |
| High Concurrency | One pass over the dataset | Consistent and comparable accuracy across all runs.  |

> [!NOTE]
> These minimum query counts require statistical validation against required sample sizes for target confidence intervals. Values are subject to adjustment pending working group ratification.

For Agentic Inference, `agentic_inference.num_trajectories_to_issue` MUST be a positive integer multiple of all 613 benchmark trajectories.

### 6.5 Dataset Considerations

*(Example constraints — subject to ratification.)*

- Performance runs use `WithReplacementSampleOrder` (random sampling with replacement from the performance dataset).
- Accuracy runs use `WithoutReplacementSampleOrder` (each sample exactly once).
- For Ultra Low Concurrency region runs, a representative subset of the dataset may be used (configured via `n_samples_from_dataset`) to reduce run time, subject to pre-approval by the working group. The subset must be documented and identical across all submitters.
- `stream_all_chunks` must be set to `true` for all performance runs to enable accurate per-token timing.

### 6.6 Accuracy Requirement

*(Example constraint — subject to ratification.)*

Accuracy validation MUST follow the single-turn or multi-turn requirements in [§4.3](#43-accuracy-metric).

---

## 7. Publication Status

Publication status categories — **Available**, **Preview**, and **RDI** — including the four-point availability test, public evidence rules, software stack requirements, the 180-day Preview commitment, the 221-day RDI cooling-off period, and the [CUSTOM-SKU] open question are defined in [MLPerf Endpoints Submission Rules §7](endpoints_submission_rules.md#7-publication).

---

## 8. Submission Requirements

### 8.1 Directory Structure

An Endpoints submission must follow this directory structure:

```
<submitting_organization>/
  └── [submission_id]/                      # Provided by MLC. Each submission can only have 1 submission_id. 
      │
      ├── src/                              # SHARED across the whole submission
      │   └── <implementation>/          # e.g. trtllm/, vllm/, sglang/
      │       ├── README.md                 # how to build/launch the SUT and reproduce a point
      │       └── <endpoint interface code, infra/cluster setup, client harness>
      │
      ├── docs/                             # SHARED across the whole submission
      │   ├── calibration.adoc              # if weight transformations applied (§3.3)
      │   ├── software_disclosure.md        # §8.4
      │   └── <additional documentation>
      │
      └── results/
          └── <system>/                     # e.g. H200-SXM-141GBx8_TRT/
              └── <model_name>/        # e.g. deepseek-r1/, gpt-oss-120b/. MLC maintains a list of canonical model names for each benchmark.
                  └── r<N>/                 # one PARETO POINT per concurrency level (r1, r32, r256, …)
                      ├── point.yaml              # §8.3 — includes shared_src / shared_docs pointers
                      ├── result_summary.json     # aggregate metrics (QPS, TPS, TTFT, TPOT, ISL, %iles)
                      ├── accuracy_results.json   # §6.6
                      ├── system_desc.json       # framework/parallelism/precision for this point
                      └── server_configs/         # OPTIONAL, point-specific: backend configs tuned
                                                  #   for THIS concurrency (batch size, max_seq_len,
                                                  #   KV cache %, TP/EP/PP). Non-standard — layout is
                                                  #   submitter-defined. May include its own README.md.
```

The tree separates content that can be shared across the submission from content that is genuinely
per-measurement-point:

- **Shared content** (`src/`, `docs/`) is written once per submission. Infrastructure code (cluster
  instantiation, endpoint setup, client harness) and documentation are not duplicated per Pareto
  point. A submitter that needs different code or documentation for different systems or models adds
  another `src/<implementation_id>/` or a subdirectory under `docs/` rather than duplicating the tree.
- **Point-specific content** is only what varies with concurrency level: `point.yaml`, the result and metadata
  JSON files, and the optional `server_configs/`. Adding, replacing, or withdrawing a Pareto point must not
  require any change under `src/` or `docs/`.

Each point declares which shared content it used via the `shared_src` and `shared_docs` pointers in
its `point.yaml` (see [§8.3](#83-measurement-point-yaml)). A point whose pointers are missing or do
not resolve to an existing directory is incomplete under [§9.1](#91-automated-checks).

### 8.2 System Description (`system_desc_id.json`)

Endpoints submissions must include the following metadata:

| Field | Description |
|---|---|
| `division` | `Standardized`, `Serviced`, or `RDI`. |
| `system_name` | Submitter selected string to describe the system under test (SUT). |
| `shortened_system_name` |  Shortened `system_name` that's at most 20 characters. |
| `system_availability_status` | `Available` , `Preview`, or `RDI` (not available for purchase soon) at submission time. |
| `system_size` | Number of accelerators per node type, e.g. "72 accelerators + 144 accelerators" for a system comprising two types of nodes with 72 accelerators in the first node type and 144 accelerators in the second node type. |
| `system_node_ensemble_count` | How many unique combinations of Hardware and Software are part of the SUT. |
| `system_node_ensemble_total` | Total number of nodes in the SUT, equal to the sum of all number_of_nodes.|
| `system_node_ensemble_id` | Identifies a unique node type within the SUT. |
| `number_of_nodes` | How many nodes of type system_node_ensemble_id are in the SUT. |
| `host_processor_model_name` | Model name of the host processor. |
| `host_processors_per_node` | # of host processors per node. |
| `host_processor_core_count` | # of CPU cores in each processor. Optional, but at least one of host_processor_core_count and host_processor_cpu_count must be present. |
| `host_processor_vcpu_count` | # of vCPUs in each processor. Optional, but at least one of host_processor_core_count and host_processor_vcpu_count must be present. |
| `accelerator_model_name` | Model name of the accelerator. |
| `accelerators_per_node` | # of accelerators per node. |
| `accelerator_host_interconnect` | Describes the interconnect link between the accelerator and the host processors. |
| `accelerator_interconnect` | Describes the interconnect link between accelerators, when multiple accelerators are present as indicated by accelerators_per_node > 1. |
| `accelerator_memory_capacity` | Memory capacity per accelerator. |
| `accelerator_memory_type` | Type of memory for the accelerator. |
| `host_memory_capacity` | Total memory capacity for all host processors. Not per-processor. |
| `host_memory_configuration` | Memory configuration for the host processors, e.g., how many DIMMs, what kind of memory (DDR5, LPDDR4, etc.), and speed. |
| `host_network_card_count` | Describes the # and type of networking cards and associated speeds. |
| `host_networking` | Describes the networking protocol, e.g., Infiniband, Ethernet. |
| `host_storage_capacity` | Total storage capacity for the node. |
| `host_storage_type` | Description of the type of storage in the node. |
| `other_hardware` | Describes any other performance relevant hardware in the node, freeform field. |
| `cooling` | Describes if the node uses any liquid cooling, only air-cooling, or only passive cooling. |
| `hw_notes` | Submitter hardware notes to supplement other information, freeform field. |
| `serving_framework` | Serving Framework used for submission, e.g., SGLang, vLLM, etc. |
| `inference_backend` | Inference backend used for submission, e.g., vendor stack components. |
| `driver` | Driver and version number for any accelerators. |
| `container_link` | Link to container for submission. |
| `model_name` | Benchmark model name (must match supported model list). |
| `max_supported_concurrency` | Declared Maximum Supported Concurrency `M`. |
| `endpoint_url` | URL or description of the endpoint under test. |
| `operating_system` | OS used for the node. |
| `filesystem` | Filesystem used for the node. |
| `other_software_stack` | Describes any other performance relevant software in the node, freeform field. |
| `sw_notes` | Submitter software notes to supplement other information, freeform field. |
| `node_config` | Describes the configuration of nodes or processors in the SUT (as described by system_size) for this run. Should be provided by submitter and contain sufficient detail to enable reproducing the submission (e.g., describing configuration of inference server for all nodes). |
| `config_summary` | Describes the configuration options for the SUT for this run — a concatenation of `disaggregated`, `tensor_parallel`, `pipeline_parallel`, `expert_parallel`, `data_parallel` (where these fields are > 1) and `config_summary_notes`. Should be provided by submitter and contain sufficient detail to enable reproducing the submission. |
| `disaggregated` | Indicates whether the system is disaggregated (disaggregated > 1). If disaggregated <!-- TODO: definition is truncated in the source data dictionary, verify full text with the data dictionary owner. --> |
| `expert_parallel` | Expert parallel partitioning of the model for the run. Only applies to Mixture-of-Expert models. EP=N means that the experts are split into N separate groups that reside on different processors/accelerators, and tokens are routed to the appropriate group. EP=1 means no partitioning. |
| `tensor_parallel` | Parallel partitioning of the model weight matrices for the run. TP=N means the weight matrices are split N ways and each partition contains 1/N of the weights of each layer and computes 1/N of the layer. Generally the number of attention heads in the model must be divisible by N. TP=1 means no partitioning. |
| `pipeline_parallel` | Sequential partitioning of the layers of the model into a pipeline for the run. PP=N means the layers of the model are split sequentially into a pipeline with N stages, each stage contains 1/N of the layers of the model. Each processor/accelerator contains one stage and a single inference must pass through all stages of the pipeline. PP=1 means no partitioning. |
| `data_parallel` | Data parallel replication of the model for the run. DP=N means the model is replicated N times, and requests are distributed across the N replicas. DP=1 means no replication. |
| `batch` | Maximum batch size. |
| `config_summary_notes` | Free form field from the submitter to contain information not captured by other fields that concatenate into config_summary. |
| `link_config` | Link to full configuration logs for the run (e.g., in GitHub). |
| `tps_utilization` | reported_system_tps / (max of all reported_system_tps for all runs) |

#### 8.2.1 Template Structure

`systems/<system_desc_id>.json` contains the fields defined in the table above.

```json
{
  "division": "",
  "system_name": "",
  "shortened_system_name": "",
  "system_availability_status": "",
  "system_size": "",
  "system_node_ensemble_count": 0,
  "system_node_ensemble_total": 0,
  "endpoint_url": "",
  "serving_framework": "",
  "node_types": [
    {
      "system_node_ensemble_id": 0,
      "number_of_nodes": 0,
      "host_processor_model_name": "",
      "host_processors_per_node": 0,
      "host_processor_core_count": 0,
      "host_processor_vcpu_count": 0,
      "host_memory_capacity": "",
      "host_memory_configuration": "",
      "accelerator_info": [
        {
          "accelerator_model_name": "",
          "accelerators_per_node": 0,
          "accelerator_memory_capacity": "",
          "accelerator_memory_type": "",
          "accelerator_interconnect": "",
          "accelerator_host_interconnect": ""
        }
      ],
      "host_network_card_count": "",
      "host_networking": "",
      "host_storage_capacity": "",
      "host_storage_type": "",
      "other_hardware": "",
      "cooling": "",
      "hw_notes": "",
      "inference_backend": "",
      "driver": "",
      "operating_system": "",
      "filesystem": "",
      "container_link": "",
      "other_software_stack": "",
      "sw_notes": ""
    }
  ],
  "node_config": "",
  "disaggregated": 0,
  "expert_parallel": 0,
  "tensor_parallel": 0,
  "pipeline_parallel": 0,
  "data_parallel": 0,
  "batch": 0,
  "config_summary": "",
  "config_summary_notes": "",
  "link_config": "",
  "tps_utilization": 0
}
```

### 8.3 Measurement Point YAML

Each measurement point must be accompanied by a YAML configuration file specifying:

| Field | Description |
|---|---|
| `concurrency` | The target concurrency level. |
| `region` | The region this point satisfies (`low_latency`, `low_throughput`, `med_throughput`, `high_throughput`, or `submitters_choice`). |
| `runtime_settings` | The `RuntimeSettings` used for this run (load pattern, `min_duration_ms`, `min_sample_count`, `stream_all_chunks`, etc.). |
| `dataset` | Dataset name and any `n_samples_from_dataset` override (if applicable). |
| `warmup` | The warmup procedure declaration required by [§6.3.3](#633-documentation-requirements) — `duration_s`, `requests_issued`, `requests_completed`, `data_source` (description of the warmup data and its origin), `concurrency`, and `initialization_steps` (platform-specific setup completed before `TEST_STARTED`). |
| `division` | `Standardized`, `Serviced`, or `RDI`. <!-- TODO: also listed in §8.2 pending placement review --> |
| `max_supported_concurrency` | Declared Maximum Supported Concurrency `M`. |
| `model_name` | Display name of model, should be consistent across all external usages. |
| `model_precision` | Lowest precision numerical format used for the weights of the model. For example, if a model comprises FP16 and FP8, then model_precision is FP8. |
| `link_to_model` | Link to model submitted e.g., via GitHub. |
| `link_to_model_transformation` | Link to calibration/quantization/retraining write-up. |
| `model_notes` | Submitter software notes to supplement other information, freeform field. |
| `dataset_name` | Display name of dataset, should be consistent across all external usages. |
| `dataset_type` | Is the dataset used for "Accuracy", "Performance", or "Accuracy + Performance". |
| `dataset_link` | Link to data used for submission e.g., via GitHub. |

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
<major-version>.<minor-version>.<cohort-number>.<model_id>.<dataset_id>.<entry-number>
```

| Component | Description |
|---|---|
| `major-version` | Major version of the MLPerf Endpoints rules under which the result was submitted (e.g., `1` for v1.0). |
| `minor-version` | Minor version of the same (e.g., `0` for v1.0). |
| `cohort-number` | Cohort Number for this submission (e.g., `0` for the first cohort of a given version, `1` for the second, etc.)
| `model_id` | Benchmark model identifier from the round's supported model list ([§3.2](#32-supported-models)). Must match `benchmark_model` in `system_desc_id.json` ([§8.2](#82-system-description-system_desc_idjson)). |
| `dataset_id` | Identifier of the dataset used for the performance and accuracy runs, as named in the benchmark definition ([§3.1](#31-benchmark-definition)) and recorded in each point's `dataset` field ([§8.3](#83-measurement-point-yaml)). |
| `entry-number` | Sequence number assigned at publication, unique within the preceding four components. |

Example: `1.0.0.deepseek-r1.mmlu-pro.7` — the seventh published DeepSeek-R1 result on MMLU-Pro under the v1.0 rules.

Result IDs are assigned by MLCommons at publication; they are not chosen by the submitter and are not part of the submitted bundle. They are stable and never reused — a result that is superseded, withdrawn, or invalidated retains its result ID in the historical record, and the replacement result receives a new entry number (see [Submission Rules §8.1](endpoints_submission_rules.md#versioning-and-historical-record)).

---

## 9. Compliance Validation

### 9.1 Automated Checks

The compliance validator — run by the submitter before submission and by MLCommons upon receipt — performs the following checks:

| Check | Validation | Failure Action |
|---|---|---|
| **Submission completeness** | All required files, YAML configurations, result artifacts, and system descriptions are present. | Reject submission. |
| **Shared path resolution** | Each point's `shared_src` and `shared_docs` resolve to an existing directory under the submission root. | Reject submission. |
| **Point count** | ≥ 7 total measurement points. | Reject submission. |
| **Ultra Low Concurrency coverage** | ≥ 1 point with concurrency in [1, 32]. | Reject submission. |
| **Low Concurrency coverage** | ≥ 1 point in the Low Concurrency region. | Reject submission. |
| **Medium Concurrency coverage** | ≥ 1 point in the Medium Concurrency region. | Reject submission. |
| **High Concurrency coverage** | ≥ 1 point in the High Concurrency region. | Reject submission. |
| **Max concurrency declared** | $C_{max} > 32$; declared in `system_desc_id.json`. | Reject submission. |
| **Point cap** | ≤ 32 total measurement points. | Reject points beyond 32. |
| **Concurrency in range** | Each point's concurrency falls within a valid region (including the 10% High Concurrency margin), computed using the reference algorithm in [§5.5](#55-region-boundary-reference-algorithm). | Flag out-of-range points. |
| **Load pattern** | All points used the benchmark-defined fixed-concurrency load pattern. | Reject non-conforming points. |
| **Run duration** | Each point meets the minimum steady-state duration for its region (see [§6.2](#62-minimum-run-duration)). | Flag non-compliant points. |
| **Minimum query count** | Each point meets §6.4, including the Agentic Inference trajectory multiple. | Flag non-compliant points. |
| **Streaming config** | `stream_all_chunks = true` for all performance runs. | Flag non-compliant points. |
| **Warmup metadata** | Each point's YAML declares the warmup fields required by [§6.3.3](#633-documentation-requirements) (`duration_s`, `requests_issued`, `requests_completed`, `data_source`, `concurrency`, `initialization_steps`). | Flag non-compliant points. |
| **Warmup logs retained** | Warmup request logs are retained and available for reviewer inspection (see [§6.3.2](#632-discard-policy)). | Flag non-compliant points. |
| **Metric consistency** | The valid per-response TPOT distribution must be non-empty with a finite, strictly positive P90; the normalized P90 value in milliseconds is `tpot_p90_ms` and `tps_per_user = 1000 / tpot_p90_ms`. For agentic points, `e2e_interactivity` must be derivable from its §4 definition. The authoritative result schema defines TPOT serialization and units. | Flag inconsistent points. |
| **Accuracy** | Accuracy satisfies the applicable single-turn or multi-turn gate in §4.3. | Reject submission. |
| **Seed-set validity** | For an initial submission, every point must record the same seed set, and that set must have been published for `target_cohort` or one of the three immediately preceding cohorts. For an amendment, every new or replacement point must match the original submission's bound seed set; the four-cohort adoption test is not reapplied using the amendment's later cohort. See [Submission Rules §4.6](endpoints_submission_rules.md#46-seed-rotation). | Reject submission. |
| **Configuration consistency** | Same model, endpoint configuration, software stack, and seed set across all measurement points. | Flag inconsistencies. |

### 9.2 Manual Review Focus Areas

Human reviewers should focus on aspects that automation cannot easily verify:

- Whether the pareto curve shape is physically plausible (throughput should generally increase with concurrency up to saturation, then plateau or decrease).
- Whether metric distributions suggest artificial manipulation (e.g., suspiciously uniform TTFT values across very different concurrency levels).
- Whether TTFT-triggering fragments are genuine parts of the model response rather than meaningless leading content emitted to stop the TTFT clock.
- Whether content is duplicated across assistant-response fields or padded to inflate the official output-token count.
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

### \[TOK-COUNT\] Reference-Chat-Template Tokenization and Reported Throughput

**Question:** The reference-chat-template tokenization rule ([§2.8 Tokenizer Rules](#28-tokenizer-rules)) may produce token counts that differ from what individual serving stacks report as "tokens/second" internally. Have MLC stakeholders and submitter organizations agreed that the published metric will use the client-side reference count and not the serving-stack-reported count?

**Context:** Resolution is needed before v1.0 publishes side-by-side comparison charts. The current §2.8 wording—coalesce visible output and reasoning in arrival order, reassemble parallel tool calls by list index, render the complete structured assistant message with the official reference chat template, subtract empty assistant framing, and tokenize once—is the proposed rule. The open question is whether stakeholders accept that the published numbers may differ from internal serving-stack-reported numbers.

### \[CKPT-RESIDENCY\] Checkpoint Component Residency

**Question:** Must a component present in the canonical checkpoint — for example a speculative-decoding head such as MTP — be loaded into accelerator memory during measurement, or is it sufficient that it be present in the submitted checkpoint artifact?

**Context:** [§2.9.3](#293-model-weight-rules) requires a derived checkpoint to preserve the component set of the canonical checkpoint, so a component may not be stripped during quantization. That rule governs the *artifact* and establishes provenance; it does not require the component to be resident at run time. A submission may therefore ship a complete checkpoint, satisfy any provenance check, and still exclude the component at load time — freeing accelerator memory that converts directly into KV-cache capacity, and therefore into concurrency and throughput. Where the component is a material fraction of the parameter count, this is a measurable advantage over a submitter who keeps it resident, and it is currently undisclosed. Resolution is needed before the first round in which a benchmark model ships an optional auxiliary head.

**Options under consideration:**

1. **Require residency.** Components present in the canonical checkpoint must be loaded into the serving process for all measurement points, whether or not they are used. Strongest comparability, but forces submitters to reserve memory for a module they have legitimately disabled under [§2.9.4](#294-speculative-decoding).
2. **Require disclosure of the loaded component set.** Permit non-residency, but declare per measurement point which canonical components were loaded, alongside the existing drafter configuration fields. Preserves the engineering choice while making it visible to reviewers; would extend the disclosure table in [§2.9.6.6](#2966-disclosure).
3. **Leave unconstrained.** Treat memory footprint as a legitimate configuration dimension, consistent with [§2.9.4](#294-speculative-decoding) already permitting speculation to be disabled at any or all measurement points.

### Division and Scenario Open Items

| Item | Current Proposal | Status |
|---|---|---|
| Allowed techniques for Standardized CoN | Framework defined, details TBD | TBD |
| Output-tokenizer scoring rules | Client-side reference tokenizer is canonical for official output counts; internal serving tokenizers do not require equivalence or mapping factors for output scoring | Proposed |
| Serviced division audit procedures | Required, details TBD | TBD |
| Caching rules for Serviced division | Not allowed across queries | Proposed |
| Response stream modification rules | Not allowed outside reference API | Proposed |
| Future division for new models/datasets | To be determined by WG | TBD |
| Fabric vs. bus restrictions (Standardized CoN) | Not imposed (borrowed from Network Division) | Proposed |
| Batch/chunk tokenizer variability | Reconstruct the complete structured assistant response, render it with the official reference chat template, exclude empty assistant framing, and apply the reference tokenizer once | Proposed |

---

## Appendix B: Quick-Reference Region Boundary Table

<details>
<summary><strong>Quick-Reference Region Boundaries by $C_{min}$ and $C_{max}$</strong></summary>

Pre-computed region boundaries for common combinations of Minimum Concurrency ($C_{min}$) and Maximum Supported Concurrency ($C_{max}$) values using the reference algorithm.

| Max Concurrency <br>($C_{max}$) | Min Concurrency <br>($C_{min}$) | Low Concurrency | Medium Concurrency | High Concurrency | 10% Margin |
|---|---|---|---|---|---|
| 64 | 2 | 3–6 | 7–18 | 19–64 | 65–71 |
| 128 | 2 | 3–7 | 8–27 | 28–128 | 129–141 |
| 256 | 2 | 3–8 | 9–42 | 43–256 | 257–282 |
| 256 | 8 | 9–14 | 15–47 | 48–256 | 257–282 |
| 512 | 8 | 9–16 | 17–71 | 72–512 | 513–564 |
| 1,024 | 8 | 9–18 | 19–109 | 110–1,024 | 1,025–1,127 |
| 512 | 16 | 17–24 | 25–79 | 80–512 | 513–564 |
| 1,024 | 16 | 17–26 | 27–117 | 118–1,024 | 1,025–1,127 |
| 2,048 | 16 | 17–29 | 30–176 | 177–2,048 | 2,049–2,253 |
| 1,024 | 32 | 33–42 | 43–131 | 132–1,024 | 1,025–1,127 |
| 2,048 | 32 | 33–45 | 46–192 | 193–2,048 | 2,049–2,253 |
| 4,096 | 32 | 33–48 | 49–287 | 288–4,096 | 4,097–4,506 |
| 8,192 | 32 | 33–52 | 53–437 | 438–8,192 | 8,193–9,012 |
| 16,384 | 32 | 33–57 | 58–676 | 677–16,384 | 16,385–18,023 |

*All boundaries computed using the reference algorithm in [§5.5](#55-region-boundary-reference-algorithm) with banker's rounding. The Low Latency point is a single point at the declared $C_{min}$ value (in the Ultra Low Concurrency region); all concurrency regions and their boundaries are submission-specific and depend on both $C_{min}$ and $C_{max}$.*

</details>
