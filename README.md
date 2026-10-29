# Mosquito Mayhem — Three Rooms + Racket (No JavaScript)

## Setup

1. Open this folder in VS Code.
2. Install Python dependencies: `python -m pip install -r requirements.txt`
3. Run: `python app.py`
4. Open `http://127.0.0.1:5000`.

## Gameplay

Select **Bedroom**, **Kitchen**, or **Living Room** before starting. Move the mouse over the room to see a racket-shaped cursor. Click moving mosquitoes to make them disappear immediately, without reloading. After the 20th hit the hunt ends visually without reloading, and a **View Results** button appears. Click it once to submit the checked mosquito IDs to Flask for the final score and elapsed time. Hit speed includes the page load before and after the game.

## Technology

HTML, CSS, Python Flask, Jinja. No JavaScript and no database. The racket is a custom PNG used by the CSS `cursor` property. Each mosquito is a checkbox paired with a label; the checked state hides the mosquito. CSS `:has()` detects when all 20 checkboxes are checked and shows the completion screen. All checked boxes are sent to Flask when View Results is clicked.

## Limitations

Each round has 20 mosquitoes, which do not respawn after being swatted. The page navigates when the round starts and ends, but not between hits. The game does not provide a live timer or continuously track the cursor's position in a separate racket element. On browsers that do not support a custom cursor, the fallback is a crosshair; on touchscreens there is no pointer cursor.

## Deployment note

Set a secure `FLASK_SECRET_KEY` environment variable and turn off Flask's debug mode in production.

## Why View Results needs a click

HTML and CSS cannot automatically submit an HTML form to Flask when the final checkbox becomes checked. The on-page game ends immediately at 20 hits, but the user must press View Results once to navigate to the server-side results page. Elapsed time therefore includes the short delay before View Results is pressed. CSS `:has()` requires a modern browser.
