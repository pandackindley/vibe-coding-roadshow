// vibe-coding-roadshow: Mastermind Web App
// This Go program serves a simple landing page and a Mastermind game page.
// The game logic and UI are implemented using Go's net/http and HTML/JS.
package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

// Secret code for the current game
var secretCode []string

// Generate a random code of 4 colors
func generateCode() []string {
	colors := []string{"Red", "Blue", "Green", "Yellow", "Orange", "Purple"}
	rand.Seed(time.Now().UnixNano())
	code := make([]string, 4)
	for i := 0; i < 4; i++ {
		code[i] = colors[rand.Intn(len(colors))]
	}
	return code
}

// Serve the landing page
func landingPage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, `<html><head><title>Mastermind</title></head><body>
	   <h1>Welcome to Mastermind!</h1>
	   <a href="/game"><button>New Game</button></a>
	   </body></html>`)
}

// Serve the game page (HTML/JS)
func gamePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, `
			  <!DOCTYPE html>
			  <html lang="en">
			  <head>
					  <meta charset="UTF-8">
					  <meta name="viewport" content="width=device-width, initial-scale=1.0">
					  <title>Mastermind Game</title>
					  <style>
							  body { font-family: Arial, sans-serif; background: #e0f7fa; text-align: center; padding-top: 40px; }
							  h1 { color: #0078d4; }
							  .peg { width: 32px; height: 32px; border-radius: 50%; display: inline-block; margin: 4px; cursor: grab; border: 2px solid #888; box-shadow: 0 2px 4px #aaa; }
							  .peg.Red { background: #e53935; }
							  .peg.Blue { background: #1e88e5; }
							  .peg.Green { background: #43a047; }
							  .peg.Yellow { background: #ffff00; }
							  .peg.Orange { background: #fb8c00; }
							  .peg.Purple { background: #fff; border: 2px solid #888; }
							  .slot { width: 34px; height: 34px; border-radius: 50%; border: 2px dashed #bbb; display: inline-block; margin: 4px; vertical-align: middle; background: #fff; }
							  .slot.filled { border-style: solid; }
							  .guess-row { margin: 10px 0; }
							  .board { margin: 0 auto; max-width: 400px; }
							  .result { margin-top: 20px; font-size: 1.1em; }
							  .disabled { opacity: 0.5; pointer-events: none; }
					  </style>
			  </head>
			  <body>
					  <h1>Mastermind</h1>
					  <p>Drag and drop colored pegs into the slots to make your guess.<br>
					  <b>Black</b> = correct color & position, <b>White</b> = correct color, wrong position.<br>
					  You have 10 guesses.</p>
					  <div id="pegTray">
							  <span class="peg Red" draggable="true" data-color="Red"></span>
							  <span class="peg Blue" draggable="true" data-color="Blue"></span>
							  <span class="peg Green" draggable="true" data-color="Green"></span>
							  <span class="peg Yellow" draggable="true" data-color="Yellow"></span>
							  <span class="peg Orange" draggable="true" data-color="Orange"></span>
							  <span class="peg Purple" draggable="true" data-color="Purple"></span>
					  </div>
					  <div class="board" id="board"></div>
					  <div class="result" id="result"></div>
					  <button onclick="location.reload()">Restart Game</button>
					  <a href="/">Back to Home</a>
					  <script>
					  // Mastermind drag-and-drop board
					  const maxGuesses = 10;
					  let currentRow = 0;
					  let history = [];
					  let gameOver = false;
					  const colors = ["Red","Blue","Green","Yellow","Orange","Purple"];

					  function pegColor(color) {
						  switch(color) {
							  case 'Red': return '#e53935';
							  case 'Blue': return '#1e88e5';
							  case 'Green': return '#43a047';
							  case 'Yellow': return '#ffff00';
							  case 'Orange': return '#fb8c00';
							  case 'Purple': return '#fff';
							  default: return '#fff';
						  }
					  }

					  function createRow(rowNum) {
						  const row = document.createElement('div');
						  row.className = 'guess-row';
						  row.id = 'row-' + rowNum;
						  for (let i = 0; i < 4; i++) {
							  const slot = document.createElement('span');
							  slot.className = 'slot';
							  slot.id = 'slot-' + rowNum + '-' + i;
							  slot.ondragover = e => { e.preventDefault(); };
							  slot.ondrop = function(e) {
								  if (gameOver || rowNum !== currentRow) return;
								  const color = e.dataTransfer.getData('color');
								  if (!colors.includes(color)) return;
								  // Remove any previous peg/color and remove button
								  slot.className = 'slot';
								  slot.removeAttribute('data-color');
								  slot.style.background = '#fff';
								  slot.style.borderStyle = 'dashed';
								  let oldBtn = slot.querySelector('.remove-btn');
								  if (oldBtn) oldBtn.remove();
								  // Now set new color
								  slot.className = 'slot filled ' + color;
								  slot.setAttribute('data-color', color);
								  slot.style.background = pegColor(color);
								  slot.style.borderStyle = 'solid';
								  // Add remove button
								  let removeBtn = document.createElement('span');
								  removeBtn.textContent = '⨯';
								  removeBtn.className = 'remove-btn';
								  removeBtn.style.cursor = 'pointer';
								  removeBtn.style.position = 'absolute';
								  removeBtn.style.right = '-10px';
								  removeBtn.style.top = '-10px';
								  removeBtn.style.background = '#fff';
								  removeBtn.style.borderRadius = '50%';
								  removeBtn.style.fontSize = '16px';
								  removeBtn.style.padding = '2px';
								  removeBtn.onclick = function(ev) {
									  ev.stopPropagation();
									  slot.className = 'slot';
									  slot.removeAttribute('data-color');
									  slot.style.background = '#fff';
									  slot.style.borderStyle = 'dashed';
									  removeBtn.remove();
								  };
								  slot.style.position = 'relative';
								  slot.appendChild(removeBtn);
							  };
							  row.appendChild(slot);
						  }
						  const submitBtn = document.createElement('button');
						  submitBtn.textContent = 'Guess';
						  submitBtn.onclick = function() { submitGuess(rowNum); };
						  row.appendChild(submitBtn);
						  const feedback = document.createElement('span');
						  feedback.className = 'feedback';
						  feedback.id = 'feedback-' + rowNum;
						  row.appendChild(feedback);
						  return row;
					  }

					  function renderBoard() {
						  const board = document.getElementById('board');
						  board.innerHTML = '';
						  for (let i = 0; i < maxGuesses; i++) {
							  board.appendChild(createRow(i));
						  }
						  updateRows();
					  }

					  function updateRows() {
						  for (let i = 0; i < maxGuesses; i++) {
							  const row = document.getElementById('row-' + i);
							  if (i !== currentRow) row.classList.add('disabled');
							  else row.classList.remove('disabled');
						  }
					  }

					  function submitGuess(rowNum) {
						  if (gameOver || rowNum !== currentRow) return;
						  let guess = [];
						  for (let i = 0; i < 4; i++) {
							  const slot = document.getElementById('slot-' + rowNum + '-' + i);
							  const color = slot.getAttribute('data-color');
							  if (!colors.includes(color)) {
								  alert('Please fill all slots with pegs!');
								  return;
							  }
							  guess.push(color);
						  }
						  // Send guess to backend
						  const params = new URLSearchParams();
						  guess.forEach((color, i) => params.append('guess'+i, color));
						  fetch('/guess', {
							  method: 'POST',
							  headers: {'Content-Type': 'application/x-www-form-urlencoded'},
							  body: params.toString()
						  }).then(res => res.json()).then(data => {
							  history.push('<b>' + guess.join(', ') + '</b>: ' + data.black + ' black, ' + data.white + ' white');
							  document.getElementById('feedback-' + rowNum).innerHTML = data.black + ' black, ' + data.white + ' white';
							  document.getElementById('result').textContent = data.message;
							  if (data.win || currentRow === maxGuesses - 1) {
								  gameOver = true;
								  document.getElementById('result').textContent += data.win ? '' : ' Game over!';
							  } else {
								  currentRow++;
								  updateRows();
							  }
						  });
					  }

					  // Peg drag events
					  document.querySelectorAll('.peg').forEach(peg => {
						  peg.ondragstart = function(e) {
							  e.dataTransfer.setData('color', peg.getAttribute('data-color'));
						  };
					  });

					  renderBoard();
					  updateRows();
					  </script>
			  </body>
			  </html>
	  `)
}

