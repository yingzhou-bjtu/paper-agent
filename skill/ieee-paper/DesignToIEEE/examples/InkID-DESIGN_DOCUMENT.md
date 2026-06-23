# Software Design Document: InkID -- Stylometric Authorship Verification and AI Text Detection System

## 1. Abstract

InkID is a computational linguistics system designed for stylometric authorship verification and artificial intelligence-generated text detection. The system employs a hybrid natural language processing (NLP) architecture that integrates character-level and word-level Term Frequency-Inverse Document Frequency (TF-IDF) representations for authorship attribution, alongside heuristic-based statistical indicators including Shannon word entropy, sentence-length variance (burstiness), and average sentence length for AI text detection. By fusing dual-similarity scoring for authorship verification with a tri-signal ensemble for AI detection, InkID provides a unified analytical platform capable of determining whether a disputed text originates from a known author and estimating the probability that a given text was machine-generated. The system is implemented as a single-page web application using the FastAPI framework, with a scikit-learn-based NLP engine and a responsive frontend interface. This document presents the complete software design, architectural decisions, algorithmic foundations, and implementation details of the InkID system.

---

## 2. Introduction

### 2.1 Problem Statement

The proliferation of large language models (LLMs) and the increasing accessibility of AI text generation tools have introduced significant challenges in digital text authentication. Two interrelated problems have emerged as critical concerns in computational linguistics and digital forensics. First, authorship verification -- the task of determining whether a disputed document was written by a claimed author -- remains computationally non-trivial, particularly when only limited writing samples are available for comparison. Second, the detection of AI-generated text has become increasingly difficult as generative models produce outputs with surface-level fluency that closely approximates human writing. Traditional stylometric approaches often rely on a single feature representation, which limits their discriminative power, while AI detection systems frequently depend on opaque, proprietary models whose decision boundaries are neither transparent nor reproducible.

### 2.2 Motivation

The motivation for developing InkID stems from the need for a transparent, interpretable, and reproducible system that addresses both authorship verification and AI text detection within a unified framework. Existing tools in this domain are frequently either proprietary, with undisclosed methodologies, or narrowly focused on a single detection task. InkID is designed to provide researchers, forensic analysts, and educators with an open-source, methodologically transparent tool that leverages well-understood statistical and information-theoretic techniques rather than black-box neural architectures. The emphasis on interpretability ensures that every scoring decision can be traced to specific linguistic features, enabling users to understand and validate the system's conclusions.

### 2.3 Objectives

The primary objectives of the InkID system are as follows. The first objective is to implement a dual-similarity authorship verification algorithm that combines character-level TF-IDF representations, which capture orthographic and morphological habits, with word-level TF-IDF representations, which capture lexical and topical preferences. The second objective is to develop a heuristic-based AI text detection module that utilizes Shannon word entropy, sentence-length variance as a proxy for burstiness, and average sentence length as complementary signals for distinguishing human-authored from machine-generated text. The third objective is to integrate both analytical pipelines into a cohesive web application with an intuitive user interface that presents results in an interpretable and actionable format. The fourth objective is to ensure that the system operates efficiently in-memory without requiring persistent storage, thereby minimizing deployment complexity and preserving user data privacy.

### 2.4 Scope and Limitations

The scope of InkID encompasses authorship verification for texts in the English language and AI detection for prose-style texts of sufficient length. The system is designed to operate on texts provided interactively through a web interface or programmatically via a RESTful API. Several limitations are inherent to the design. The authorship verification module performs optimally when at least three known writing samples are available per author; fewer samples reduce the reliability of the TF-IDF representations. The AI detection module requires a minimum of fifty words to produce meaningful results, with medium confidence thresholds requiring at least sixty words. The system is sensitive to text length, and short texts yield less reliable classifications across both modules. Topic similarity between known and test texts can confound authorship scores, as the word-level TF-IDF component partially captures topical overlap. Furthermore, a skilled human writer who deliberately mimics another's style, or an LLM output that has been heavily paraphrased, may evade detection by the heuristic-based signals employed in the AI detection module.

---

## 3. Literature Review and Related Work

### 3.1 Existing Solutions in Authorship Verification

Authorship attribution and verification have been active areas of research in computational linguistics for several decades. Early approaches relied on function word frequency analysis, as demonstrated by Mosteller and Wallace in their seminal analysis of the Federalist Papers, which established that stylistic markers such as prepositions, conjunctions, and articles serve as reliable authorial fingerprints. Subsequent research expanded the feature space to include character n-grams, part-of-speech tag distributions, syntactic parse tree features, and punctuation usage patterns.

Modern authorship verification systems predominantly employ machine learning classifiers trained on handcrafted stylometric features. The Writeprints framework, developed by Abbasi and Chen, extracts a comprehensive set of lexical, syntactic, and structural features and applies association rule mining to identify author-specific patterns. The JStylo system provides an open-source platform for stylometric analysis, supporting feature extraction and classification using standard machine learning algorithms. Commercial solutions such as Turnitin's Authorship Investigate apply similar principles within an educational integrity context.

### 3.2 Existing Solutions in AI Text Detection

The detection of AI-generated text has emerged as a distinct research area following the release of increasingly sophisticated language models. Approaches in this domain can be broadly categorized into three classes. The first class comprises classifier-based methods that train supervised models on labeled datasets of human and machine-generated text, using features such as perplexity, burstiness, and syntactic complexity. Tools such as GPTZero and Turnitin's AI detection module employ proprietary implementations of this approach. The second class includes watermarking techniques, wherein language models are modified during generation to embed detectable statistical patterns in their output, as proposed by Kirchenbauer et al. The third class encompasses heuristic-based methods that exploit known characteristics of LLM output, such as reduced lexical diversity, uniform sentence lengths, and elevated word-level entropy relative to human writing.

### 3.3 Limitations of Existing Systems

Existing authorship verification systems exhibit several limitations. Many rely on single-feature representations, such as character n-grams alone or function word frequencies alone, which capture only one dimension of an author's stylistic profile. Systems that employ complex feature sets with dozens or hundreds of dimensions often suffer from the curse of dimensionality when training data is limited, leading to overfitting. Furthermore, many commercial systems are proprietary, preventing independent validation of their methodologies and results.

AI text detection systems face distinct challenges. Classifier-based detectors are vulnerable to distributional shifts; a model trained on outputs from one generation of LLMs may perform poorly on outputs from newer models with different generation characteristics. Watermarking approaches require cooperation from model providers and are ineffective for detecting outputs from unwatermarked models. Heuristic-based methods, while transparent, often rely on thresholds calibrated on specific corpora that may not generalize across domains, genres, or languages.

