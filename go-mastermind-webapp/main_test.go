package main

import (
	"testing"
)

func TestGenerateCodeLengthAndColors(t *testing.T) {
	code := generateCode()
	if len(code) != 4 {
		t.Errorf("Code length should be 4, got %d", len(code))
	}
	validColors := map[string]bool{"Red": true, "Blue": true, "Green": true, "Yellow": true, "Orange": true, "Purple": true}
	for _, c := range code {
		if !validColors[c] {
			t.Errorf("Code color invalid: %s", c)
		}
	}
}

func TestMastermindScore_BlackAndWhite(t *testing.T) {
	// code: [Red, Blue, Green, Yellow], guess: [Red, Green, Blue, Yellow] => 2 black, 2 white
	black, white := mastermindScore(
		[]string{"Red", "Blue", "Green", "Yellow"},
		[]string{"Red", "Green", "Blue", "Yellow"},
	)
	if black != 2 || white != 2 {
		t.Errorf("Expected 2 black, 2 white, got %d black, %d white", black, white)
	}

	// code: [Red, Red, Blue, Blue], guess: [Blue, Blue, Red, Red] => 0 black, 4 white
	black, white = mastermindScore(
		[]string{"Red", "Red", "Blue", "Blue"},
		[]string{"Blue", "Blue", "Red", "Red"},
	)
	if black != 0 || white != 4 {
		t.Errorf("Expected 0 black, 4 white, got %d black, %d white", black, white)
	}

	// code: [Red, Blue, Green, Yellow], guess: [Red, Blue, Green, Yellow] => 4 black, 0 white
	black, white = mastermindScore(
		[]string{"Red", "Blue", "Green", "Yellow"},
		[]string{"Red", "Blue", "Green", "Yellow"},
	)
	if black != 4 || white != 0 {
		t.Errorf("Expected 4 black, 0 white, got %d black, %d white", black, white)
	}
}
