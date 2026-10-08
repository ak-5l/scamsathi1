# Finish ScamSathi with three hours left

Your priorities are a working public demo, a clear explanation, and a timely submission. Get the replacement running first; use the remaining time to test and rehearse.

## 1. Replace the files (about 15 minutes)

1. Download and extract `ScamSathi-ready.zip`.
2. Open the inner `scamsathi` folder. You should see `app.py`, `helpers.py`, `requirements.txt`, `README.md`, `START_HERE.md`, `.gitignore`, `.streamlit`, and `tests`.
3. Make a backup of your current project **outside** its Git repository.
4. Copy the extracted folder's **contents** into your existing project folder, replacing matching files. Keep your existing `.git` folder. If you already have `.streamlit/secrets.toml`, keep it; copy `config.toml` into the same `.streamlit` folder.
5. Keep any unrelated files you already have. Do not upload the ZIP itself as the application.

The added `.streamlit/config.toml` matters: do not skip it because its folder begins with a dot.

## 2. Run locally (about 20 minutes)

In File Explorer, open the project folder containing `app.py`. Right-click an empty area and open a terminal there. In PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If you already have `.venv`, the first command can be skipped. Use the URL printed in the terminal. Keep this terminal running while testing the app. Press Ctrl+C to stop it later.

**Run tests from the project root, not from inside `tests`.** The command discovers the tests subfolder relative to where you run it.

If the local app has no server secret, use **Connection settings** at the bottom to enter your own Google AI Studio key. Do not send the key in chat, include it in screenshots, or commit it to Git.

## 3. Check the actual interface (about 15 minutes)

The redesigned app has a paper-colored background, a red SS mark, the heading “A second look. Before you trust it.”, and two numbered sections. On a narrow screen, the assessment should appear below the message editor.

- On desktop, confirm all four sample buttons, the message field, Check, and Clear are usable.
- Reduce the browser window width, or open your eventual deployed app on your phone. Check for horizontal scrolling, clipped text, and hard-to-read buttons.
- Click each sample. Confirm it replaces the text and removes the previous assessment.
- Click Clear. Confirm both the text and the result are gone.
- Check a short message such as `Hi`. Confirm you see a helpful validation message.
- With a valid key, check a sample. Then edit the text. Confirm the old result has a warning until you check again.
- Download an assessment and open it. Confirm it contains the exact analyzed message.

Automated behavior tests passed in the prepared environment; live browser layout and real API output still need these checks on your machine and deployment.

## 4. Push the update (about 15 minutes)

If you use GitHub Desktop, inspect Changes, confirm no secrets are present, commit, and use **Push origin**.

If you use Git in PowerShell, from your existing repository root:

```powershell
git status
git diff -- app.py helpers.py requirements.txt README.md
git add app.py helpers.py requirements.txt README.md START_HERE.md .gitignore .streamlit/config.toml tests/test_app.py tests/test_helpers.py
git diff --cached --stat
git diff --cached
git commit -m "Refine ScamSathi interface and assessment handling"
git push
```

Read the staged diff before committing. Never stage `.streamlit/secrets.toml`, `.env`, or a real API key. Use the branch already connected to your Streamlit deployment; do not create an unrelated repository unless necessary.

If Git says this is not a repository, you are in the extracted copy rather than your existing Git project. Move back to the existing project folder. If push requires authentication, sign in through your usual GitHub flow on your computer.

## 5. Update the deployed app (about 15 minutes)

Your existing Streamlit Cloud app should pick up updates to its connected branch. Watch its build logs. If it fails, use the first error in the logs to diagnose it.

At https://share.streamlit.io/, find your app and open **Settings → Secrets**. Set this if it is not already present:

```toml
GEMINI_API_KEY = "YOUR_REAL_GOOGLE_AI_STUDIO_KEY"
```

Keep your other existing secrets. Save. Use **Reboot** if the app still appears stale or needs a restart after configuration changes.

Test the public app in an incognito window. A visitor should be able to check a message without entering a key. **The absence of a key-entry box only means a key is configured; it does not prove the key works.** Run a real check.

## 6. Test the model (about 30 minutes)

Use invented messages rather than real private messages. Results are model judgments and can vary.

| Message | What to look for |
| --- | --- |
| Bank KYC sample | Identifies the OTP request, deadline pressure, and unverified link; suggests an official bank contact. |
| Prize offer sample | Understands the Romanized Nepali demand for an upfront fee. |
| Job offer sample | Notices the registration payment and unrealistic earnings. |
| Class reminder sample | Avoids declaring an ordinary reminder a scam. |
| `Your order is ready. Please collect it from our usual shop tomorrow.` | Allows a legitimate explanation; does not flag every request as malicious. |
| `Bank bata call aayo, OTP share garnu parcha re natra account block huncha.` | Interprets the OTP demand and threat in Romanized Nepali. |
| `तपाईंको खाता बन्द हुँदैछ। तुरुन्त आफ्नो OTP पठाउनुहोस्।` | Handles Nepali text and identifies the credential request. |
| `Please confirm the payment.` | Recognizes missing context rather than inventing facts about the sender. |

Write down anything wrong. Do not call a few successful examples “99% accuracy.” If there is a real failure, record it as a limitation. Never substitute hardcoded results and present them as live AI output.