### 3.4 Positioning of InkID

InkID addresses the identified limitations through several design choices. For authorship verification, the system employs a dual-similarity architecture that fuses character-level and word-level TF-IDF representations, capturing both sub-lexical stylistic habits and lexical preferences within a single scoring framework. The weighting scheme (sixty percent character-level, forty percent word-level) reflects the empirical observation that character n-grams are more robust to topic variation than word-level features. For AI detection, InkID adopts a transparent, heuristic-based approach using three information-theoretic and statistical signals whose individual contributions are reported to the user, enabling interpretability. The system avoids dependency on proprietary models or undisclosed thresholds, ensuring full reproducibility. By integrating both analytical capabilities into a single platform, InkID provides a comprehensive tool for text authentication that addresses complementary aspects of the authorship verification and AI detection problems.

---

## 4. System Overview

### 4.1 High-Level Architecture

InkID is structured as a single-page web application with a Python-based backend that serves both the user interface and the analytical API. The architecture follows a client-server model in which the client consists of a browser-rendered HTML page styled with Tailwind CSS and enhanced with vanilla JavaScript for asynchronous communication. The server is implemented using the FastAPI framework, an asynchronous Python web framework that provides automatic request validation, OpenAPI schema generation, and high-performance request handling through the ASGI protocol.

The backend is organized into two principal modules. The first module, designated as the web server module, handles HTTP routing, request parsing, response serialization, and template rendering. The second module, designated as the NLP analysis engine, encapsulates all computational logic for authorship verification and AI text detection. This modular separation ensures that the analytical core is decoupled from the presentation layer, enabling the analysis engine to be reused in alternative deployment contexts such as command-line interfaces or batch processing pipelines.

### 4.2 Key Components and Modules

The system comprises four principal components. The web interface component provides the user-facing application, including input forms for known author samples and test texts, result visualization panels with animated score indicators, and feature comparison tables. The routing and middleware component manages HTTP request dispatching, Cross-Origin Resource Sharing (CORS) policy enforcement, and error handling. The authorship verification component implements the dual-similarity algorithm with character and word TF-IDF vectorization, cosine similarity computation, score normalization, and confidence classification. The AI detection component implements the tri-signal ensemble comprising Shannon word entropy calculation, sentence-length variance computation, and average sentence length analysis.

### 4.3 System Workflow

The operational workflow of InkID proceeds through the following sequence. Upon initialization, the server loads the HTML template and serves it to the client in response to a GET request at the root endpoint. The user populates one or more text input fields with known writing samples attributed to the target author and enters the disputed or test text in a separate input field. Upon submission, the client serializes the input data as a multipart form and transmits it via an HTTP POST request to the `/analyze` endpoint. The server parses the request, extracting the list of known texts and the test text, and invokes the unified analysis function. This function sequentially executes the authorship verification pipeline and the AI detection pipeline on the provided inputs. The authorship verification pipeline preprocesses each text through dual preprocessing pathways, constructs TF-IDF matrices for character and word n-grams, computes cosine similarities between the concatenated known text representation and the test text representation, normalizes the raw similarity scores, computes the blended score, and assigns a classification label. The AI detection pipeline tokenizes the test text, computes the three detection signals, normalizes each signal to the unit interval, computes the blended AI probability score, and assigns a classification label. The results from both pipelines are merged into a unified response structure that includes numerical scores, classification labels, confidence assessments, explanatory text, and extracted linguistic features. The server serializes this response as JSON and returns it to the client, which dynamically renders the results in the designated result panels without requiring a page reload.

---

## 5. System Architecture

### 5.1 Architectural Style

InkID employs a layered monolithic architecture, which is appropriate for a system of its scale and operational requirements. The architecture consists of three logical layers: the presentation layer, the application layer, and the analysis layer. The presentation layer encompasses the HTML template, CSS styling, and client-side JavaScript responsible for user interaction and result visualization. The application layer encompasses the FastAPI routing logic, request validation, and response serialization. The analysis layer encompasses the NLP analysis engine, including all feature extraction, vectorization, similarity computation, and classification logic.

The monolithic architecture is selected over a microservices architecture due to the system's modest scale, the tight coupling between the analysis modules (which share preprocessing utilities and are invoked sequentially within a single request lifecycle), and the absence of a requirement for independent scaling of individual components. The architecture does, however, maintain clear modular boundaries within the monolith, such that the analysis engine could be extracted into an independent service if future requirements demand horizontal scaling of the computational layer.

### 5.2 Component Architecture

The component architecture of InkID can be described as a sequential pipeline with two parallel analytical branches within the analysis layer. At the top of the hierarchy, the Client Component (browser-based UI) interacts with the Server Component (FastAPI application) via HTTP. The Server Component contains the Route Handler, which dispatches incoming requests to the appropriate handler function. The Route Handler invokes the Analysis Orchestrator, which coordinates the execution of the two analytical branches.

The first analytical branch, the Authorship Verification Module, receives the known texts and test text as inputs. It delegates preprocessing to the Shared Helpers Module, which provides text normalization, tokenization, and stopword filtering functions. The preprocessed texts are then passed to the Character TF-IDF Vectorizer and the Word TF-IDF Vectorizer, which independently construct term-document matrices. The resulting vectors are passed to the Cosine Similarity Calculator, which computes pairwise similarities. The raw similarity scores are passed to the Score Normalizer, which maps them to the unit interval using empirically derived scaling parameters. The normalized scores are passed to the Blending Function, which computes the weighted sum, and subsequently to the Classification Function, which maps the blended score to a categorical label.

The second analytical branch, the AI Detection Module, receives the test text as input. It delegates tokenization to the Shared Helpers Module and then independently computes the Shannon Word Entropy, the Sentence-Length Variance, and the Average Sentence Length. Each signal is passed through a normalization function that maps its raw value to the unit interval. The normalized signals are passed to the Blending Function, which computes the weighted sum, and subsequently to the Classification Function, which maps the blended score to a categorical label with an associated confidence assessment.

Both analytical branches return their results to the Analysis Orchestrator, which merges them into a unified response structure that is returned to the Route Handler, serialized as JSON, and transmitted to the Client Component.

### 5.3 Data Flow and Interactions

