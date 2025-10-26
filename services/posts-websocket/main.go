package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"
	"strconv"

	"time"

	env "github.com/joho/godotenv"
	"github.com/lib/pq"

	amqp "github.com/rabbitmq/amqp091-go"
)

type User struct {
	Id       int    `json:"name"`
	Username string `json:"username"`
}

type Post struct {
	Id          int      `json:"id"`
	Description string   `json:"description"`
	Created_at  string   `json:"created_at"`
	User        User     `json:"user"`
	Is_liked    bool     `json:"is_liked"`
	Image_urls  []string `json:"image_urls"`
	Likes_count int      `json:"likes_count"`
}

func getPost(db *sql.DB, id int) Post {
	rows, err := db.Query(
		`SELECT post.id,users.id as owner_id,array_remove(array_agg(image_key.key), NULL) as image_keys, username as owner_username,post.description,post.created_at from posts as post
		INNER JOIN users on users.id = post.owner_id
		LEFT JOIN image_key on image_key.post_id = post.id
		WHERE post.id = $1
		GROUP BY post.id , users.id`, id)
	if err != nil {
		log.Fatal(":", err)
	}

	defer rows.Close()
	rows.Next()
	var post Post
	var user User
	rows.Scan(&post.Id, &user.Id, pq.Array(&post.Image_urls), &user.Username, &post.Description, &post.Created_at)
	post.User = user
	post.Is_liked = false
	post.Likes_count = 0
	return post
}

func main() {

	env.Load()

	amqp_url := os.Getenv("AMQP_URL")
	queue_name := os.Getenv("QUEUE_NAME")
	database_url := os.Getenv("DATABASE_URL")

	db, err := sql.Open("postgres", database_url)
	if err != nil {
		log.Fatal("Failed to open DB:", err)
	}
	defer db.Close()
	conn, _ := amqp.Dial(amqp_url)

	channel, _ := conn.Channel()
	queue, _ := channel.QueueDeclare(
		queue_name, // name
		false,      // durable
		false,      // delete when unused
		false,      // exclusive
		false,      // no-wait
		nil,        // arguments
	)

	http.HandleFunc("/", HandleWebSocket)

	msgs, _ := channel.Consume(
		queue.Name, // queue
		"",         // consumer
		true,       // auto-ack
		false,      // exclusive
		false,      // no-local
		false,      // no-wait
		nil,        // args
	)

	msgChannel := make(chan amqp.Delivery, 100)

	forever := make(chan bool)

	go func() {

		http.ListenAndServe(":8080", nil)

	}()

	go func() {
		for msg := range msgs {
			msgChannel <- msg
		}
	}()

	go func() {
		ticker := time.NewTicker(5 * time.Second)
		defer ticker.Stop()
		for range ticker.C {
			msg := <-msgChannel
			id, _ := strconv.Atoi(string(msg.Body))
			post := getPost(db, id)
			message := WebsocketMessage{
				Action:  "created",
				Payload: post,
			}
			BroadcastMessage(message)
		}
	}()

	<-forever
}
