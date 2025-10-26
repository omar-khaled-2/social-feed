package main

import (
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // allow all origins for demo
	},
}

var clients = make(map[*websocket.Conn]bool)
var mutex = sync.Mutex{}

type WebsocketMessage struct {
	Action  string      `json:"action"`
	Payload interface{} `json:"payload"`
}

func BroadcastMessage(message WebsocketMessage) {
	mutex.Lock()
	defer mutex.Unlock()

	for conn := range clients {
		err := conn.WriteJSON(message)
		if err != nil {
			conn.Close()
			delete(clients, conn)
		}
	}
}

func HandleWebSocket(w http.ResponseWriter, r *http.Request) {
	conn, _ := upgrader.Upgrade(w, r, nil)
	defer conn.Close()

	mutex.Lock()
	clients[conn] = true
	mutex.Unlock()
	for {
		_, _, err := conn.ReadMessage()
		if err != nil {
			conn.Close()
			mutex.Lock()
			delete(clients, conn)
			mutex.Unlock()
			break
		}

	}
}