The data flow through InkID follows a request-response pattern with in-memory data transformation at each stage. Input data enters the system as HTTP form data, which is parsed into Python string objects. These strings flow through the preprocessing pipeline, where they are transformed into token lists and normalized text representations. The tokenized representations are then vectorized into sparse TF-IDF matrices or aggregated into scalar statistical features, depending on the analytical branch. The vectorized and scalar features are transformed into similarity scores and signal values, which are normalized and blended into final classification scores. The scores are mapped to categorical labels and explanatory text, which are assembled into a JSON response object. This response is serialized and transmitted back to the client, where it is parsed and rendered as dynamic HTML content.

All data transformations occur in-memory; no intermediate results are persisted to disk or a database between requests. This design choice minimizes I/O overhead and ensures that each request is processed independently, providing inherent statelessness that facilitates horizontal scaling if required.

---

## 6. Detailed Module Design

### 6.1 Shared Helpers Module

The Shared Helpers Module provides foundational text processing utilities that are consumed by both the authorship verification and AI detection modules. Its purpose is to encapsulate common preprocessing operations, thereby avoiding code duplication and ensuring consistent text normalization across analytical pipelines.

The module exposes four principal functions. The `_alpha_words` function accepts a text string and returns a list of alphabetic tokens extracted via regular expression matching, filtering out tokens containing numeric or special characters. The `_preprocess_word` function accepts a text string, converts it to lowercase, removes punctuation, splits it into tokens, filters out stopwords, and returns the cleaned token list. The stopword list is sourced from NLTK's English stopword corpus when NLTK is available; otherwise, a built-in fallback list of common English stopwords is used. The `_preprocess_char` function accepts a text string, converts it to lowercase, and collapses multiple consecutive whitespace characters into single spaces, preserving punctuation and spacing patterns that are informative for character n-gram analysis. The `extract_features` function accepts a text string and computes eight human-readable linguistic statistics: word count, sentence count, average word length, average sentence length, number of unique words, lexical diversity (unique words divided by total words), punctuation density (punctuation characters divided by total characters), and paragraph count.

The internal logic of the module prioritizes robustness through graceful degradation. The NLTK dependency is handled with a try-except block; if NLTK is not installed, the module falls back to regex-based sentence tokenization using a pattern that matches sentence-ending punctuation followed by whitespace, and a built-in stopword list. This design ensures that the system remains functional even in minimal deployment environments where NLTK cannot be installed.

The module has an external dependency on the NumPy library for numerical operations and an optional dependency on NLTK for advanced tokenization. It has no internal dependencies on other application modules.

### 6.2 Authorship Verification Module

The Authorship Verification Module implements the dual-similarity algorithm for determining whether a test text was authored by the same individual who produced a set of known reference texts. Its purpose is to quantify stylistic similarity between the test text and the known texts across two complementary representation spaces.

The module accepts as input a list of known text strings and a single test text string. It produces as output a dictionary containing the blended similarity score, the character-level similarity score, the word-level similarity score, a categorical classification label, a confidence assessment, and an explanatory text string.

The internal logic proceeds through the following stages. First, each known text is preprocessed through both the character and word preprocessing pathways, producing two sets of representations. The character representations preserve punctuation and whitespace patterns, while the word representations are normalized and stopword-filtered. The known text representations in each pathway are concatenated into a single composite document. Second, a TF-IDF vectorizer is fitted on the corpus consisting of the concatenated known document and the test document. For the character pathway, the vectorizer uses the `char_wb` analyzer with an n-gram range of three to four characters and sublinear TF scaling (logarithmic term frequency). For the word pathway, the vectorizer uses the `word` analyzer with an n-gram range of one to two words (unigrams and bigrams), stopword removal, and sublinear TF scaling. Third, the TF-IDF vectors for the known composite document and the test document are extracted, and cosine similarity is computed between them for each pathway. Fourth, the raw cosine similarity scores are normalized to the unit interval using empirically derived scaling parameters. The character similarity score is normalized by subtracting a baseline of 0.15 and dividing by 0.70, then clipping to the range [0, 1]. The word similarity score is normalized by dividing by 0.35 and clipping to the range [0, 1]. Fifth, the normalized scores are blended using a weighted sum with weights of 0.60 for the character score and 0.40 for the word score. Sixth, the blended score is classified into one of four categories using threshold values: scores greater than or equal to 0.55 are classified as "Same Author" with high confidence, scores between 0.30 and 0.55 are classified as "Possibly Same" with medium confidence, scores between 0.12 and 0.30 are classified as "Possibly Different" with low confidence, and scores below 0.12 are classified as "Different Author" with high confidence.

The module depends on the Shared Helpers Module for preprocessing functions, on scikit-learn for TF-IDF vectorization and cosine similarity computation, and on NumPy for numerical array operations. It has no dependencies on the AI Detection Module, enabling independent execution and testing.

### 6.3 AI Detection Module

The AI Detection Module implements a heuristic-based tri-signal ensemble for estimating the probability that a given text was generated by a large language model. Its purpose is to exploit statistical regularities that differentiate human-authored prose from machine-generated text.

The module accepts as input a single text string. It produces as output a dictionary containing the blended AI probability score, the individual signal scores (entropy, variance, and length), a categorical classification label, a confidence assessment, and an explanatory text string.

The internal logic proceeds through the following stages. First, the input text is tokenized into words and sentences using the tokenization utilities from the Shared Helpers Module. A minimum length check is performed; texts with fewer than fifty words are flagged as too short for meaningful analysis. Second, Signal A (Shannon Word Entropy) is computed by calculating the frequency distribution of word unigrams, computing the probability of each unique word, and calculating the Shannon entropy as the negative sum of p(w) multiplied by log-base-2 of p(w) for each unique word. The raw entropy value is normalized to the unit interval by subtracting 4.0 and dividing by 2.5, then clipping to [0, 1]. This mapping reflects the empirical observation that human prose typically exhibits word entropy in the range of 3.5 to 5.5 bits, while LLM-generated prose typically exhibits entropy in the range of 5.0 to 7.0 bits. Third, Signal B (Sentence-Length Variance) is computed by calculating the word count of each sentence, computing the variance of these counts, and mapping the variance to the unit interval using an inverted linear transformation: the score is computed as 1.0 minus (variance minus 10.0) divided by 110.0, then clipped to [0, 1]. This inverted mapping reflects the observation that human writing exhibits high sentence-length variance (burstiness), while LLM output tends toward uniform sentence lengths. Variances above 120 correspond to strongly human-like burstiness, while variances below 10 correspond to strongly machine-like uniformity. Fourth, Signal C (Average Sentence Length) is computed by dividing the total word count by the total sentence count and mapping the result to the unit interval by subtracting 12.0 and dividing by 16.0, then clipping to [0, 1]. This mapping reflects the observation that human sentences average 12 to 18 words, while LLM sentences average 18 to 28 words. Fifth, the three normalized signals are blended using a weighted sum with weights of 0.50 for entropy, 0.30 for variance, and 0.20 for length. The higher weight assigned to entropy reflects its greater discriminative power in empirical evaluations. Sixth, the blended score is classified: scores greater than or equal to 0.65 are classified as "Possibly AI-Generated", scores between 0.40 and 0.65 are classified as "Uncertain", and scores below 0.40 are classified as "Likely Human-Written". Confidence is assessed as medium if the text contains at least sixty words and high otherwise.