// Standard library imports

// ...rest of code...
func guessHandler(w http.ResponseWriter, r *http.Request) {
	r.ParseForm()
	guess := []string{
		r.FormValue("guess0"),
		r.FormValue("guess1"),
		r.FormValue("guess2"),
		r.FormValue("guess3"),
	}
	// Generate a new code if needed
	if len(secretCode) != 4 {
		secretCode = generateCode()
	}
	// Score the guess
	black, white := mastermindScore(secretCode, guess)
	win := black == 4
	msg := ""
	if win {
		msg = "You win! The code was " + fmt.Sprintf("%v", secretCode)
		secretCode = nil // Reset for next game
	} else {
		msg = "Try again!"
	}
	// Respond with JSON
	resp := map[string]interface{}{
		"black":   black,
		"white":   white,
		"win":     win,
		"message": msg,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

// mastermindScore compares the guess to the code and returns
// the number of black (correct color & position) and white (correct color, wrong position) pegs.
func mastermindScore(code, guess []string) (int, int) {
	black, white := 0, 0
	usedCode := make([]bool, 4)
	usedGuess := make([]bool, 4)
	// First pass: count black pegs
	for i := 0; i < 4; i++ {
		if guess[i] == code[i] {
			black++
			usedCode[i] = true
			usedGuess[i] = true
		}
	}
	// Second pass: count white pegs
	for i := 0; i < 4; i++ {
		if usedGuess[i] {
			continue
		}
		for j := 0; j < 4; j++ {
			if usedCode[j] {
				continue
			}
			if guess[i] == code[j] {
				white++
				usedCode[j] = true
				break
			}
		}
	}
	return black, white
}

// main sets up the HTTP server and routes.
func main() {
	// Serve landing page at '/'
	http.HandleFunc("/", landingPage)
	// Serve game page at '/game', generate new code on GET
	http.HandleFunc("/game", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "GET" {
			secretCode = generateCode()
		}
		gamePage(w, r)
	})
	// Handle guesses at '/guess'
	http.HandleFunc("/guess", guessHandler)
	fmt.Println("Server running on http://localhost:8080 ...")
	// Start server on port 8080
	http.ListenAndServe(":8080", nil)
}
