# ScamSathi

**A second look at suspicious messages. Built for Nepal.**

ScamSathi helps people examine SMS, WhatsApp messages, and emails before responding, sending money, or sharing private information. It uses Gemma 4 to interpret English, Nepali, and Romanized Nepali messages, explain possible warning signs, and suggest practical next steps.

It is an educational screening prototype. It does not verify senders or websites, and a low-risk assessment is not a guarantee of safety.

## Why this project

A scam can look like a routine KYC request, a prize notification, or a job offer. Messages written in Romanized Nepali add context that a simple English keyword filter can miss. ScamSathi explores whether a language model can make the warning signs easier to understand. Its accuracy across these languages has not been measured on a representative dataset.

## What it does

- Accepts up to 4,000 characters of message text.
- Provides four one-click samples, including an ordinary class reminder.
- Shows HIGH, MEDIUM, LOW, or UNCERTAIN indicators, a plain-English explanation, possible warning signs, and safer next steps.
- Lets users save the assessment as a text file.
- Marks results as stale after a message is edited and removes an old result when a new request fails.
- Presents a focused two-column desktop layout that stacks on narrow screens.

## Stack and flow

Python · Streamlit · Google Gen AI SDK · `gemma-4-26b-a4b-it`

1. Streamlit validates the length of the submitted text.
2. `analyze()` asks the hosted model for a structured assessment, using a prompt that treats the message as untrusted input.
3. `parse_analysis()` parses and normalizes the response into a consistent shape.
4. The UI escapes model-supplied text before rendering custom HTML and displays the result.
5. `format_report()` builds a downloadable plain-text assessment.

Prompt instructions reduce some misuse but are not a complete prompt-injection defense. No links in the submitted message are fetched.

## Run locally on Windows

Open PowerShell **in the project root**, where `app.py` and `requirements.txt` are located:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Using the virtual environment's Python directly avoids PowerShell activation-policy problems. If `py` is unavailable, use `python -m venv .venv` for the first command.

Open the local URL printed by Streamlit. Enter your Google AI Studio key in **Connection settings**. Alternatively, create `.streamlit/secrets.toml` locally:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

The secret file is ignored by Git. Never paste a real key into source code or the README.

## Update an existing Streamlit Cloud app

Commit the updated project to the same repository and branch your app already uses. Keep `app.py` as the entrypoint. Include `.streamlit/config.toml`; it supplies the default theme.

In [Streamlit Community Cloud](https://share.streamlit.io/), open the app's **Settings → Secrets** and set:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

When a server key is configured, visitors do not see the key-entry controls. Verify the public deployment in a private browser window. If necessary, use the app's Reboot action after a dependency or config update.

## Tests

From the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Ten offline tests cover JSON parsing, Unicode, malformed fields, report formatting, sample loading, validation, all four result categories, HTML escaping, stale-result warnings, clearing, and failure handling. The UI tests mock the Google client: passing tests do **not** establish live API availability or model accuracy.

## Privacy and limitations

- Submitted messages go to Google's hosted AI service and are subject to its API terms. Remove OTPs, credentials, bank details, and other private information first.
- The app does not persist messages in a database. Text and the latest assessment are held in the Streamlit session; **Clear** removes them from app session state, not from Google's systems.
- A model can miss a scam or wrongly flag a legitimate message. Verify important claims through a trusted official channel.
- There is a 45-second timeout per API request. Quota, connection, invalid-response, and authorization failures produce user-facing errors without displaying the raw provider response.
- There is no production authentication or global abuse protection. This is a hackathon prototype.
- Custom CSS uses Streamlit's rendered element selectors, so UI changes in Streamlit may require style updates. The dependencies are pinned to the versions used for the offline checks.

## Development and attribution

Development used LLM assistance for coding, interface iteration, and documentation. Describe the parts you implemented, reviewed, and tested accurately, and follow the event's disclosure rules. This project uses Google's hosted Gemma model; it does not train a custom scam classifier.

## Next steps

- Build a consented, anonymized evaluation set of real and legitimate messages in all three language styles.
- Measure missed scams and false alarms before making accuracy claims.
- Improve Nepali explanations and test them with native speakers.
- Evaluate screenshot OCR only after the text workflow is reliable.

For a deadline-focused deployment walkthrough, demo script, and code explanation, see [START_HERE.md](START_HERE.md).

## References

- [Gemma through the Gemini API](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api)
- [Streamlit configuration](https://docs.streamlit.io/develop/api-reference/configuration/config.toml)
- [Streamlit Cloud settings and secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-settings)
- [Streamlit app testing](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest)