The module depends on the Shared Helpers Module for tokenization, on NumPy for numerical computations including variance calculation, and on the Python standard library's math module for logarithmic operations. It has no dependencies on the Authorship Verification Module.

### 6.4 Web Server Module

The Web Server Module implements the HTTP interface for the InkID system. Its purpose is to handle incoming HTTP requests, delegate processing to the analysis engine, and format responses for consumption by the client.

The module exposes two routes. The GET route at the root path (`/`) renders the HTML template using Jinja2's template rendering engine and returns it as an HTML response. The POST route at the `/analyze` path accepts form data containing a list of known texts and a test text, invokes the unified analysis function from the analysis engine, and returns the result as a JSON response.

The module configures CORS middleware with permissive settings that allow requests from all origins, methods, and headers. This configuration facilitates development and local deployment but should be restricted in production environments. Error handling is implemented through a try-except block in the analysis route; exceptions are logged to the terminal with full stacktrace information, and a 500 Internal Server Error response is returned to the client with the error message.

The module depends on FastAPI for the web framework, Uvicorn for the ASGI server, Jinja2 for template rendering, python-multipart for form data parsing, and the analysis engine module for computational logic.

### 6.5 Frontend Interface Module

The Frontend Interface Module implements the client-side user interface for the InkID system. Its purpose is to provide an intuitive input mechanism for text data and a clear, visually informative presentation of analysis results.

The module is implemented as a single HTML file with embedded CSS and JavaScript. The layout uses a two-column responsive grid: the left panel contains the Known Author Profile section with dynamically addable textarea elements for multiple writing samples, and the right panel contains the Test Document section with a single textarea. The results section, initially hidden, is populated dynamically upon receipt of analysis results and contains a verdict panel with a color-coded classification label and confidence badge, an animated progress bar displaying the match score, four stat cards showing the character TF-IDF score, word TF-IDF score, sample count, and blended score, an AI detection card with a circular gauge visualization, and a feature breakdown grid comparing known and test text statistics.

The module's JavaScript contains two principal functions. The `analyze` function collects input values from the form fields, constructs a FormData object, sends a POST request to the `/analyze` endpoint, and passes the JSON response to the rendering function. The `renderResult` function parses the response object and populates all result UI elements, including label text, color coding, progress bar widths, gauge angles, and feature comparison values.

The module depends on Tailwind CSS (loaded via CDN) for styling, Lucide Icons (loaded via CDN) for iconography, Google Fonts for the JetBrains Mono and Plus Jakarta Sans typefaces, and the browser's Fetch API for asynchronous HTTP communication.

---

## 7. Database Design

### 7.1 Design Philosophy

InkID is designed as a stateless, in-memory analysis system that does not require persistent data storage. All text inputs, intermediate computational results, and analysis outputs exist only within the memory space of a single request lifecycle and are discarded upon response transmission. This design decision is motivated by several considerations. First, the analytical computations are computationally lightweight and do not benefit from caching or precomputation. Second, the absence of persistent storage eliminates the need for database administration, migration management, and backup procedures, thereby reducing operational complexity. Third, the stateless design inherently preserves user privacy, as no submitted texts are retained on the server beyond the duration of the request.

### 7.2 Hypothetical Schema Design

Although the current implementation does not include a database, the `.gitignore` configuration file includes a pattern for `*.sqlite3` files, indicating consideration for future persistent storage. Should persistent storage be introduced in a future iteration, the following schema is proposed.

The `authors` table would store author metadata with fields including `author_id` as the primary key (INTEGER, auto-increment), `name` as a text field (VARCHAR(255)), `created_at` as a timestamp (DATETIME, defaulting to the current timestamp), and `updated_at` as a timestamp (DATETIME, defaulting to the current timestamp and updating on modification).

The `text_samples` table would store individual writing samples with fields including `sample_id` as the primary key (INTEGER, auto-increment), `author_id` as a foreign key referencing `authors.author_id`, `text_content` as a text field (TEXT, non-null), `source` as an optional descriptor field (VARCHAR(255)), and `created_at` as a timestamp (DATETIME). An index on `author_id` would optimize queries retrieving all samples for a given author.

The `analysis_results` table would store the outcomes of analysis requests with fields including `result_id` as the primary key (INTEGER, auto-increment), `test_text` as a text field (TEXT, non-null), `known_author_id` as an optional foreign key referencing `authors.author_id`, `authorship_score` as a floating-point value (REAL), `authorship_label` as a categorical field (VARCHAR(50)), `ai_detection_score` as a floating-point value (REAL), `ai_detection_label` as a categorical field (VARCHAR(50)), and `analyzed_at` as a timestamp (DATETIME).

### 7.3 Justification of Design Choices

The choice of SQLite for the hypothetical schema is motivated by its zero-configuration deployment model, its suitability for read-heavy workloads with moderate write volumes, and its compatibility with Python through the built-in `sqlite3` module. For production deployments requiring higher concurrency, a migration to PostgreSQL would be advisable, given its superior handling of concurrent write operations, its support for advanced indexing strategies, and its robustness in multi-user environments. The normalization of the schema into separate `authors`, `text_samples`, and `analysis_results` tables follows standard relational design principles, eliminating data redundancy and ensuring referential integrity through foreign key constraints.

---

## 8. Algorithms and Logic

### 8.1 Dual-Similarity Authorship Verification Algorithm

The core algorithm for authorship verification in InkID is a dual-similarity approach that computes stylistic similarity across two complementary text representation spaces. The algorithm is formalized as follows.

