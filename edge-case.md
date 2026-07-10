# Edge Cases and Corner Scenarios

This document lists important edge cases for the AI-powered restaurant recommendation system so the implementation can be made robust and user-friendly.

---

## 1. User Input Edge Cases

### 1.1 Missing or blank values
- Location is left empty.
- Cuisine is not provided.
- Budget is not selected.
- Minimum rating is omitted.
- Additional preferences are left blank.

### 1.2 Invalid values
- Location contains only spaces or special characters.
- Budget value is not one of: low, medium, high.
- Minimum rating is negative, greater than 5, or non-numeric.
- Cuisine is passed as an unsupported or empty string.

### 1.3 Unexpected input formats
- Cuisine provided as a list, comma-separated string, or mixed casing.
- Additional preferences include irrelevant text, emojis, or long paragraphs.
- User enters very short or very long free-text input.

### 1.4 Ambiguous preferences
- User requests a cuisine that does not exist in the dataset.
- User asks for a city that has few or no matching restaurants.
- User selects a strict minimum rating that filters out almost everything.

---

## 2. Dataset Edge Cases

### 2.1 Missing data fields
- Restaurant name is missing.
- Cuisine field is empty or null.
- Rating is missing.
- Cost field is missing or unparseable.
- Location is absent.

### 2.2 Invalid data values
- Rating is stored as text like "Not rated".
- Cost is given as a string that cannot be parsed to a number.
- Duplicate restaurant entries appear in the dataset.
- Same restaurant exists with slightly different spelling or casing.

### 2.3 Unusual dataset content
- Restaurants with multiple cuisines.
- Restaurants listed in cities with regional aliases such as Bengaluru vs Bangalore.
- Very low or very high cost entries.
- Restaurants with extremely high votes but low rating.

### 2.4 Large dataset behavior
- Dataset load takes too long.
- Memory usage becomes high during preprocessing.
- Many restaurants match the same filter combination.

---

## 3. Filtering Edge Cases

### 3.1 No matches after filtering
- No restaurant satisfies the selected location and cuisine.
- The minimum rating is too high for the available data.
- Budget tier excludes all available options.

### 3.2 Too many matches
- Hundreds of restaurants match the filters.
- The system must limit the candidate set passed to the LLM.

### 3.3 Partial matches
- A restaurant matches location and rating but not cuisine.
- A restaurant matches cuisine and budget but not location.
- Some filters are applied and others are ignored due to invalid input.

---

## 4. LLM and Prompting Edge Cases

### 4.1 LLM API failure
- API key is missing or invalid.
- Groq service is down or returns timeout errors.
- Request limit or quota is exceeded.

### 4.2 Invalid LLM response
- The model returns malformed JSON.
- The model returns restaurant IDs that are not in the candidate list.
- The model returns fewer recommendations than requested.
- The model invents restaurants that are not present in the dataset.

### 4.3 Prompt-related issues
- Candidate list is too large for the prompt context window.
- The prompt contains too much free-text input.
- The model produces inconsistent explanations.

### 4.4 Low-quality recommendations
- The model ranks restaurants purely by generic popularity rather than user preference.
- Explanations are too vague or repetitive.
- The model ignores budget or rating constraints.

---

## 5. Fallback and Recovery Edge Cases

### 5.1 LLM unavailable
- The application should fall back to deterministic rule-based ranking.
- The UI should clearly indicate that AI explanations are unavailable.

### 5.2 Invalid fallback output
- Rule-based ranking returns duplicate items.
- Ranking order is unstable when ratings and votes tie.

### 5.3 Retry behavior
- A transient API error occurs once and then succeeds.
- The system should retry gracefully within a bounded limit.

---

## 6. UI and User Experience Edge Cases

### 6.1 Empty results display
- No restaurants are found after filtering.
- The UI should show a friendly message and suggest relaxing filters.

### 6.2 Rendering issues
- Long restaurant names overflow the card layout.
- Explanations are too long for display.
- Special characters or unicode text render incorrectly.

### 6.3 Interaction issues
- User submits the form with no valid inputs.
- The app becomes slow when loading the dataset for the first time.
- The UI should show a loading state while processing.

---

## 7. Performance and Reliability Edge Cases

### 7.1 Slow startup
- Dataset takes a long time to load on first run.
- The app should support caching or lazy loading where possible.

### 7.2 High memory usage
- Dataset preprocessing consumes large amounts of memory.
- The system should avoid unnecessary copies of data.

### 7.3 Timeout issues
- Network access to Hugging Face or Groq is slow or interrupted.
- The app should fail gracefully and preserve a usable experience.

---

## 8. Security and Safety Edge Cases

### 8.1 Prompt injection
- User enters text that attempts to manipulate the LLM prompt.
- The system should sanitize or constrain free-text input before sending it to the model.

### 8.2 Secret handling
- API keys are accidentally committed to source control.
- Environment variables should be used and kept out of version control.

---

## 9. Recommended Handling Strategy

For each edge case, the system should:
- validate input before processing,
- provide safe defaults where possible,
- degrade gracefully when external services fail,
- return clear, understandable feedback to the user,
- avoid hallucinated or unsupported recommendations.

---

## 10. Summary Checklist

The implementation should explicitly handle:
- empty or invalid user inputs,
- missing or malformed dataset values,
- zero-result and over-result filter scenarios,
- LLM API errors and malformed outputs,
- UI empty-state and loading-state behavior,
- performance bottlenecks and timeout issues,
- prompt injection and secret safety concerns.
