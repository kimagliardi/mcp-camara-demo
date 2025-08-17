package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func sessionsHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("→ Received request:", r.Method, r.URL.Path)

	if r.Method != http.MethodPost {
		log.Printf("✖ Method not allowed: %s\n", r.Method)
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var payload map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		log.Printf("✖ Failed to parse JSON: %v\n", err)
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	log.Printf("✔ Payload received: %+v\n", payload)

	response := map[string]interface{}{
		"status":  "success",
		"payload": payload,
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("✖ Failed to encode response: %v\n", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
		return
	}

	log.Println("✔ Response sent successfully")
}

func main() {
	addr := "localhost:9000"
	log.Printf("🚀 Server running in DEBUG mode at http://%s/sessions\n", addr)
	http.HandleFunc("/sessions", sessionsHandler)

	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatalf("✖ Server error: %v", err)
	}
}