**Input**: A set of known texts K = {k_1, k_2, ..., k_n} and a test text t.

**Step 1 -- Preprocessing**. For each text in K and for t, compute two representations: a character-level representation obtained by lowercasing and collapsing whitespace, and a word-level representation obtained by lowercasing, removing punctuation, tokenizing, and removing stopwords.

**Step 2 -- Concatenation**. Concatenate all character-level representations of texts in K into a single string K_char. Concatenate all word-level representations into a single string K_word.

**Step 3 -- Character TF-IDF Vectorization**. Construct a TF-IDF vectorizer V_char with parameters: analyzer = `char_wb`, ngram_range = (3, 4), sublinear_tf = True. Fit V_char on the corpus [K_char, t_char]. Transform both documents to obtain vectors v_K_char and v_t_char.

**Step 4 -- Word TF-IDF Vectorization**. Construct a TF-IDF vectorizer V_word with parameters: analyzer = `word`, ngram_range = (1, 2), sublinear_tf = True. Fit V_word on the corpus [K_word, t_word]. Transform both documents to obtain vectors v_K_word and v_t_word.

**Step 5 -- Cosine Similarity Computation**. Compute the cosine similarity between v_K_char and v_t_char, denoted raw_c. Compute the cosine similarity between v_K_word and v_t_word, denoted raw_w.

**Step 6 -- Score Normalization**. Normalize the character similarity score as char_sim = clip((raw_c - 0.15) / 0.70, 0, 1). Normalize the word similarity score as word_sim = clip(raw_w / 0.35, 0, 1).

**Step 7 -- Score Blending**. Compute the blended score as blended = char_sim * 0.60 + word_sim * 0.40.

**Step 8 -- Classification**. Assign a label based on threshold values: if blended >= 0.55, return "Same Author" with high confidence; if blended >= 0.30, return "Possibly Same" with medium confidence; if blended >= 0.12, return "Possibly Different" with low confidence; otherwise, return "Different Author" with high confidence.

**Output**: A dictionary containing blended, char_sim, word_sim, label, confidence, and explanatory text.

### 8.2 Complexity Analysis of Authorship Verification

The time complexity of the authorship verification algorithm is dominated by the TF-IDF vectorization and cosine similarity computation steps. Let N be the total number of tokens (characters or words) across all input texts, and let D be the dimensionality of the TF-IDF vocabulary. The preprocessing step operates in O(N) time. The TF-IDF vectorization step operates in O(N * D) time for fitting and O(N * D) time for transformation, where D is bounded by the vocabulary size, which in turn is bounded by N. The cosine similarity computation operates in O(D) time. The normalization and blending steps operate in O(1) time. Therefore, the overall time complexity is O(N * D), which in the worst case is O(N^2) when the vocabulary size is proportional to the input size. In practice, D is significantly smaller than N due to the repetition of common n-grams, yielding near-linear performance for typical text inputs.

The space complexity is O(D) for storing the TF-IDF vocabulary and O(D) for storing the sparse TF-IDF vectors, yielding an overall space complexity of O(D). For character n-grams with n in [3, 4], D is bounded by 26^n for alphabetic characters, though in practice it is much smaller due to the constraint that n-grams must appear in the input text.

### 8.3 AI Detection Algorithm

The AI detection algorithm employs a tri-signal ensemble based on information-theoretic and statistical properties of the input text.

**Input**: A text string t.

**Step 1 -- Tokenization**. Tokenize t into a list of words W and a list of sentences S. If |W| < 50, return a result indicating insufficient text length.

**Step 2 -- Signal A: Shannon Word Entropy**. Compute the frequency distribution of words in W. For each unique word w, compute its probability p(w) = count(w) / |W|. Compute the Shannon entropy H = -sum over all unique w of p(w) * log_2(p(w)). Normalize as ent_score = clip((H - 4.0) / 2.5, 0, 1).

**Step 3 -- Signal B: Sentence-Length Variance**. Compute the word count c_i for each sentence s_i in S. Compute the variance V = (1 / |S|) * sum over all i of (c_i - mean(c))^2. Normalize as var_score = clip(1.0 - (V - 10.0) / 110.0, 0, 1).

**Step 4 -- Signal C: Average Sentence Length**. Compute the average sentence length L = |W| / |S|. Normalize as len_score = clip((L - 12.0) / 16.0, 0, 1).

**Step 5 -- Score Blending**. Compute the blended AI probability as ai_prob = ent_score * 0.50 + var_score * 0.30 + len_score * 0.20.

**Step 6 -- Classification**. If ai_prob >= 0.65, return "Possibly AI-Generated". If ai_prob >= 0.40, return "Uncertain". Otherwise, return "Likely Human-Written". Confidence is assessed as medium if |W| >= 60.

**Output**: A dictionary containing ai_prob, ent_score, var_score, len_score, label, confidence, and explanatory text.

### 8.4 Complexity Analysis of AI Detection

The time complexity of the AI detection algorithm is as follows. The tokenization step operates in O(N) time, where N is the number of characters in the input text. The Shannon entropy computation requires a single pass over the word list to build the frequency distribution (O(|W|) time) and a second pass over the unique words to compute the entropy (O(|W_unique|) time), yielding O(|W|) overall. The sentence-length variance computation requires a single pass over the sentences to compute word counts (O(|S| * avg_words_per_sentence) = O(|W|) time) and a second pass to compute the variance (O(|S|) time), yielding O(|W|) overall. The average sentence length computation operates in O(1) time given the precomputed values. The blending and classification steps operate in O(1) time. Therefore, the overall time complexity is O(N), linear in the input size.

The space complexity is O(|W_unique|) for storing the word frequency distribution and O(|S|) for storing the per-sentence word counts, yielding an overall space complexity of O(N) in the worst case.

---

## 9. Technology Stack

### 9.1 Backend Framework: FastAPI

The backend of InkID is implemented using FastAPI version 0.111.0, a modern Python web framework built on Starlette and Pydantic. FastAPI was selected for several reasons. Its native support for asynchronous request handling through the ASGI protocol enables efficient processing of concurrent requests without the overhead of thread-per-request models. Its automatic request validation and response serialization, powered by Python type hints, reduces boilerplate code and minimizes the risk of data integrity errors. Its automatic generation of OpenAPI (Swagger) documentation provides a machine-readable specification of the API, facilitating integration testing and third-party development. Its performance characteristics, which are comparable to Node.js and Go frameworks due to its foundation on Starlette, ensure that the computational overhead of the web layer is negligible relative to the NLP analysis computations.

