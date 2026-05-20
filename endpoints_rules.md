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
9. [Compliance Validation](#9-compliance-validation)
   - [9.1 Automated Checks](#91-automated-checks)
   - [9.2 Manual Review Focus Areas](#92-manual-review-focus-areas)
- [Appendix A: Open Questions and Working Group Items](#appendix-a-open-questions-and-working-group-items)
- [Appendix B: Quick-Reference Region Boundary Table](#appendix-b-quick-reference-region-boundary-table)

---

## 1. Basics

These rules define the technical requirements for MLPerf Endpoints benchmark submissions: what to measure, how to measure it, which division to submit under, and what evidence is required for each publication status category.

The submission, review, and publication *process* is defined separately in the companion [MLPerf Endpoints Submission Rules](endpoints_submission_rules.md) document.

MLPerf Endpoints measures the performance of *inference endpoints* serving generative AI models. Unlike traditional MLPerf Inference benchmarks — which measure latency or throughput at a single operating point — MLPerf Endpoints characterizes the full performance *envelope* of a serving system as a Pareto curve across a range of concurrency levels.

The benchmark is designed to be:

- **Fair** — standardized measurement methodology with compliance validation.
- **Inclusive** — minimum 7 measurement points with flexible placement to accommodate systems of all scales.
- **Relevant** — covering operating points valued by real users: single-user interactive latency through high-throughput batch serving.
- **Extensible** — modular rules that can accommodate new models, metrics, and divisions without redesign.

---

## 2. Divisions and Deployment Scenarios

MLPerf Endpoints replaces the traditional Closed/Open division structure from MLPerf Inference with three divisions tailored to endpoint benchmarking: Standardized, Serviced, and RDI. All divisions use the same pareto collection methodology ([§5](#5-pareto-collection-methodology)) and run requirements ([§6](#6-run-requirements-per-measurement-point)). A submission must declare exactly one division.

The Available/Preview/RDI publication status categories defined in [Submission Rules §7](endpoints_submission_rules.md#7-publication) continue to apply independently of division.

### 2.1 Client Deployment Scenarios

MLPerf Endpoints defines two scenarios that determine how the client infrastructure connects to the System Under Test (SUT).

#### 2.1.1 Client on Prem (CoP)

The submitter hosts both the client infrastructure and the endpoint server infrastructure. The client and server may be co-located in the same data center or connected via a local network.

- The submitter provides and operates both client and server infrastructure.
- The client must use the MLPerf Endpoints reference client (`inference_endpoint` from `github.com/mlcommons/endpoints`) without modification, compiled from the tagged revision for the submission round.
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

The Standardized division is the primary benchmark division, requiring strict adherence to model equivalence rules and full code visibility. It replaces the traditional "Closed" division from MLPerf Inference.

**Transparency:** Whitebox — all source code, model weights, configurations, and optimization details must be disclosed.

**Available Scenarios:** Client on Prem (CoP) and Client over Network (CoN), reported as separate sub-divisions.

#### 2.2.1 General Rules

- Requires pre-processing, post-processing, and a model equivalent to the reference or alternative implementation, per the model equivalence rules defined in these rules.
- Allows calibration for quantization. Does not allow any retraining, fine-tuning, pruning, or sparsification of model weights.
- All submissions must be reproducible: complete source code for the inference server, client integration, and all optimization scripts must be submitted.
- On-prem (CoP) submissions must be self-contained.

**Allowed optimization techniques:**

- Quantization (with calibration only; no retraining).
- KV-cache optimizations.
- Kernel fusion and operator-level optimizations.
- Hardware-specific memory management and scheduling.
- Continuous / in-flight batching.
- Speculative decoding (within model equivalence constraints).

**Not allowed:** Retraining, fine-tuning, pruning, sparsification, response caching, deliberate token dispatch delays, or any modification of the request/response stream outside the reference API specification.

#### 2.2.2 Client over Network (CoN) — Additional Rules

When submitting to the Standardized division via the CoN scenario, the following additional rules apply:

- CoN submitters may choose to submit to CoP instead, but must follow all CoN compliance rules when doing so.
- Servers must not modify incoming or outgoing request/response streams outside the provided MLPerf Endpoints reference API specification.
- No pre-processing of incoming requests (e.g., changing precision or data layout) or post-processing of outgoing responses (e.g., gather, reduction, ArgMax) beyond what is specified in the reference implementation.
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

Primary accelerator details include: accelerator model, count, memory capacity, and interconnect type. Mapping configurations include: tensor parallelism (TP), expert parallelism (EP), pipeline parallelism (PP), batch size, and other deployment parameters. For Serviced submissions, full rack hardware disclosure is optional, but the primary accelerator must be identified.

---

### 2.8 Tokenizer Rules

Different tokenizers can produce different token counts depending on batch or chunk size. To ensure consistent measurement across divisions:

- The **reference tokenizer** output is the canonical measurement for token counting across all divisions.
- All performance metrics (System TPS, TPS/User, TTFT) are computed using reference tokenizer token counts.
- Submitters using alternative tokenizers must report mapping factors or demonstrate equivalence.

> [!NOTE]
> **[WIP]** — Detailed tokenizer equivalence rules and batch/chunk variability handling are under development by the working group.

---

### 2.9 Model Equivalence Rules (Standardized Division)

> [!Note]
>  This entire section is a working draft. The working group has agreed to use existing [MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc) model equivalence and optimization rules for the initial v0.7 submission in June 2026.

> [!WARNING]
> **[WIP — WG Input Required]** — This entire section is a working draft. The model equivalence rules must be aligned with and should not stray from the definitions in [MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc). All subsections below require review and ratification by the working group before they can be treated as policy. Nothing in this section represents finalized rules.

These rules define what it means for a Standardized division submission to be "model equivalent" to the reference implementation. The accuracy quality target (§4.3) is the ultimate arbiter of model equivalence: a submission that passes the accuracy gate is considered equivalent regardless of internal implementation choices. The rules below define which implementation choices are permitted in reaching that accuracy gate.

#### 2.9.1 Reference Implementation

> [!NOTE]
> **[WIP — align with inference_rules.adoc §reference-implementation]**

Each benchmark has a **reference implementation** published in the MLPerf Endpoints reference repository. The reference implementation defines:

- The canonical model weights and tokenizer.
- The required input and output format (including prompt templates and chat templates).
- The accuracy evaluation methodology and quality target.
- The endpoint API interface.

An **alternative reference implementation** may be designated by the working group for a specific architecture or hardware class, subject to passing the same accuracy quality target as the primary reference implementation.

#### 2.9.2 Pre-Processing Equivalence

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division pre-processing rules]**

The server-side pre-processing applied to each incoming request must be functionally equivalent to the reference implementation:

- **Tokenization:** Must produce the same token IDs as the reference tokenizer for the same input text. Submitters using an alternative tokenizer implementation must demonstrate token-for-token equivalence on the accuracy dataset.
- **Chat template / prompt formatting:** The system prompt, user turn formatting, and special tokens (BOS, EOS, role markers) must match the canonical chat template defined in the benchmark specification. Modifications to the chat template that change the effective input to the model are not permitted.
- **Input truncation:** If the reference implementation truncates inputs that exceed the model's context window, the submitter's truncation method must produce the same result.

#### 2.9.3 Model Weight Rules

> [!NOTE]
> **[WIP — align with inference_rules.adoc closed division model rules]**

All Standardized division submissions must begin from the **canonical model weights** specified in the benchmark definition (identified by Hugging Face model ID or a published checksum).

**Allowed weight transformations:**

| Transformation | Allowed | Conditions |
|---|---|---|
| Post-training quantization | ✓ | Calibration dataset only. No gradient updates. Must be disclosed. |
| Weight format conversion | ✓ | e.g., fp32 → fp16 → bf16, transposition, tiling for hardware layout. |
| INT8 / INT4 / FP8 quantization | ✓ | Any precision supported by the hardware. Must pass accuracy gate. |
| AWQ, GPTQ, bitsandbytes-style methods | ✓ | Post-training only. Calibration data must be disclosed. |
| Block-sparse weight pruning | ✗ | Not permitted. |
| Unstructured pruning | ✗ | Not permitted. |
| Fine-tuning / LoRA / adapter layers | ✗ | Any gradient-based weight update is not permitted. |
| Retraining from scratch or continued pre-training | ✗ | Not permitted. |
| Knowledge distillation to a smaller architecture | ✗ | Not permitted. |

#### 2.9.4 Speculative Decoding

> [!WARNING]
> **[WIP — WG Input Required]** — The constraints below were not taken directly from inference_rules.adoc and must not be treated as policy. The working group must define speculative decoding rules for MLPerf Endpoints from first principles or by explicit adoption of the inference rules definition. Do not implement compliance checks based on this subsection.

Speculative decoding is permitted in the Standardized division, subject to the following constraints:

- **Draft model disclosure.** The draft model used must be identified by name, version, and source. A draft model that is not publicly disclosed and available is not permitted.
- **Draft model weights.** The draft model must use publicly available weights from the same model family (e.g., a smaller checkpoint of the same base model, or the same model with a draft head trained on public data). A custom draft model trained specifically for benchmark performance is not permitted.
- **Verification step.** The target model used in the verification step must be the canonical model with permitted weight transformations (§2.9.3) applied. The verification step may not be approximated, skipped, or replaced by a secondary draft model.
- **Number of speculative tokens.** The number of draft tokens per step (`k`) must be declared in the submission YAML. It may vary dynamically, but the distribution must be reported.
- **Output equivalence.** Speculative decoding must produce outputs that are token-for-token identical to what the target model would generate without speculation — i.e., the verification step must not introduce acceptance criteria that would cause the model to accept tokens the target would not have generated. Approximate speculative decoding methods that alter the output distribution are not permitted in the Standardized division.

#### 2.9.5 KV Cache Rules

> [!WARNING]
> **[WIP — WG Input Required]** — KV cache rules were not taken directly from inference_rules.adoc and must be defined by the working group. The inference rules address KV cache in the context of the closed division; those definitions should be the starting point for this section.

- **KV cache quantization.** The KV cache may be stored at reduced precision (e.g., INT8, INT4, FP8 KV). This must be disclosed and does not require working group pre-approval, provided the submission passes the accuracy gate.
- **Paged / virtual KV cache.** Paged attention and virtual KV cache implementations (e.g., vLLM's PagedAttention) are permitted.
- **KV cache compression.** Structured KV cache compression methods (e.g., H2O, SnapKV, sliding-window eviction) are permitted if they are part of the reference implementation or a designated alternative implementation. Compression methods not in the reference must be disclosed and are subject to Methodology objections during peer review.
- **Cross-request KV sharing.** Sharing KV cache state across independent requests (prefix caching, prompt caching) is **permitted** as a serving optimization, provided: (1) the output tokens produced are identical to what would be produced without caching; and (2) the cache is not used to share information from one user's response into another user's generation (no cross-user context leakage).
- **Response caching.** Returning a cached response verbatim to a request that matches a previous request is **not permitted**. Every request must go through the forward pass.

#### 2.9.6 Attention Mechanism Rules

> [!WARNING]
> **[WIP — WG Input Required]** — Attention mechanism rules were not taken directly from inference_rules.adoc. Working group should review the inference rules closed division definitions and adopt or adapt as appropriate for the Endpoints context.

The attention mechanism may be replaced with any functionally equivalent implementation:

- Flash Attention, Flash Attention 2, Flash Attention 3, and equivalent hardware-optimized attention kernels are permitted.
- Grouped Query Attention (GQA) and Multi-Query Attention (MQA) are permitted if present in the canonical model architecture.
- Sliding window attention and local attention are permitted if present in the canonical model architecture.
- Changes to the attention pattern that are **not** present in the canonical model (e.g., converting full attention to sparse attention, adding sink tokens not in the reference) are not permitted.

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

A Standardized division submission passes model equivalence if and only if it meets the **accuracy quality target** defined for the benchmark, evaluated using the reference evaluation methodology on the accuracy dataset. Passing the accuracy gate is necessary and sufficient for model equivalence.

The accuracy quality target and tolerance relative to the reference score are specified per benchmark in the benchmark definition.

---

## 3. Benchmarks and Models

### 3.1 Benchmark Definition

A benchmark in MLPerf Endpoints is defined by a specific model, task, and quality target. Each benchmark has a reference implementation that defines the correct endpoint interface, input/output format, and accuracy evaluation method.

### 3.2 Supported Models

The set of supported benchmark models is defined per submission round and maintained in the MLPerf Endpoints reference repository. Each supported model specifies:

- The canonical model weights (e.g., Hugging Face model ID or checksum).
- The input/output format (token IDs or text, streaming or non-streaming).
- The accuracy metric and quality target.
- The dataset used for performance and accuracy runs.

> [!NOTE]
> The model list for each submission round is published in the MLPerf Endpoints reference repository at least 6 weeks before the submission round opens. New models may be proposed to the working group per the benchmark roadmap process defined in the MLPerf General Submission Rules §4.3.

### 3.3 Weight Transformations

Submitters may apply quantization, format conversion, or other weight transformations to the reference weights, subject to the accuracy quality target. All transformations must be documented in the submission. For the Standardized division, the full set of permitted and prohibited transformations is defined in [§2.9.3 Model Weight Rules](#293-model-weight-rules).

---

## 4. Metrics

### 4.1 Primary Metrics

Each measurement point on the pareto curve captures the following metrics at a specific concurrency level:

| Metric | Symbol | Definition |
|---|---|---|
| System Tokens per Second | `system_tps` | Total output tokens produced per second across all concurrent users. `system_tps = total_output_tokens / elapsed_duration_seconds`. |
| TPS per User | `tps_per_user` | Average output tokens per second experienced by a single user. `tps_per_user = system_tps / concurrency`. |
| Time to First Token (P50) | `ttft_p50_ms` | Median time from query issuance to receipt of the first output token, in milliseconds. |
| Time to First Token (P95) | `ttft_p95_ms` | 99th-percentile time to first token, in milliseconds. |
| Concurrency | `concurrency` | The target number of in-flight concurrent queries for this measurement point. |

### 4.2 Derived and Presentation Metrics

The following metrics are derived from primary measurements and used in publication charts:

| Metric | Description |
|---|---|
| **Pareto curve (System TPS vs. TPS/User)** | The primary publication chart. Plots `system_tps` on the y-axis against `tps_per_user` on the x-axis, with each point corresponding to a different concurrency level. Represents the fundamental tradeoff between aggregate system capacity and per-user experience. |
| **Concurrency vs. System TPS** | Shows aggregate throughput scaling with load. Each point annotated with its region. |
| **Concurrency vs. TTFT P50 and P95** | Shows how first-token latency degrades with load. |
| **Concurrency vs. Interactivity** | Shows how interactivity, shown as `tps_per_user`, degrades with load. |

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

*(Example values — subject to ratification.)*

A warmup period of at least **60 seconds** at the target concurrency must precede the measurement period. Warmup events (before `TEST_STARTED`) are excluded from metric computation. The warmup ensures connection pools are populated, caches are warm, and the system is in steady state.

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
      <implementation_id>/
        <endpoint interface code and configuration>
  pareto/
    <system_desc_id>/
      <benchmark_model>/
        points/
          point_<concurrency_level>.yaml    # one per measurement point
        results/
          point_<concurrency_level>/
            mlperf_endpoints_log_summary.json
            mlperf_endpoints_log_detail.json
            system_desc.json 
        accuracy/
          accuracy_result.json
          accuracy.txt
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

### 8.4 Software Disclosure

For **Standardized** and **RDI** division submissions, all software components that substantially determine ML performance must be disclosed. This includes, at minimum:

- Inference serving framework (name, version, commit hash or release tag).
- ML accelerator library (e.g., TensorRT-LLM, cuDNN — version and build).
- Driver version.
- Operating system.

For **Serviced** division submissions, disclose all software information available from public documentation and API metadata.

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
| **Metric consistency** | `system_tps` derivable from total tokens and elapsed duration; `tps_per_user = system_tps / concurrency`. | Flag inconsistent points. |
| **Accuracy** | At least one accuracy run passes the benchmark quality target. | Reject submission. |
| **Configuration consistency** | Same model, endpoint configuration, and software stack across all measurement points. | Flag inconsistencies. |

### 9.2 Manual Review Focus Areas

Human reviewers should focus on aspects that automation cannot easily verify:

- Whether the pareto curve shape is physically plausible (throughput should generally increase with concurrency up to saturation, then plateau or decrease).
- Whether metric distributions suggest artificial manipulation (e.g., suspiciously uniform TTFT values across very different concurrency levels).
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

**Question:** What are the ratified values for minimum run duration, warmup period, minimum query count, and dataset subset rules?

**Context:** [§6 Run Requirements](#6-run-requirements-per-measurement-point) currently contains illustrative example values. All values in that section are pending working group ratification based on empirical validation data.

### Division and Scenario Open Items

| Item | Current Proposal | Status |
|---|---|---|
| Allowed techniques for Standardized CoN | Framework defined, details TBD | TBD |
| Tokenizer equivalence rules | Reference tokenizer as canonical | TBD |
| Serviced division audit procedures | Required, details TBD | TBD |
| Caching rules for Serviced division | Not allowed across queries | Proposed |
| Response stream modification rules | Not allowed outside reference API | Proposed |
| Future division for new models/datasets | To be determined by WG | TBD |
| Fabric vs. bus restrictions (Standardized CoN) | Not imposed (borrowed from Network Division) | Proposed |
| Batch/chunk tokenizer variability | Reference tokenizer output is canonical | Proposed |

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