## 7. Understand the code (about 20 minutes)

Read these functions in order:

| Part | Explanation you should be able to give |
| --- | --- |
| `main()` in `app.py` | Builds the interface, reads the input, validates it, and starts a check when the user presses the button. |
| `EXAMPLES` | Four synthetic messages for quickly trying the app; these are inputs, not prewritten model results. |
| `get_configured_key()` | Loads a server key from Streamlit secrets or the environment without displaying it. |
| `analyze()` | Sends a cautious prompt and the pasted message to hosted Gemma; asks for JSON and limits each request to 45 seconds. |
| `parse_analysis()` in `helpers.py` | Accepts JSON or fenced JSON, normalizes risk labels, limits lists, and supplies useful fallbacks. |
| `st.session_state` | Holds the current input and latest result between Streamlit reruns. It is not a permanent message database. |
| `show_assessment()` | Renders a readable assessment and escapes dynamic text so model output is not interpreted as custom HTML. |
| `reset_message()` | Loads a sample or clears input; also removes the previous result. |
| `friendly_error()` | Converts failures into understandable messages without displaying raw provider details. |
| `format_report()` | Builds the plain-text download. |
| `.streamlit/config.toml` and `CSS` | Define the base theme and the more deliberate typography, spacing, and visual hierarchy. |

The prompt requests careful reasoning, but the app does not independently verify the model's conclusions. JSON parsing validates the format, not factual accuracy.

## 8. Prepare the demo and submit (about 35 minutes)

Use the exact deliverables requested by your event. Check whether it needs a repository URL, live URL, video, description, screenshots, or AI-assistance disclosure. Submit before the deadline; polish a recording only after the links work.

### A 60–90 second demo

1. **Problem:** “A message can pressure you to act before you notice the warning signs. That is especially tricky when it is written in everyday Romanized Nepali.”
2. **Product:** “ScamSathi gives a second opinion on English, Nepali, and Romanized Nepali messages.”
3. **Live check:** Load Bank KYC and check it. Explain the actual output: risk indicators, specific clues, and safer next steps.
4. **Language example:** Check Prize offer. Point out whether it correctly identifies the upfront fee.
5. **Legitimate example:** Check Class reminder to show why context matters.
6. **Technical explanation:** “It uses Python and Streamlit, calls Google's hosted Gemma model, normalizes the JSON response, and shows a readable assessment. I added checks for malformed responses, stale results, and API failures.”
7. **Limits:** “It does not verify a sender or visit links, and it can be wrong. My next step is to evaluate it on a representative multilingual dataset.”

For a short demo, choose two examples rather than rushing all three. If a live API call fails, explain the failure and show a previously recorded genuine successful run, clearly labeling it as recorded.

### Submission description — edit to reflect your own work

ScamSathi is a message-screening prototype for people in Nepal. Users paste an SMS, WhatsApp message, or email and receive an explanation of possible scam indicators and practical precautions. It uses hosted Gemma 4 to interpret English, Nepali, and Romanized Nepali text, with a Streamlit interface and a downloadable assessment. It does not verify senders or websites, and its multilingual accuracy has not yet been measured. Development used LLM assistance; the project includes offline parser and UI tests.

### Likely judging questions

- **Did you train a model?** No. It uses Google's hosted Gemma model with a task-specific prompt.
- **How is it different from asking a chatbot?** It supplies a focused workflow, multilingual input, consistent result categories, specific precautions, and an export. That is a useful product wrapper; it is not a new model or a claim of superior accuracy.
- **How accurate is it?** Not established. Synthetic examples demonstrate behavior, not a measured accuracy rate. A labeled evaluation set is the next step.
- **What did AI help with?** Answer honestly about generation, debugging, design, and documentation; describe what you personally reviewed and tested. Follow the event's rules.
- **What would you improve?** Multilingual evaluation, better native-language explanations, and production abuse controls before broad public use.

## Fast troubleshooting

| Symptom | First action |
| --- | --- |
| No sample fills the field | Confirm you replaced `app.py`; restart your local Streamlit process. |
| Theme looks wrong | Confirm `.streamlit/config.toml` is in the root project folder and committed; run Streamlit from that folder. Reboot Cloud if needed. |
| Connection settings visible to judges | Configure `GEMINI_API_KEY` in the deployed app's Secrets. Your local secret is not automatically uploaded. |
| Authorization failure | Check the deployed key and API access in Google AI Studio. Do not publish the key. |
| Request limit reached | Wait and inspect the API quota in your Google account. Repeated clicks will not fix the quota. |
| Model unavailable | Check that `gemma-4-26b-a4b-it` is available to your key/account. Do not silently switch to another model and keep claiming Gemma. |
| No usable assessment | Retry once. The model may have returned malformed or incomplete JSON. |
| `No module named ...` | Install `requirements.txt` using the same Python executable you use to run Streamlit. |
| `Start directory is not importable: 'tests'` | Return to the root folder containing `app.py`, then run the test command. |
| Cloud fails after the push | Read the build logs; confirm requirements and entrypoint. Send the error text for help, with keys removed. |

Keep approximately 15 minutes as a buffer. If time is tight, reduce rehearsal time before cutting the live-deployment test or submission.