### 9.2 ASGI Server: Uvicorn

Uvicorn version 0.30.1 serves as the ASGI server for InkID. Uvicorn is an ASGI server implementation built on uvloop and httptools, providing high-performance HTTP handling. It was selected for its compatibility with FastAPI, its low resource footprint, and its support for hot reloading during development, which accelerates the development cycle. In production deployments, Uvicorn can be run with multiple worker processes to utilize multi-core processors.

### 9.3 Template Engine: Jinja2

Jinja2 version 3.1.4 is used for server-side rendering of the HTML interface. Jinja2 was selected for its expressive template syntax, its security features (including automatic HTML escaping), and its seamless integration with FastAPI through the `Jinja2Templates` utility class. While the InkID interface is primarily rendered client-side through dynamic JavaScript, Jinja2 is used to serve the initial HTML shell that loads the CSS, JavaScript, and font resources.

### 9.4 NLP and Machine Learning: scikit-learn

scikit-learn version 1.3.0 or higher provides the TF-IDF vectorization and cosine similarity computation capabilities that form the foundation of the authorship verification algorithm. scikit-learn was selected for its well-optimized implementations of text vectorization algorithms, its extensive parameter configurability (enabling fine-tuning of n-gram ranges, analyzer types, and TF scaling strategies), and its mature, well-tested codebase. The `TfidfVectorizer` class provides a single interface for both vocabulary construction and vector transformation, simplifying the implementation of the dual-similarity pipeline.

### 9.5 Tokenization: NLTK

The Natural Language Toolkit (NLTK) version 3.8.0 or higher provides word and sentence tokenization utilities for the AI detection module. NLTK was selected for its well-established tokenization algorithms, particularly the Punkt sentence tokenizer, which handles abbreviations, decimal numbers, and other edge cases in English sentence boundary detection. NLTK is implemented as an optional dependency with a regex-based fallback, ensuring that the system remains functional in environments where NLTK installation is not feasible.

### 9.6 Numerical Computing: NumPy

NumPy version 1.24.0 or higher provides numerical array operations, including variance computation and vector arithmetic, that underpin both analytical modules. NumPy was selected for its performance advantages over pure Python implementations of numerical operations, its extensive library of mathematical functions, and its role as a foundational dependency for scikit-learn.

### 9.7 Frontend: Tailwind CSS and Vanilla JavaScript

The frontend of InkID is styled using Tailwind CSS, loaded via CDN, and enhanced with vanilla JavaScript. Tailwind CSS was selected for its utility-first approach, which enables rapid prototyping and consistent styling without the overhead of a component library. Vanilla JavaScript was selected over a frontend framework (such as React or Vue.js) due to the simplicity of the client-side logic, which requires only form submission and result rendering without complex state management or routing. The use of CDN-loaded resources eliminates the need for a build pipeline, simplifying deployment.

### 9.8 Form Data Parsing: python-multipart

The python-multipart library version 0.0.9 is used for parsing multipart form data submitted by the client. It is a required dependency for FastAPI when handling form submissions, as FastAPI's default request parsing handles only JSON-encoded bodies.

---

## 10. Security Considerations

### 10.1 Authentication and Authorization

The current implementation of InkID does not include authentication or authorization mechanisms. The system is designed as a publicly accessible analysis tool, and all endpoints are available without credential verification. For production deployments where access control is required, authentication should be implemented using JSON Web Tokens (JWT) or session-based authentication. FastAPI's dependency injection system provides a natural integration point for authentication middleware, and the `OAuth2PasswordBearer` utility class can be used to implement token-based authentication with minimal code changes. Authorization, if required, could be implemented through role-based access control (RBAC), distinguishing between regular users who can submit texts for analysis and administrators who can manage stored data (if a database is introduced).

### 10.2 Data Protection

InkID's stateless, in-memory architecture provides inherent data protection, as submitted texts are not persisted beyond the request lifecycle. This design eliminates the risk of data breaches through database compromise and ensures compliance with data minimization principles. However, several data protection considerations remain relevant. In transit, data should be protected through HTTPS encryption; in production deployments, the server should be configured behind a reverse proxy (such as Nginx) that terminates SSL/TLS connections. At rest, if persistent storage is introduced in a future iteration, text content should be encrypted using AES-256 encryption, with encryption keys managed through a dedicated key management service. Input validation should be implemented to prevent excessively large text submissions that could trigger denial-of-service conditions through memory exhaustion; the current implementation does not enforce input size limits.

### 10.3 Threat Modeling

A threat model for InkID identifies the following attack vectors and corresponding mitigations. Cross-Site Scripting (XSS) attacks are mitigated by Jinja2's automatic HTML escaping, which prevents the injection of malicious scripts through template variables, and by the fact that analysis results are rendered client-side using `textContent` property assignments rather than `innerHTML`, preventing the execution of injected scripts in result displays. Cross-Site Request Forgery (CSRF) attacks are not directly mitigated in the current implementation, as the system does not use session-based authentication; however, the POST-only nature of the analysis endpoint provides partial protection. In production, CSRF tokens should be implemented if session-based authentication is introduced. Denial-of-Service (DoS) attacks through excessive text submission are not mitigated in the current implementation; rate limiting should be implemented at the reverse proxy level or through middleware to restrict the number of requests per client per time window. Dependency supply chain attacks are mitigated by pinning dependency versions in the `requirements.txt` file and by using the `--trusted-host` flag when installing packages from verified sources.

---

## 11. Performance and Scalability

### 11.1 Expected Load

InkID is designed for interactive, user-driven analysis requests rather than high-throughput batch processing. The expected load profile consists of sporadic requests from individual users, each request involving the analysis of a test text against a small set of known samples (typically three to ten texts of moderate length). Under this load profile, the system is expected to handle concurrent requests from tens of users without performance degradation, given the modest computational requirements of the analysis algorithms. A single analysis request on a modern CPU typically completes within one to three seconds for texts of up to five thousand words, with the majority of the computation time consumed by TF-IDF vectorization.

### 11.2 Optimization Strategies

Several optimization strategies are employed or recommended for InkID. The TF-IDF vectorization step uses scikit-learn's optimized sparse matrix representations, which minimize memory usage and accelerate linear algebra operations on the typically sparse term-document matrices. Sublinear TF scaling (logarithmic term frequency) is applied, which reduces the influence of high-frequency terms and improves the quality of similarity scores without additional computational cost. The use of character n-grams with a bounded range (3 to 4 characters) limits the vocabulary size of the character vectorizer, preventing excessive dimensionality. For AI detection, the use of O(N) algorithms ensures that processing time scales linearly with text length, avoiding the quadratic or higher-order complexity that would arise from pairwise comparison approaches.

Further optimization strategies that could be implemented include: caching TF-IDF vectorizers for known authors whose sample texts do not change frequently, thereby avoiding redundant vectorization on repeated queries; implementing asynchronous processing for long texts to prevent blocking the request thread; and precomputing and storing the TF-IDF representations of known texts in a persistent cache (such as Redis) to eliminate recomputation.

### 11.3 Scalability Approach

The stateless, in-memory design of InkID provides inherent horizontal scalability. Individual request processing is independent, with no shared state between requests, enabling the deployment of multiple server instances behind a load balancer. In a horizontally scaled configuration, each instance would process requests independently, and the load balancer would distribute incoming requests across instances using a round-robin or least-connections algorithm.

For deployments requiring higher throughput, the analysis engine could be decoupled from the web server and deployed as an independent worker service. In this configuration, the web server would enqueue analysis requests into a message broker (such as RabbitMQ or Redis Streams), and a pool of worker processes would consume requests from the queue, execute the analysis, and return results through a response channel. This architecture would enable independent scaling of the web tier and the computational tier, optimizing resource allocation based on the relative load on each component.

---

## 12. Implementation Details

### 12.1 Development Methodology

InkID was developed using an iterative, prototype-driven methodology. The initial implementation focused on establishing the core analytical algorithms (dual-similarity authorship verification and tri-signal AI detection) in an isolated Python module, with validation performed against manually crafted test cases. Once the analytical core was validated, the web server layer was implemented to expose the analysis functions through HTTP endpoints. The frontend interface was developed in parallel, with incremental refinement of the layout, styling, and result visualization components. Testing was performed continuously throughout development, with each analytical function validated against known inputs and expected outputs.

### 12.2 Tools and Frameworks

The development of InkID utilized the following tools and frameworks. Python 3 serves as the implementation language, selected for its extensive ecosystem of NLP and machine learning libraries. Visual Studio Code or any equivalent Python IDE serves as the development environment, with linting provided by Ruff or Flake8 and formatting provided by Black. Git serves as the version control system, with commits organized around discrete functional changes. Virtual environments (venv or conda) are used for dependency isolation, ensuring reproducible development environments. The project dependencies are specified in a `requirements.txt` file with pinned version numbers, enabling deterministic environment reconstruction.

### 12.3 Version Control Strategy

The version control strategy for InkID follows a feature-branch workflow on Git. The main branch contains the stable, production-ready codebase. Feature branches are created for individual enhancements or bug fixes, reviewed through pull requests (if a collaborative workflow is used), and merged into the main branch upon validation. Commit messages follow a conventional format, with a short summary line describing the change and an optional body providing additional context. Tagging is used to mark release versions, following semantic versioning principles (major.minor.patch). The `.gitignore` file excludes build artifacts, Python bytecode files, virtual environment directories, IDE configuration files, and NLTK data downloads, ensuring that only source code and configuration files are tracked in the repository.

---

## 13. Testing Strategy

### 13.1 Unit Testing

Unit testing for InkID targets the individual functions within the analysis engine, validating their correctness against known inputs and expected outputs. Each preprocessing function should be tested with representative inputs, including edge cases such as empty strings, single-word texts, and texts containing only punctuation. The TF-IDF vectorization and similarity computation should be tested with controlled corpora where the expected similarity scores can be manually verified. The score normalization functions should be tested with boundary values to confirm correct clipping behavior. The classification functions should be tested with scores at, above, and below each threshold to verify correct label assignment. The AI detection signals should be tested with texts of known characteristics (e.g., text with deliberately high or low entropy, text with uniform or varied sentence lengths) to confirm correct signal computation and normalization. A testing framework such as pytest should be used, with test fixtures providing reusable test data and parametrized tests enabling efficient coverage of multiple input scenarios.

### 13.2 Integration Testing

Integration testing for InkID validates the end-to-end behavior of the system, from HTTP request submission to response rendering. Tests should verify that the GET route correctly renders the HTML template, that the POST route correctly parses form data and returns valid JSON responses, and that the CORS middleware correctly handles cross-origin requests. The unified analysis function should be tested with realistic input combinations, including cases where the known texts and test text are from the same author, from different authors, and from a mixture of human and AI sources. Error handling should be tested by submitting malformed requests (e.g., missing fields, empty text bodies) and verifying that appropriate error responses are returned. Integration tests should be implemented using the `TestClient` utility provided by FastAPI, which enables testing of the application without requiring a running server instance.

### 13.3 Performance Testing

Performance testing for InkID evaluates the system's response time and resource utilization under varying load conditions. Response time should be measured for texts of increasing length (e.g., 100 words, 500 words, 1000 words, 5000 words) to verify that processing time scales linearly as predicted by the complexity analysis. Concurrent request handling should be tested using a load testing tool such as Apache JMeter or Locust, simulating multiple simultaneous users to identify the system's throughput limit and the point at which response times degrade. Memory usage should be monitored during processing of large texts to verify that the sparse matrix representations of TF-IDF vectors do not cause excessive memory consumption. The results of performance testing should inform the configuration of server instances (e.g., number of Uvicorn workers) and the deployment of rate limiting policies.

---

## 14. Results and Expected Outcomes

### 14.1 Expected System Behavior

Upon successful deployment, InkID is expected to provide accurate and interpretable authorship verification and AI text detection results for English-language texts of sufficient length. For authorship verification, the system is expected to produce high similarity scores (above 0.55) when the test text is authored by the same individual as the known samples, and low similarity scores (below 0.12) when the test text is authored by a different individual, assuming the known samples are representative of the author's style and the texts are of adequate length (at least 200 words each). Intermediate scores (between 0.12 and 0.55) are expected when the test text exhibits partial stylistic overlap with the known samples, such as when the author's style has evolved over time or when the test text covers a significantly different topic.

For AI detection, the system is expected to produce high AI probability scores (above 0.65) for text generated by contemporary large language models without post-processing, and low AI probability scores (below 0.40) for text written by humans without deliberate stylometric manipulation. Intermediate scores (between 0.40 and 0.65) are expected for text that exhibits mixed characteristics, such as human-written text that has been lightly edited by an AI assistant, or AI-generated text that has been substantially paraphrased by a human editor.

### 14.2 Evaluation Metrics

The performance of InkID can be evaluated using standard classification metrics computed over a labeled dataset. For authorship verification, the evaluation dataset should consist of pairs of texts labeled as "same author" or "different author," and the system's predictions should be evaluated using accuracy, precision, recall, and F1-score at each classification threshold. The Area Under the Receiver Operating Characteristic Curve (AUROC) should be computed to assess the system's discriminative power across all possible threshold values. For AI detection, the evaluation dataset should consist of texts labeled as "human-written" or "AI-generated," and the same metrics should be computed. Additionally, the calibration of the system's probability scores should be assessed by comparing the predicted probabilities with the observed frequencies of positive cases in binned score ranges, using metrics such as the Brier score or Expected Calibration Error (ECE).

The interpretability of the system's outputs should be evaluated through user studies, in which participants are presented with analysis results and asked to assess their confidence in the system's conclusions. High interpretability is indicated by participants' ability to understand the basis for each classification decision and to identify cases where the system's conclusion may be unreliable (e.g., due to insufficient text length or topic mismatch).

---

## 15. Future Scope

### 15.1 Semantic Embedding Integration

A significant enhancement to the authorship verification module would be the integration of semantic text embeddings, such as those produced by transformer-based models (e.g., Sentence-BERT or OpenAI's text embedding models). Semantic embeddings capture the meaning and contextual usage of text at a level that is complementary to the surface-level stylistic features captured by TF-IDF representations. By computing cosine similarity between the semantic embeddings of known and test texts and incorporating this similarity as a third component in the blended score, the system could improve its robustness to topic variation and its sensitivity to deeper authorial characteristics such as argumentation style and conceptual framing. The integration would require careful weighting of the semantic similarity component relative to the existing character and word components, and would introduce a dependency on an embedding model, which could be hosted locally (for open-source models) or accessed via an API (for proprietary models).

### 15.2 Dynamic Threshold Calibration

The classification thresholds used in both the authorship verification and AI detection modules are currently fixed values derived from empirical observation on limited datasets. A more sophisticated approach would implement dynamic threshold calibration, in which the thresholds are adjusted based on the characteristics of the input texts and the available reference data. For example, the authorship verification thresholds could be lowered when the known samples are highly consistent with each other (indicating a stable authorial style) and raised when the known samples exhibit high internal variance (indicating a variable style). Similarly, the AI detection thresholds could be adjusted based on the domain of the input text (e.g., academic prose vs. creative writing), as different domains exhibit different baseline characteristics for entropy, burstiness, and sentence length. Dynamic calibration would require the collection and analysis of domain-specific corpora and the implementation of adaptive threshold selection algorithms.

### 15.3 Multi-Author Classification

The current authorship verification module operates in a binary verification mode: given a set of known samples from a single author, it determines whether the test text matches that author. An extension to this model would support multi-author classification, in which known samples from multiple authors are provided, and the system identifies which author (if any) is most likely to have written the test text. This would require modifying the dual-similarity algorithm to compute similarity scores against each author's known samples independently, and then applying a classification rule (e.g., selecting the author with the highest score above a confidence threshold, or returning "unknown" if no author exceeds the threshold). Multi-author classification would broaden the system's applicability to scenarios such as historical authorship attribution, where the candidate author pool is known but the true author is unknown.

### 15.4 Feature Importance Visualization

The current implementation reports numerical feature values (word count, sentence count, lexical diversity, etc.) in the feature breakdown panel but does not indicate the relative importance of each feature in the classification decision. An enhancement would implement feature importance visualization, using techniques such as SHAP (SHapley Additive exPlanations) values or LIME (Local Interpretable Model-agnostic Explanations) to quantify the contribution of each feature to the final classification score. For the authorship verification module, this would involve computing feature-level attributions for the TF-IDF vectors, identifying which character n-grams and word n-grams contribute most to the similarity score. For the AI detection module, this would involve decomposing the blended score into the contributions of each signal and reporting the individual signal values alongside their weights. Feature importance visualization would enhance the interpretability of the system's outputs and provide users with actionable insights into the linguistic characteristics that differentiate the texts under analysis.

### 15.5 Language Support Expansion

The current implementation is designed for English-language texts, with English-specific stopword lists, tokenization rules, and normalization parameters. Expansion to support additional languages would require the incorporation of language-specific resources (stopword lists, tokenization models) and the recalibration of normalization parameters and classification thresholds for each supported language. The modular design of the preprocessing and analysis functions facilitates this expansion, as language-specific resources can be selected based on a language identifier parameter. Priority languages for expansion would include those with large digital text corpora available for threshold calibration, such as Spanish, French, German, and Chinese.

---

## 16. Conclusion

InkID presents a comprehensive, transparent, and reproducible system for stylometric authorship verification and AI-generated text detection. The system's dual-similarity authorship verification algorithm combines character-level and word-level TF-IDF representations to capture complementary dimensions of authorial style, while its tri-signal AI detection ensemble leverages information-theoretic and statistical indicators to distinguish human-authored from machine-generated text. The integration of both analytical capabilities within a single, stateless web application provides a unified platform for text authentication that is accessible to researchers, forensic analysts, and educators.

The architectural decisions underlying InkID -- including the selection of a monolithic layered architecture, the use of interpretable statistical and information-theoretic methods over black-box neural models, and the adoption of a stateless in-memory processing model -- reflect a commitment to transparency, reproducibility, and operational simplicity. The system's modular design facilitates future enhancements, including semantic embedding integration, dynamic threshold calibration, multi-author classification, feature importance visualization, and multilingual support.

The contributions of this work are threefold. First, InkID demonstrates the viability of a hybrid NLP approach to authorship verification that fuses sub-lexical and lexical feature representations within a single scoring framework, achieving robustness to topic variation through the elevated weighting of character-level features. Second, InkID provides a transparent, heuristic-based alternative to proprietary AI detection systems, with fully documented signal definitions, normalization procedures, and classification thresholds that enable independent validation and reproducible results. Third, InkID establishes a reference implementation for a unified text authentication platform that addresses the complementary challenges of authorship verification and AI text detection within a single, accessible interface.

As the capabilities of generative language models continue to advance, the need for reliable, interpretable text authentication tools will only intensify. InkID provides a foundation for such tools, grounded in established computational linguistics principles and designed for extensibility in response to emerging challenges in the domain of digital text authentication.
